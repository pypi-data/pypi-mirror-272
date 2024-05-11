from setuptools import setup

setup(
    name='focusployer',
    version='1.1',
    packages=['focusployer'],
    author='uni',
    install_requires=[
        'asyncssh',
        'loguru'
    ],
    long_description=open('ReadMe.md').read(),
    long_description_content_type='text/markdown',
)
