from setuptools import setup, find_packages

setup(
    name='g2opy',
    version='0.0.1',
    package_dir={'g2opy': 'g2opy'},
    packages=find_packages(),
    include_package_data=True,
    description='Simple package containing a shared object library',
    author='Your Name',
    author_email='your.email@example.com'
)