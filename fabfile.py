# -*-coding: UTF-8 -*-
# Run these commands with fab

from datetime import date, datetime
from fabric.api import local, settings, abort, run, cd, env, sudo, prefix
from fabric.contrib.console import confirm
from fabric.contrib.files import exists

env.site_name = 'spreadsite'
env.hosts = ['{0}@spreadsite.org'.format(env.site_name)]
env.virtualenv = env.site_name
env.settings_subdir = env.site_name
env.django_apps = ['spreadlinks', 'downblog']

def update_requirements():
    local("pip freeze | egrep -v 'Fabric|pycrypto|ssh' > REQUIREMENTS")

def test():
    with settings(warn_only=True):
        result = local('./manage.py test {0}'.format(' '.join(env.django_apps)), capture=True)
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at user request.")

def push():
    local('git push')

def deploy():
    test()
    push()

    run('if [ ! -d static ]; then mkdir static; fi')
    #run('mkdir -p caches/httplib2')
    run('mkdir -p caches/django')

    code_dir = '/home/{0}/Sites/{0}'.format(env.site_name)
    with cd(code_dir):
        run('git pull')
        run('cp -p {0}/settings_production.py {0}/settings.py'.format(env.settings_subdir))

        with prefix('. /home/{0}/virtualenvs/{1}/bin/activate'.format(env.site_name, env.virtualenv)):
            run('pip install -r REQUIREMENTS')
            run('./manage.py collectstatic --noinput')

    run('touch /etc/uwsgi/emperor.d/{0}.ini'.format(env.site_name))

def make_virtualenv():
    env_name = 'virtualenvs/{0}'.format(env.site_name)
    if exists(env_name):
        bak_name = 'virtualenvs/before-{0}.{1}'.format(date.today().isoformat(), env.site_name)
        if not exists(bak_name):
            run('mv {0} {1}'.format(env_name, bak_name))
    run('virtualenv {0}'.format(env_name))
