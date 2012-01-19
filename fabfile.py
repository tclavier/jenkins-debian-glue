################################################################################
# Deploy Debian package to jenkins build system(s)
#
# Usage examples:
# % fab all
# % fab build && fab deploy
# % fab -H root@jenkins.example.org deploy
################################################################################

from fabric.api import *
import os, paramiko, sys

def set_hosts():
    if not env.hosts:
        env.hosts = []

        for host in 'jenkins', 'jenkins-slave1', 'jenkins-slave2':
            config = paramiko.SSHConfig()
            config.parse(open(os.path.expandvars("$HOME") + '/.ssh/config'))
            h = config.lookup(host)
            env.hosts.append(h['user'] + "@" + h['hostname'])

    return env.hosts

@runs_once
def build():
    local('rm -f ../jenkins-debian-glue_*all.deb')
    local('fakeroot debian/rules clean')
    local('fakeroot debian/rules binary')

@hosts(set_hosts())
def deploy():
    put('../jenkins-debian-glue_*all.deb', '~/')
    run('dpkg -i ~/jenkins-debian-glue_*all.deb')

def all():
    build()
    deploy()

## END OF FILE #################################################################
