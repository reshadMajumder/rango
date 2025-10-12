#!/usr/bin/env python3
"""
Rango Framework CLI
-----------------------------------
Usage:
    python manage.py startproject myproject
    python manage.py startapp blog
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
"""
import typer
import os
import subprocess
from pathlib import Path

cli = typer.Typer(help="Rango Framework management CLI")
PROJECT_ROOT = Path(__file__).resolve().parent

# ----------------------------
# STARTPROJECT
# ----------------------------
@cli.command()
def startproject(name: str):
    project_dir = PROJECT_ROOT / name
    if project_dir.exists():
        typer.echo(f"❌ Project '{name}' exists")
        raise typer.Exit(code=1)
    os.makedirs(project_dir / "apps", exist_ok=True)
    os.makedirs(project_dir / "project", exist_ok=True)
    # settings.py
    (project_dir / "project" / "settings.py").write_text(
        "INSTALLED_APPS = []\nDATABASE_URL='sqlite://db.sqlite3'\nTORTOISE_ORM={\n"
        "    'connections':{'default': DATABASE_URL},\n"
        "    'apps':{'models':{'models':['aerich.models'], 'default_connection':'default'}}\n}\n"
    )
    # urls.py
    (project_dir / "project" / "urls.py").write_text(
        "from rango.router import Router\nrouter = Router()\n"
    )
    # asgi.py
    (project_dir / "project" / "asgi.py").write_text(
        "from rango.core import RangoApp\nfrom rango.middleware import SimpleCORSMiddleware\n"
        "from project.urls import router\napp = RangoApp(debug=True)\napp.add_middleware(SimpleCORSMiddleware)\napp.include_router(router)\n"
    )
    # main.py
    (project_dir / "main.py").write_text(
        "from project.asgi import app\nif __name__=='__main__':\n import uvicorn\n uvicorn.run(app, host='127.0.0.1', port=8000, reload=True)\n"
    )
    typer.echo(f"✅ Project '{name}' created!")

# ----------------------------
# STARTAPP
# ----------------------------
@cli.command()
def startapp(name: str):
    project_path = Path.cwd()
    apps_dir = project_path / "apps"
    app_dir = apps_dir / name
    if not (project_path / "project" / "settings.py").exists():
        typer.echo("❌ Not in a Rango project")
        raise typer.Exit(code=1)
    os.makedirs(app_dir, exist_ok=True)
    (app_dir / "__init__.py").write_text("")
    (app_dir / "models.py").write_text(
        "from tortoise import fields, models\nclass Example(models.Model):\n id=fields.IntField(pk=True)\n title=fields.CharField(max_length=255)\n created_at=fields.DatetimeField(auto_now_add=True)\n"
    )
    (app_dir / "serializers.py").write_text(
        "from rango.serializers import ModelSerializer\nfrom .models import Example\nclass ExampleSerializer(ModelSerializer):\n class Meta:\n  model=Example\n  fields=['id','title','created_at']\n"
    )
    (app_dir / "views.py").write_text(
        "from rango.generics import ListCreateView, RetrieveUpdateDeleteView\nfrom .models import Example\nfrom .serializers import ExampleSerializer\nclass ExampleListCreateView(ListCreateView):\n model=Example\n serializer_class=ExampleSerializer\nclass ExampleDetailView(RetrieveUpdateDeleteView):\n model=Example\n serializer_class=ExampleSerializer\n"
    )
    (app_dir / "urls.py").write_text(
        "from rango.router import Router\nfrom .views import ExampleListCreateView, ExampleDetailView\nrouter=Router()\nrouter.add('/example',ExampleListCreateView,methods=['GET','POST'])\nrouter.add('/example/{id}',ExampleDetailView,methods=['GET','PUT','DELETE'])\n"
    )
    typer.echo(f"✅ App '{name}' created!")

# ----------------------------
# DB COMMANDS
# ----------------------------
@cli.command()
def makemigrations(message: str = "auto"):
    typer.echo("📦 Making migrations...")
    subprocess.run(["aerich", "migrate", "--name", message], check=False)

@cli.command()
def migrate():
    typer.echo("⚙️ Applying migrations...")
    subprocess.run(["aerich", "upgrade"], check=False)

# ----------------------------
# RUN SERVER
# ----------------------------
@cli.command()
def runserver(host: str = "127.0.0.1", port: int = 8000):
    typer.echo(f"🚀 Running server at http://{host}:{port}")
    subprocess.run(["uvicorn", "project.asgi:app", "--host", host, "--port", str(port), "--reload"])

if __name__ == "__main__":
    cli()
