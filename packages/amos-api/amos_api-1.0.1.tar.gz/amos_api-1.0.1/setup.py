import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='amos_api',
    version='1.0.1',
    description='AMOS common api',
    author='ilex.h',
    author_email='390132625@qq.com',
    url='https://github.com/aptray/python-pkg',
    packages=setuptools.find_packages(),
    py_modules=['amos_api'],
)