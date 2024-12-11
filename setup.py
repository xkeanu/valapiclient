from setuptools import setup, find_packages

VERSION = '1.1.2'
DESCRIPTION = 'Python package for Unofficial Valorant API'
LONG_DESCRIPTION = 'A package that allows you to interact with the Valorant API.'

setup(
    name="valapiclient",
    version=VERSION,
    author="xkeanu",
    author_email="keanu.code@proton.me",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        'requests',
        'pythonping',
        'urllib3'
    ],
    keywords=[
        'valorant', 'api', 'valorant-api', 'valorant-client', 
        'insta-lock', 'valorant-python', 'stats', 'riot', 'riot-games'
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]   
)