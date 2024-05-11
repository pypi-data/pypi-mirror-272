from setuptools import setup, find_packages

setup(
    name='control_op_scnu',  # 库的名字
    version='0.1.1',  # 版本号，遵循语义化版本控制
    packages=find_packages(),  # 自动发现并包含所有包
    description='服务于机器人部',  # 简短描述

    author='cpw',  # 作者名
    author_email='1994777538@qq.com',  # 作者邮箱
    url='https://github.com/cpw041130/control_op_scnu',  # 项目主页
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],  # 分类标签
    install_requires=[  # 依赖列表
        'dependency1>=0.1.0',
        'dependency2>=1.0.0',
    ],
)