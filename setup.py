from setuptools import find_packages, setup

setup(
    name='tekstur',
    packages=find_packages(include=['tekstur']),
    version='0.1.0',
    description='Texture generation library',
    author='Steffen Geving',
    install_requires=['pillow'],
    setup_requires=['pytest-runner'],
    tests_requires=['pytest==7.4.4'],
    test_suite='tests',
)