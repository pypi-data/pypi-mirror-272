from setuptools import setup, find_packages
setup(
name='textbr',
version='0.1.0',
author='Foundation Scott',
author_email='foundationscott.vercel.app@gmail.com',
description="A package with basic helpful functions for text-based games which can be imported like so 'from textbr import *'\nThe package contains the following functions: \n'wait(seconds)' - Makes the code wait a few seconds\n'clear()' - Clears the console screen\n'bgm(file_path)'",
packages=find_packages(),
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.6',
)