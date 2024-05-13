from . import app
from .gitea import app as gitea_app
from .k8s import app as k8s_app

app.add_typer(gitea_app, name='gitea')
app.add_typer(k8s_app, name='k8s')


def main():
    app()
