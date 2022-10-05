# Ansible

This directory contains the resources related to Ansible.

Install the dependencies before running the playbooks:

```
$ ansible-galaxy install -r requirements.yml
```

Firewall redirections for 80 and 443:

```
apt install -y firewalld
sudo firewall-cmd --add-forward-port=port=80:proto=tcp:toport=8080
sudo firewall-cmd --add-forward-port=port=443:proto=tcp:toport=8443
```
