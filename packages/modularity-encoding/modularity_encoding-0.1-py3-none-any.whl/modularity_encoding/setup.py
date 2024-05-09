from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()
    
setup(
    name='modularity_encoding',
    version='0.1.3',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'networkx',
        'python-louvain',
        'tqdm',
        'matplotlib'
    ],
    author='Mohsen Askar',
    author_email='ceaser198511@gmail.com',
    description='A package to group healthcode systems using network analysis modularity',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    url='https://github.com/MohsenAskar'
)

