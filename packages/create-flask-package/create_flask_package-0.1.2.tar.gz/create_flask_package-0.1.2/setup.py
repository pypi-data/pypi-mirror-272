from setuptools import setup, find_packages

setup(
    name='create_flask_package',
    version='0.1.2',
    author='Nasir iqbal',
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
)
