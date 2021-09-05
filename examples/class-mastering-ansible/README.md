# Class Mastering Ansible

## Documentation

- [Flask Mod WSGI](https://flask.palletsprojects.com/en/2.0.x/deploying/mod_wsgi/)

## Environment Setup

```bash
# Provision Instances
vagrant up

# Generate inventory
vagranttoansible >> inventory.ini

# Testing inventory
ansible --list-hosts -i inventory.ini
```
