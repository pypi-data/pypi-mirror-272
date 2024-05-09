from setuptools import setup, find_packages

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='ezalpy',
    version='0.1',
    description='Modul with System Extension and many more Features, available for Linux and Windows',
    long_description=readme(),
    author='Kevin Alexander Krefting',
    author_email='kakrefting@gmail.com',
    maintainer='Kevin Alexander Krefting',
    maintainer_email='kakrefting@gmail.com',
    url='https://github.com/DevMasterLinux/al.py',
    download_url='https://github.com/DevMasterLinux/al.py/releases/download/0.1/file.tar.gz',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[]
)
