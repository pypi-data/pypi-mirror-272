import os
from pathlib import Path
import click
import subprocess
import json

def __generate_models_store_json():
  """
  This function generates json of models from GUI interface using tkinter
  """
  pass


# TODO: Add a command to create a new Django app within a project and register it in INSTALLED_APPS.
def __create_django_project(project_name):
    """Creates a new Django project with basic structure."""
    subprocess.run(['django-admin', 'startproject', project_name])
    click.echo(f"Project '{project_name}' created successfully!")

def __create_django_app(project_name:str, app_name:str=None):
    """Creates a new Django app within a project and registers it in INSTALLED_APPS."""

    try:
        # Change directory to the project (handle potential errors)
        original_dir = os.getcwd()
        os.chdir(project_name)
        project_dir = Path(os.getcwd())
        if not app_name:
          app_name = click.prompt("Enter the name of the app")
        # Create the app using manage.py (better error handling
        proccess =subprocess.run(['python', 'manage.py', 'startapp', app_name])
        if proccess.returncode != 0:
            click.secho(f"Error creating app: {app_name}", fg="red")
            return
        click.secho(f"App '{app_name}' created successfully!", fg="green", bold=True)
        click.secho("Registering the app in the installed apps list in settings...", fg="yellow", bold=True)
        # Register the app in the INSTALLED_APPS list (improved approach)
        settings_file = project_dir / project_name /'settings.py'
        if not settings_file.is_file():
            click.secho(f"Missing settings.py file in '{project_name}'. Skipping app registration.", fg="red", bold=True)
            return
        __add_app_to_settings(settings_file, app_name)
    except subprocess.CalledProcessError as e:
        click.secho(f"Error creating app: {e}", fg="red")
    except FileNotFoundError:
        click.secho(f"Project directory '{project_name}' not found. Please create it first.", fg="red")
    finally:
        # Change back to the original directory
        os.chdir(original_dir)


def __generate_models(project_name, app_name, models_json:str):
    """Interactively generates a model within an app."""
    models_type = {
       "int":"IntegerField()",
       "str": "CharField(max_length=255)",
       "bool": "BooleanField()",
       "pos_int": "PositiveIntegerField()",
       "email": "EmailField()",
       "url": "URLField()",
       "date": "DateField()",
       "datetime": "DateTimeField()",
       "time": "TimeField()",
       "decimal": "DecimalField(max_digits=10, decimal_places=2)",
    }

    script="""from django.db import models
    """
    try:
      with open(models_json, "r") as mj:
        models_data = json.load(mj)
      
      for model in models_data:
        script += f"""\nclass {model['model_name']}(models.Model):"""
        click.secho(f"Creating model {model['model_name']}...", fg="yellow", bold=True)
        for attr in model['model_attrs']:
          if attr["attr_type"] in models_type:
            script+=f"""\n    {attr['attr_name']}=models.{models_type[attr['attr_type']]}"""
        click.secho(f"Successfully created model {model['model_name']} and written {len(model['model_attrs'])} attributes", fg="green", bold=True)
      file_path = "{cwd}\\{project_name}\\{app_name}\\models.py".format(project_name=project_name,app_name=app_name, cwd=os.getcwd())
      with open (str(file_path), "w") as f:
        f.write(script)
    except Exception as e:
      click.secho(f"Error: {e}", fg="red", bold=True)
      return
    finally:click.secho(f"successfully edited the models.py..", fg="green")


def __add_app_to_settings(settings_file_path, app_name):
  """
  Adds an app to the INSTALLED_APPS list in a Python settings file.

  Args:
      settings_file_path (str): Path to the settings file.
      app_name (str): Name of the app to be added (enclosed in single quotes).

  Raises:
      FileNotFoundError: If the specified settings file is not found.
      ValueError: If the "INSTALLED_APPS" string cannot be located in the file.
  """

  settings_file = Path(settings_file_path)

  if not settings_file.is_file():
    raise FileNotFoundError(f"Settings file not found: {settings_file}")

  # Read the file contents
  with open(settings_file, "r") as f:
    settings_content = f.read()

  # Find the "INSTALLED_APPS" line (case-insensitive)
  installed_apps_line = None
  for line in settings_content.splitlines():
    if "INSTALLED_APPS" in line.upper():
      index = settings_content.index("INSTALLED_APPS")
      installed_apps_line = line.strip()
      break

  if not installed_apps_line:
    raise ValueError("Could not find 'INSTALLED_APPS' in the settings file.")

  # Extract the existing app list and add the new app
  try:
    # Assuming a typical format like `INSTALLED_APPS = [...]`
    start_index = installed_apps_line.index("[") + index + 1
    end_index = settings_content.find("]", index)
    existing_apps_str = settings_content[start_index:end_index]
    existing_apps = existing_apps_str.split()  
  except (IndexError, SyntaxError):
    raise ValueError("Invalid format for 'INSTALLED_APPS' in the settings file.")

  existing_apps.append(f"'{app_name}',")

  # Update the settings with the modified app list
  text = "\n    ".join(existing_apps)
  # Replace the existing app list with the updated one
  settings_content = settings_content.replace(existing_apps_str, '')
  updated_settings = settings_content.replace(installed_apps_line,f"{installed_apps_line.split('=')[0]} = [\n    {text}\n")

  # Write the updated settings back to the file (assuming write permissions)
  with open(settings_file, "w") as wf:
    wf.write(updated_settings)

  del settings_content
  del updated_settings  # Free up memory (not needed anymore) 
  click.secho(f"App {app_name} created and registered successfully.", fg="green", bold=True)

