import random
import os
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run

REPO_URL = "https://github.com/robertsont/tdd_project.git"


def deploy(server_type):
    site_folder = f"/home/{env.user}/sites/{server_type}"
    run(f"mkdir -p {site_folder}")
    with cd(site_folder):
        _get_latest_source()
        _update_virtualenv()
        _create_or_update_dotenv(server_type)
        _update_static_files()
        _update_database()


def _get_latest_source():
    if exists(".git"):
        run("git fetch")
    else:
        run(f"git clone {REPO_URL} .")
    if os.getenv("CURRENT_COMMIT") == "TRUE":
        current_commit = local("git log -n 1 --format=%H", capture=True)
        run(f"git reset --hard {current_commit}")


def _update_virtualenv():
    if not exists("virtualenv/bin/pip"):
        run(f"python3.6 -m venv virtualenv")
    run("./virtualenv/bin/pip install -r requirements.txt")


def _create_or_update_dotenv(server_type):
    append(".env", "DJANGO_DEBUG_FALSE=true")
    append(".env", f"SITENAME={server_type}")
    current_contents = run("cat .env")
    if "DJANGO_SECRET_KEY" not in current_contents:
        new_secret = "".join(
            random.SystemRandom().choices("abcdefghijklmnopqrstuvwxyz0123456789", k=50)
        )
        append(".env", f"DJANGO_SECRET_KEY={new_secret}")
    email_password = os.environ["EMAIL_PASSWORD"]
    append(".env", f"EMAIL_PASSWORD={email_password}")


def _update_static_files():
    run("./virtualenv/bin/python manage.py collectstatic --noinput")


def _update_database():
    run("./virtualenv/bin/python manage.py migrate --noinput")
