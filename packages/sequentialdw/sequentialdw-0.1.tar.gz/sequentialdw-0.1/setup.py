from setuptools import setup, find_packages

setup(
    name='sequentialdw',
    version='0.1',
    packages=find_packages(),
    install_requires=['requests'],
    entry_points={
        'console_scripts': [
            'seqdownload = sequentialdw.seq_download:main'  
        ]
    },
    author='wweziza',
    description='A simple website scrapper with sequential files in it.'
)
