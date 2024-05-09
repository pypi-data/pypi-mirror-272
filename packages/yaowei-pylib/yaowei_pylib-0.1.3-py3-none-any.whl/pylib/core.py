import copy
import os
import platform
import re
import time
import uuid
from datetime import datetime, timedelta

import boto3
import redis
from boto3 import Session
from botocore.exceptions import ClientError

def dict_merge(dct, *merge_dcts):
    """
    merge multiple dicts.
    merge
         {"a": 1, "b": {"c": 2},         "c": 5       , "d": {"e": 6},  "f": [1,2] }
         {"a": 2, "b": {"d": 3},         "c": {"d": 4}, "d": 5    ,     "f": [2,3] }
       = {"a": 2, "b": {"c": 2, "d": 3}, "c": {"d": 4}, "d": 5    ,     "f": [1,2,3] }
    :param dct: the source dict.
    :type dct: dict.
    :param merge_dcts: the dicts that would be merged into dct.
    :type merge_dcts: array dicts.
    """
    for merge_dct in merge_dcts:
        if merge_dct is None:
            continue
        for k in merge_dct:
            if k in dct and type(dct[k]) is dict and type(merge_dct[k]) is dict:
                dict_merge(dct[k], merge_dct[k])
            elif k in dct and type(dct[k]) is list and type(merge_dct[k]) is list:
                for t in merge_dct[k]:
                    if t not in dct[k]:
                        dct[k].append(t)
            else:
                dct[k] = copy.deepcopy(merge_dct[k])
    return dct


def average(values):
    """Calculate the average of a list of numbers."""
    if not values:
        return 0
    return sum(values) / len(values)


__built_in_role = {
    "ipsyprod": "arn:aws:iam::769100407790:role/PowerUserAccess"
}


def get_aws_token(arn_role=None):
    arn_role = None if platform.system() != 'Darwin' else arn_role or os.environ.get("arn_role")

    if arn_role:

        sts_client = boto3.client('sts')
        assumed_role = sts_client.assume_role(
            RoleArn=__built_in_role.get(arn_role, arn_role),
            RoleSessionName='AssumedRoleSession'
        )
        boto3.setup_default_session(
            aws_access_key_id=assumed_role['Credentials']['AccessKeyId'],
            aws_secret_access_key=assumed_role['Credentials']['SecretAccessKey'],
            aws_session_token=assumed_role['Credentials']['SessionToken']
        )
        return {
            "AWS_ACCESS_KEY_ID": assumed_role['Credentials']['AccessKeyId'],
            "AWS_SECRET_ACCESS_KEY": assumed_role['Credentials']['SecretAccessKey'],
            "AWS_SESSION_TOKEN": assumed_role['Credentials']['SessionToken']
        }
    else:
        session = Session()
        credentials = session.get_credentials()

        return {
            "AWS_ACCESS_KEY_ID": credentials.access_key,
            "AWS_SECRET_ACCESS_KEY": credentials.secret_key,
            "AWS_SESSION_TOKEN": credentials.token,
            "AWS_S3_ALLOW_UNSAFE_RENAME": "true"
        }

def try_none(func):
    try:
        return func()
    except Exception as _:
        return None


def retry(func, attempts, delay=1, *args, **kwargs):
    for _ in range(attempts):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Retrying...")
            time.sleep(delay)
    raise Exception(f"Failed after {attempts} attempts")


def get_s3_file_content_and_updated_timestamp(bucket_name, key, s3=None):
    """
    获取指定S3存储桶中对象的内容和最后修改时间。

    :param s3:
    :param bucket_name: S3存储桶的名称
    :param key: 对象的键（路径）
    :return: 文件内容和最后修改时间（如果存在），否则返回 None
    """
    try:
        s3 = s3 or boto3.client('s3')
        # 获取对象内容
        response = s3.get_object(Bucket=bucket_name, Key=key)
        content = response['Body'].read().decode('utf-8')

        # 获取最后修改时间
        last_modified = response['LastModified']

        # 格式化最后修改时间
        last_modified_formatted = last_modified.strftime("%Y-%m-%d")

        return content, last_modified_formatted, response['ContentLength']
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            print(f"The object with key '{key}' does not exist in bucket '{bucket_name}'.")
        else:
            print("Error:", e)
        return None, None, None


