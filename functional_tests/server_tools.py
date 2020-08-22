from fabric.api import run
from fabric.context_managers import settings, shell_env
import os

STAGING_SERVER_IP = os.environ.get("STAGING_SERVER_IP")
IDENTITY_FILE = os.environ.get("IDENTITY_FILE")


def _get_manage_dot_py(site):
    return f"~/sites/{site}/virtualenv/bin/python ~/sites/{site}/manage.py"


def reset_database(site):
    manage_dot_py = _get_manage_dot_py(site)
    with settings(host_string=f"trobe@{STAGING_SERVER_IP}", key_filename=IDENTITY_FILE):
        run(f"{manage_dot_py} flush --noinput")


def _get_server_env_vars(site):
    env_lines = run(f"cat ~/sites/{site}/.env").splitlines()
    return dict(l.split("=") for l in env_lines if l)


def create_session_on_server(site, email):
    manage_dot_py = _get_manage_dot_py(site)
    with settings(host_string=f"trobe@{STAGING_SERVER_IP}", key_filename=IDENTITY_FILE):
        env_vars = _get_server_env_vars(site)
        with shell_env(**env_vars):
            session_key = run(f"{manage_dot_py} create_session {email}")
            return session_key.strip()
