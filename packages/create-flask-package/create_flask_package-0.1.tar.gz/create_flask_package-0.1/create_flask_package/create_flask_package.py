import os

def create_package(package_name):
    # Create package directory
    package_dir = os.path.join(package_name)
    os.makedirs(package_dir)

    # Create subdirectories and files
    os.makedirs(os.path.join(package_dir, 'routes'))
    open(os.path.join(package_dir, '__init__.py'), 'a').close()
    open(os.path.join(package_dir, 'routes', '__init__.py'), 'a').close()
    open(os.path.join(package_dir, 'routes', 'routes.py'), 'a').close()
    open(os.path.join(package_dir, 'db_queries.py'), 'a').close()
    open(os.path.join(package_dir, 'models.py'), 'a').close()
    open(os.path.join(package_dir, 'utils.py'), 'a').close()
    
    # Create application.py at the same level as the package directory
    with open('application.py', 'w') as f:
        f.write(f'''from {package_name} import create_app

application = create_app()

if __name__ == "__main__":
    application.run(debug=True, host="0.0.0.0")
''')

    # Create setup.py
    with open('setup.py', 'w') as f:
        f.write(f'''from setuptools import setup, find_packages

setup(
    name='{package_name}',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'Flask',
        'Flask-SQLAlchemy'
    ],
)
''')

    # Create MANIFEST.in
    with open('MANIFEST.in', 'w') as f:
        f.write('recursive-include {} *.py'.format(package_name))

if __name__ == "__main__":
    package_name = input("Enter the name of your package: ")
    create_package(package_name)
