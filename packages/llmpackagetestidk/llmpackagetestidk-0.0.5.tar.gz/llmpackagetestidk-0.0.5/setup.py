from setuptools import setup, find_packages

VERSION = '0.0.5'
DESCRIPTION = 'A test package for llm'

# Setting up
setup(
    name="llmpackagetestidk",
    version=VERSION,
    author="Mihai Simedrea",
    author_email="mihai.nicolae.simedrea@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
