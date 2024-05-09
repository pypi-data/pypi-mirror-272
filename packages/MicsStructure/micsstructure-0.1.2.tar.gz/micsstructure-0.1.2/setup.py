from setuptools import setup, find_packages

setup(
    name='MicsStructure',
    version='0.1.2',
    packages=find_packages(),
    author='Merbux',
    author_email='krytoi330@mail.ru',
    description='Mics Structure - module for website',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/merbux/MicsStructure',
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
