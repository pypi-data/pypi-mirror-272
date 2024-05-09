from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='PotSql',
    version='1.0',
    author='ForestBu',
    author_email='tvc55.admn@gmail.com',
    description='MySQL Library',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/ForestBu/PotSql',
    packages=find_packages(),
    install_requires=['requests>=2.25.1'],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='mysql MySQL MySql requests request query',
    python_requires='>=3.11'
)
