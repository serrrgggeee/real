from fabric.api import *

# import deploy.fabric.setup as setup

from fabric.utils import _AttributeDict

import os

env.project = _AttributeDict({
    'name': 'name',
    'username': 'name',  # group assumed to be the same
    'reqs': 'requirements.txt',
    'src_dir': 'source_tmp',  # rel from home
    'src_web': 'host',  # rel from home
    'src_branch': 'master',
    'pip_cache': '.pip-cache',  # rel path from home
    'venv': '.venv',

    'persistent_dirs': [
        {'media': [
            'cache',
            'ckeditor',
        ]},
    ],

    'links': [
        ('media', 'media')
    ]
})

env.project.home = os.path.join('/home', env.project.username)
env.project.pip = os.path.join(env.project.home, env.project.venv,
                               'bin', 'pip')
env.project.python = os.path.join(env.project.home, env.project.venv,
                                  'bin', 'python')


def co_branch():
    local('git checkout {branch}'.format(branch=env.project.src_branch))


def push():
    local('git push origin {branch}'.format(branch=env.project.src_branch))


@task
def prod():
    env.type = 'prod'
    env.hosts = [
        'host'
    ]
    co_branch()
    push()





@task
def full_deploy():
    setup.full()


@task
def complete_deploy():
    print env
    # setup.complete()


try:
    from fabfile_local import *
except ImportError:
    pass

try:
    from fabfile_local import modify
    modify(globals())
except ImportError:
    pass
