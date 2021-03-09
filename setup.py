from setuptools import setup, find_packages

setup(
    packages=find_packages(exclude=['contrib', 'docs', 'tests', 'examples']),
    install_requires=[
        'beautifulsoup4>=4.9.1',
        'numpy>=1.18.5',
        'requests>=2.24.0',
        'yfinance>=0.1.54',
        'pandas>=1.1.2',
        'lxml>=4.5.2'
    ]
)