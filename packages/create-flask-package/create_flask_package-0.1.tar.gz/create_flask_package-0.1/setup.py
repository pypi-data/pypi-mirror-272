from setuptools import setup, find_packages

setup(
    name='create_flask_package',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'Flask',
        'Flask-SQLAlchemy',
    ],
)
