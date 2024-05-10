from setuptools import setup, find_packages

# short and long descriptions
SHORT_DESCRIPTION = "Flask Project Creator: A CLI tool for quickly setting up Flask web applications."
LONG_DESCRIPTION = """
Flask Project Creator is a command-line interface (CLI) tool designed to expedite the creation of Flask web applications. With just a single command, this tool automates the generation of a Flask project directory structure, including essential files and folders such as `run.py`, `__init__.py`, `templates`, and `static`. Additionally, it provides basic templates (`base.html` and `home.html`) along with example route definitions to jumpstart your development process.

This tool leverages Click, a Python package for creating command-line interfaces, to offer a user-friendly experience with customizable options. Whether you're starting a new web project, prototyping ideas, or simply looking to streamline your Flask development workflow, Flask Project Creator simplifies the initial setup process, allowing you to focus on building your application logic without the hassle of manual configuration.

Key Features:
- Automated generation of Flask project directory structure.
- Includes basic templates and example route definitions.
- Customizable options via Click command-line interface.
- Simplifies Flask development workflow, saving time and effort.

CLI Command:
- Command Name: create-flask-project
"""

setup(
    name='flask_project_creator',
    version='0.1.2',
    author='Omkar Subhash Parab',
    author_email='omkar211196@gmail.com',
    description=SHORT_DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'create-flask-project=flask_project_creator.__init__:create_project',
        ],
    },
    install_requires=[
        'click',
        'flask',
    ],
)
