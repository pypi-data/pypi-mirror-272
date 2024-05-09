# -*- coding: utf-8 -*-
# @Time   :08/05/2024 6:03 pm
# @Author :UPEX_FCC
# @Email  :cc.cheng@bitget.com
# @Site   :
# @File   :setup.py

import setuptools

setuptools.setup(
    name='cc_report',
    version='0.0.2',
    packages=setuptools.find_packages(),
    license='MIT',
    author='cc.cheng',
    author_email='chaicc145@gmail.com',
    description='A MODIFIED REPORT',
    install_requires=['pytest', 'jinja2'],
    # data_files=[('cc_report',['aa.ini'])],
    package_data={"": ['*.html']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
