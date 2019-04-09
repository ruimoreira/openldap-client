import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_nsswitch(host):
    nsswitchfile = host.file('/etc/nsswitch.conf')
    assert nsswitchfile.contains("passwd:     files sss")
    assert nsswitchfile.contains("shadow:     files sss")
    assert nsswitchfile.contains("group:      files sss")


def test_packages(host):
    package_list = ["sssd", "libnss-sss", "libpam-sss"]
    for package in package_list:
        assert host.package(package).is_installed
