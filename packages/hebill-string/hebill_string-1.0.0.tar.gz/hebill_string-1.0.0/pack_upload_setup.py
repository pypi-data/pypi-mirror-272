# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
setup(
    name='hebill_string',
    version='1.0.0',
    description='python字符串扩展类',
    long_description=open(r'D:\SDK\GitHub\python_hebill_string\hebill_string\README.MD', encoding='utf-8').read(),
    long_description_content_type='text/plain',
    packages=find_packages(),
    package_data={
        '': ['*.md', '*.MD'],
    },
    install_requires=[
    ],
    python_requires='>=3.12',
)