@click.group()
def cli():
    pass

@cli.command()
@click.argument('project_name')
def create_project(project_name):
  __create_django_project(project_name)


@cli.command()
@click.argument('project_name')
def create_app(project_name):
    __create_django_app(project_name)
    models_json = click.prompt("enter the path of the json file fo models data")
    __generate_models(project_name, "api", models_json)

@cli.command()
@click.argument('project_name')
@click.argument('app_name')
@click.argument('models_json')
def create_models(project_name, app_name, models_json:str):
  __generate_models(project_name, app_name, models_json)

def write_urls(project_name,app_name,api_views:list):
  """

  Write a urls class file (urls.py) for a Django REST API endpoint.

  Args:
    app_name: The name of the Django app where the API resides.
    api_views: The list of views from which the url of the API endpoint is generated.
  """
  urls_content_imports = f"""from django.urls import path
from .views import *"""
  api_urls = """
urlpatterns = [
  {paths}
]
"""
  urls_content = urls_content_imports
  paths = ""
  for view in api_views:
    view_name = view.strip()
    paths += f"path('api/{view_name.lower()}', {view_name}.as_view(), name='api_{view_name.lower()}'),\n"
  urls_content += api_urls.format(paths=paths)
  with open(f"{project_name}/{app_name}/urls.py", "w") as urls_file:
    urls_file.write(urls_content)
  del urls_content_imports
  del api_urls
  del urls_content
  del paths
  click.secho("urls.py written successfully", fg="green", bold=True)


def write_views(project_name,app_name, models_api_method:dict):
  """
  Writes a view class file (views.py) for a Django REST API endpoint.

  Args:
      app_name: The name of the Django app where the API resides.
      model: The Django model class associated with the API endpoint.
      models_api_method: This contains whether the model in models has an associated API method.

      models_api_method will looks like this:
        models_api_method = {
        "model_name": ["list", "create"]
        }
  """
  api_list = []
  views_content_imports = f"""from rest_framework.generics import CreateAPIView, ListAPIView\n
from .serializers import *\n"""

  apicreate = """
class Create{model}(CreateAPIView):
  serializer_class = {model}Serializer
"""
  apilist = """
class List{model}(ListAPIView):
  serializer_class = {model}Serializer
"""
  views_content = views_content_imports
  for model, api_methods in models_api_method.items():
    for api_method in api_methods:
       match api_method:
         case "list":
           views_content += apilist.format(model=model)
           api_list.append(f"List{model}")
         case "create":
           views_content += apicreate.format(model=model)
           api_list.append(f"Create{model}")

  with open(f"{project_name}/{app_name}/views.py", "w") as f:
    f.write(views_content)
  del views_content
  click.secho("views.py created successfully" , fg="green", bold=True)
  return api_list

def write_serializers(project_name, app_name, models:list[dict]):
  """
  Writes a serializer class file (serializers.py) for a Django REST API.

  Args:
      model: The Django model class for which a serializer is generated.
  """
  serializer_imports = f"""from rest_framework.serializers import ModelSerializer
from .models import *"""
  seraializers = """
class {model}Serializer(ModelSerializer):
  class Meta:
    model = {model}
    fields = '__all__'  # Expose all fields by default (consider customizing)
"""
  file_text = serializer_imports
  for model in models:
     file_text+=seraializers.format(model=model['name'])
  with open(f"{project_name}/{app_name}/serializers.py", "w") as f:
    f.write(file_text)
  del file_text, seraializers, serializer_imports
  click.secho("serializers.py written successfully", fg="green", bold=True)  


@cli.command()
@click.argument("project_name")
@click.argument("app_name")
@click.argument("models_json")
def create_project_app(project_name, app_name, models_json:str):
  """
  :param project_name:
  :param app_name:
  :param models_json:
  :return: None
  Create a project and an app in the project with the given name and models

  """
  __create_django_project(project_name)
  __create_django_app(project_name, app_name=app_name)
  __generate_models(project_name, app_name, models_json)
  # Extract model information from the JSON for API component generation
  with open(models_json, "r") as mj:
      models_data = json.load(mj)
      models = [{"name": model["model_name"], "fields": model["model_attrs"]} for model in models_data]
  
  # Write serializer classes for the models in the app's serializers.py
  write_serializers(project_name,app_name, models)

  # Write view classes for the API endpoints in the app's views.py
  models_api_method = {model["name"]: [] for model in models}  # Initialize empty dictionary
  # You can define API methods (list, create, etc.) here based on your requirements
  # For example, to include list and create methods for all models by default:
  for model in models:
    models_api_method[model["name"]] = ["list", "create"]
  api_list = write_views(project_name,app_name, models_api_method)

  # Write URL patterns for the API endpoints in the app's urls.py
  write_urls(project_name,app_name, api_list)

  click.secho(f"Project '{project_name}' with app '{app_name}' created successfully, including basic functionalities for a Django REST API.", fg="green", bold=True)


if __name__ == '__main__':
    cli()
