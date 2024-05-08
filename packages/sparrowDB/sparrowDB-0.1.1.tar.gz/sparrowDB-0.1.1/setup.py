from setuptools import setup, find_packages

setup(
    name='sparrowDB',
    version='0.1.1',
    description='基于Python字典的内存数据库',
    packages=find_packages(),
    python_requires='>=3.11',
    install_requires=['sparrowApi', 'colorama']
)

