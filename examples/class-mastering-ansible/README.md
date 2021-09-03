# Class Mastering Ansible

## Environment Setup

```bash
# Provision Instances
vagrant up

# Generate inventory
vagranttoansible >> inventory.ini

# Testing inventory
ansible --list-hosts -i inventory.ini
```
