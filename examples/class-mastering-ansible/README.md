# Class Mastering Ansible

## Documentation

- [Flask Mod WSGI](https://flask.palletsprojects.com/en/2.0.x/deploying/mod_wsgi/)

## Environment Setup

### Vagrant

```bash
# Provision Instances
vagrant up

# Generate inventory
vagranttoansible >> inventory.ini

# Testing inventory
ansible --list-hosts -i inventory.ini
```

### Docker

This setup requires testing.

```bash
# Create ssh keypair
ssh-keygen -t rsa -f ansible

# Copy keypair to env folder

# Build and run containers
docker-compose build && docker-compose up
```