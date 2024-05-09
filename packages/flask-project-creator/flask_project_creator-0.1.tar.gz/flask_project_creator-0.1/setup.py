from setuptools import setup, find_packages

setup(
    name='flask_project_creator',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'create-flask-project=flask_project_creator.__init__:create_project',
        ],
    },
    install_requires=[
        'click',
    ],
)
