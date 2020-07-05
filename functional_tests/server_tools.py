from fabric.api import run
from fabric.context_managers import settings, shell_env
import os

SERVER_IP = os.environ["SERVER_IP"]
IDENTITY_FILE = os.environ["IDENTITY_FILE"]

def _get_manage_dot_py(host):
    return f'~/sites/{host}/virtualenv/bin/python ~/SITES/{host}/manage.py'


def reset_database(host):
    manage_dot_py = _get_manage_dot_py(host)
    with settings(host_string=f'trobe@{SERVER_IP}'):
        run(f'{manage_dot_py} flush --noinput -i {IDENTITY_FILE}')


def _get_server_env_vars(host):
    env_lines = run(f'cat ~/sites/{host}.env -i {IDENTITY_FILE}').splitlines()
    return dict(l.split('=') for l in env_lines if l)


def create_session_on_server(host, email):
    manage_dot_py = _get_manage_dot_py(host)
    with settings(host_string=f'trobe@{SERVER_IP}'):
        env_vars = _get_server_env_vars(host)
        with shell_env(**env_vars):
            session_key = run(f'{manage_dot_py} create_session {email} -i {IDENTITY_FILE}')
            return session_key.strip()