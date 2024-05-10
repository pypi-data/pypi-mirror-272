# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
setup(
    name='hebill_html',
    version='1.0.1',
    description='python生成HTML代码',
    long_description=open(r'D:\SDK\GitHub\python_hebill_html\hebill_html\README.MD', encoding='utf-8').read(),
    long_description_content_type='text/plain',
    packages=find_packages(),
    package_data={
        '': ['*.md', '*.MD'],
    },
    install_requires=[
    ],
    python_requires='>=3.12',
)
