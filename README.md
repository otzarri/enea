# enea

Personal cloud.

## Installation

Python dependencies:

```
$ python -m pip install pyyaml
```

Ansible dependencies:

```
$ ansible-galaxy install -r requirements.yml
```

## App deployment

Deploy an application:

```
$ ansible-playbook -i inventory/hosts.ini app-deploy.yaml --extra-vars "app_name=iml-fe web=open"
```
