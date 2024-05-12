from setuptools import setup, find_packages

setup(
    name='mr_hawk',
    version='0.1',
    packages=find_packages(),
    description='A Python package to install external libraries that we need in our code',
    author='Nyctophile',
    author_email='shanumartin3@gmail.com',
    entry_points={
        'console_scripts': [
            'mr_hawk = Night:main'
        ]
    },
    install_requires=[],
)
