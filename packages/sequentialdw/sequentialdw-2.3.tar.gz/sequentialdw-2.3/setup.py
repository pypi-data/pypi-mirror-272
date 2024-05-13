from setuptools import setup, find_packages

setup(
    name='sequentialdw',
    version='2.3',
    packages=find_packages(),
    install_requires=['requests', 'time'],
    entry_points={
        'console_scripts': [
            'seqdownload = sequentialdw.seq_download:main'  
        ]
    },
    author='wweziza',
    description='A simple website scrapper with sequential files in it.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
)
