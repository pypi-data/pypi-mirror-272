# -*-coding:utf-8-*-

import setuptools                                    #导入setuptools打包工具
 
setuptools.setup(
    name="zitools",                                  # 发布wheel包名
    version="0.0.1",                                 # 包版本号
    author="Momodo",                                 # 作者
    author_email="momodosky@outlook.com",            # 作者联系方式
    description="A small example package",           # 包的简述
    long_description='long_description',             # 包的详细介绍，一般在README.md文件内, 或者用字符串定义
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",     # 自己项目地址，比如github的项目地址
    packages=setuptools.find_packages(),
    # packages=['zitools',]                            # python项目文件夹的名字，安装包名。和name保持一致
    python_requires='>=3.6',                         #对python的最低版本要求
)
