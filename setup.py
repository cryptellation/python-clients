from setuptools import find_packages, setup

setup(
    name='cryptellation',
    packages=find_packages(),
    version='1.0.0',
    description='Cryptellation Python Library',
    author='Louis FRADIN',
    install_requires=['temporalio==1.11.1'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==7.1.2'],
    test_suite='tests',
)