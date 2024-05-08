# -*- coding: utf-8 -*- 
"""
Author: JerryLaw
Time: 2024/5/8 17:01
Email: 623487850@qq.com
"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="JerryMSScript",
    version="1.0",
    author="JerryLaw",
    author_email="623487850@qq.com",
    description="乱写的项目",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    package_data={'': ['*.yaml', '*.csv', '*.txt', '.toml']},
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'jsonpath<=0.82.2',
        'redis<=3.5.3',
        'redis-py-cluster<=2.1.3'
    ],  # 项目依赖，也可以指定依赖版本
)