def parse_csv_content(rows):
    result, temp, inside_quotes = [], '', False

    for row in rows:
        i = 0
        while i < len(row):
            char = row[i]
            if char == '"':
                if i < len(row) - 1 and row[i + 1] == '"':
                    temp += char
                    i += 1
                else:
                    inside_quotes = not inside_quotes
            elif char == ',' and not inside_quotes:
                result.append(temp)
                temp = ''
            else:
                temp += char
            i += 1
        if not inside_quotes:
            result.append(temp)
            yield result
            temp = ''
            result = []
        else:
            temp += "\n"


__pattern = re.compile(r'([^/]+)=([^/]+)/')


def get_s3_csv_content(url, s3=None):
    s3 = s3 or boto3.client('s3')
    bucket, key = url.replace("s3://", "").split("/", 1)
    response = retry(s3.get_object, 3, Bucket=bucket, Key=key)
    content = response['Body'].read().decode('utf-8')
    field_line, *data_lines = [line.strip() for line in content.split("\n") if len(line.strip()) > 10]
    fields = field_line.split(",")

    partitions = dict(__pattern.findall(url))
    for data in parse_csv_content(data_lines):
        yield {
            **partitions,
            **{key: value for key, value in zip(fields, data)},

        }


def get_files_in_bucket(url, s3=None):
    s3 = s3 or boto3.client('s3')
    bucket, key = url.replace("s3://", "").split("/", 1)
    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=bucket, Prefix=key):
        for obj in page.get('Contents', []):
            yield obj['Key']


def date_range(start_date_str, end_date_str):
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    current_date = start_date
    while current_date <= end_date:
        yield current_date.strftime("%Y-%m-%d")  # 使用yield语句产生当前日期字符串
        current_date += timedelta(days=1)  # 增加一天


import hashlib


def sorted_dict_to_md5(d):
    return hashlib.md5(''.join([f"{key}:{d[key]}" for key in sorted(d.keys())]).encode()).hexdigest()


class RedisLock(object):
    def __init__(self, name, redis_config, **kwargs):
        self.redis = redis.StrictRedis(**redis_config)
        self.id = uuid.uuid4().hex
        self.key = f"{name}{sorted_dict_to_md5(kwargs)}"

    def __del__(self):
        if self.redis:
            self.unlock()

    def lock(self, wait=False, timeout=600, fn=lambda x: print(x)):
        index = 0
        while True:
            index += 1
            fn(index)
            ret = self.redis.set(self.key, self.id, ex=timeout, nx=True)
            if ret:
                break
            previous = self.redis.get(self.key)
            if previous and previous.decode('utf-8') == self.id:
                break
            if not wait:
                return False
            time.sleep(2)
        return True

    def unlock(self):
        value = self.redis.get(self.key)
        if value and value.decode('utf-8') == self.id:
            self.redis.delete(self.key)

    def setnx(self, value=None, expire=24 * 3600, nx=True, **kwargs):
        value = value or self.id
        return self.redis.set(sorted_dict_to_md5(kwargs), value, ex=expire, nx=nx)


if __name__ == "__main__":
    locker = RedisLock("aa", redis_config={"host": "10.66.134.122", "password":  "Z4e7QOothx"}, aa="vv", timeout=600)
    locker1 = RedisLock("aa", redis_config={"host": "10.66.134.122", "password":  "Z4e7QOothx"}, aa="vv", timeout=600)
    locker.lock(wait=True)
    locker1.lock(wait=True)

