import click
import os
import shutil
import secrets


@click.command()
def create_project():
    """-
    We are creating a new Flask project structure.
    """
    project_name = click.prompt("Enter project name", type=str)
    apps_folder = click.prompt(
        "Enter name for 'apps' folder", default='FlaskApp', type=str)

    try:
        os.mkdir(project_name)
        os.chdir(project_name)
        os.mkdir(apps_folder)
        os.mkdir(os.path.join(apps_folder, 'templates'))
        os.mkdir(os.path.join(apps_folder, 'static'))
        
        # Create base.html template
        with open(os.path.join(apps_folder, 'templates', 'base.html'), 'w') as f:
            f.write(
                "<html>\n<head>\n    <title>{{ title }}</title>\n</head>\n<body>\n{% block content %}{% endblock content %}\n</body>\n</html>")

        # Create home.html template
        with open(os.path.join(apps_folder, 'templates', 'home.html'), 'w') as f:
            f.write(
                "{% extends 'base.html' %}\n\n{% block content %}\n <center><h1>Welcome to my Flask App!</h1></center>\n <center><p>This is the home page. </p></center>\n{% endblock content %}")

        with open('run.py', 'w') as f:
            f.write(f"from {apps_folder} import app\n\n")
            f.write("if __name__ == '__main__':\n")
            f.write("    app.run(debug=True)\n")

        with open('requirements.txt', 'w') as f:
            pass  # You can add required packages to this file
        
        with open('readme.md', 'w') as f:
            pass  # You can add required packages to this file
        
        with open('.env', 'w') as f:
            pass  # You can add required packages to this file

        with open(f'{apps_folder}/__init__.py', 'w') as f:
            f.write(f"from flask import Flask\n\n")
            f.write("app = Flask(__name__)\n\n")
            f.write(f"app.config['SECRET_KEY'] = '{secrets.token_hex(16)}'\n\n")
            f.write(f"from .models import *\n")
            f.write(f"from .forms import *\n")
            f.write(f"from {apps_folder} import routes, auth_routes\n")
            

        with open(f'{apps_folder}/models.py', 'w') as f:
            pass  # You might want to add some content here
        
        with open(f'{apps_folder}/forms.py', 'w') as f:
            pass  # You might want to add some content here

        with open(f'{apps_folder}/routes.py', 'w') as f:
            f.write(f"from {apps_folder} import app\n")
            f.write("from flask import render_template\n\n\n\n")
            f.write("@app.route('/', methods=['GET'])\n")
            f.write("def home():\n")
            f.write("    return render_template('home.html', title='Home')\n")
            
        with open(f'{apps_folder}/auth_routes.py', 'w') as f:
            pass  # You might want to add some content here

        click.echo(f"Created Flask project structure for '{project_name}'.")

    except FileExistsError:
        click.echo(f"Error: '{project_name}' already exists.")


if __name__ == '__main__':
    create_project()
