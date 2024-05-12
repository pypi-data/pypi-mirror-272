from setuptools import setup, find_packages


# read the contents of your README file
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='g2opy',
    version='0.0.5',
    package_dir={'g2opy': 'g2opy'},
    packages=find_packages(),
    include_package_data=True,
    description='g2o for python',
    author='ubicoders',
    keywords='g2o, SLAM, BA, ICP, optimization, python, binding',
    author_email='info@ubicoders.com',
    long_description=long_description,
    long_description_content_type='text/markdown',  # This is important for Markdown files
)