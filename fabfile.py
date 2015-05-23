from fabric.api import *
import os

env.hosts=["api.kraang.io"]
env.user=os.environ['KRAANG_SERVER_USER']
env.password=os.environ['KRAANG_SERVER_PW']

def deploy():
    run("service nginx stop")
    if run("file '/tmp/master.pid'", warn_only=True).succeeded:
        if run("uwsgi --stop /tmp/master.pid", warn_only=True).succeeded:
            run("echo 'stopped with pid...'")

    with cd("/var/www/kraang.io"):
        with cd("src"):
            run("rm -rf kraang_api")
            run("git clone https://github.com/keymholio/kraang_api.git")
            run(". ../venv/bin/activate")
            run("pip install -r kraang_api/requirements.txt")
            with cd("kraang_api"):
                run("python manage.py collectstatic --noinput")

    run("service nginx start")
    run("uwsgi /var/www/kraang.io/conf/uwsgi.ini --pidfile=/tmp/master.pid")
