from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='create_flask_package',
    version='0.1.6',
    author='Nasir Iqbal',
    description="A CLI tool for generating Flask web application scaffolding.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dev-nasir-iqbal/create_flask_package",
    packages=find_packages(),
    install_requires=[
        'Flask',
        'Flask-SQLAlchemy',
        'Flask-CORS',
        'Flask-Login',
        'Flask-Session'
    ],
    entry_points={
        'console_scripts': [
            'create_flask_package = create_flask_package.create_flask_package:create_package_entry_point'
        ]
    },
    license="MIT",
)
