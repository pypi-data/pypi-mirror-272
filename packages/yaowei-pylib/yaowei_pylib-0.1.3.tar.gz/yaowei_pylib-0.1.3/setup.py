from setuptools import setup, find_packages

setup(
    name='yaowei_pylib',
    version='0.1.3',
    packages=find_packages(),
    description='A simple description',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Yaowei',
    author_email='yaoweiu@gmail.com',
    url='https://github.com/yaoweiipsy/pylib',
    install_requires=[
        'requests',
        'boto3'
    ],
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
