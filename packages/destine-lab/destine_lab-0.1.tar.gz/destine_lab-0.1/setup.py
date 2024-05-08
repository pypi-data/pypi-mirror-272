from setuptools import setup, find_packages

setup(
    name='destine_lab',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'lxml',
    ],
)
