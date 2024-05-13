from setuptools import setup, find_packages
setup(
name='anemone_daisy_maker',
version='1.55',
author='Silas S. Brown',
author_email='ssb22@cam.ac.uk',
description='Create DAISY digital talking books from HTML text, MP3 audio and JSON time index data',
packages=find_packages(),
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: Apache Software License',
'Operating System :: OS Independent',
],
python_requires='>=3.6',
)
