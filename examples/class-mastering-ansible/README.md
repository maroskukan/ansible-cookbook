# Class Mastering Ansible

- [Class Mastering Ansible](#class-mastering-ansible)
  - [Documentation](#documentation)
  - [Environment Setup](#environment-setup)
    - [Vagrant](#vagrant)
    - [Docker](#docker)
  - [Application Setup](#application-setup)
    - [Install](#install)
    - [Validate](#validate)
  - [Clean up](#clean-up)


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
ansible-inventory --list -i inventory.ini all

# Create Vault Password file
echo 'demo' > ~/.vault_pass.txt
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

## Application Setup


### Install

```bash
ansible-playbook site.yml
```

### Validate

```bash
ansible-playbook validate.yml
```

## Clean up

```bash
vagrant destroy --force
```