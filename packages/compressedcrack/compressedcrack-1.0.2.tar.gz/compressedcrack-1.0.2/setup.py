from setuptools import setup, find_packages

setup(
    name='compressedcrack',
    version='1.0.2',
    description='A command-line tool to crack password-protected compressed files using brute force.',
    author='Thanh Minh',
    author_email='thanhdoantranminh@gmail.com',
    url='https://github.com/mnismt/CompressedCrack',
    packages=find_packages(),
    install_requires=[
        'patoolib',
    ],
    entry_points={
        'console_scripts': [
            'compressedcrack = main:main',
        ],
    },
)
