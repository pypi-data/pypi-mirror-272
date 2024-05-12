import typer
from .base.django import generate_command

app = typer.Typer(add_completion=False)

generate_command(app, 'djcreator-project-backend')
