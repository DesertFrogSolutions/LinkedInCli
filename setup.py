# https://click.palletsprojects.com/en/8.0.x/setuptools/#setuptools-integration
from setuptools import setup

setup(
    name='linkedin',
    version='0.1.0',
    py_modules=['linkedin'],
    install_requires=[
        'Click',
        'dynaconf',
        'linkedin_api>=2.0.0a'
    ],
    entry_points={
        'console_scripts': [
            'cli = linkedin:cli',
        ],
    },
)

