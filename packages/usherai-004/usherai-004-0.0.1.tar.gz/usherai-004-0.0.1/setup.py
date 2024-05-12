from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.00.01'
DESCRIPTION = 'Experimental A.I. Intergration Module, including text to speech'
LONG_DESCRIPTION = 'Experimental Python terminal created by Bertran Usher. Purpose: Create automated processes.'

# Setting up
setup(
    name="usherai-004",
    version=VERSION,
    author="Bertran Usher",
    author_email="<bjusher820@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['openai','pyttsx3'],
    keywords=['python', 'openai', 'ai', 'artificial intelligence'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)