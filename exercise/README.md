# Exercise

## Environment

```bash
# Provision Virtual machines
vagrant up

# Generate inventory
vagranttoansible > ../inventory/hosts

# Create base ansible configuration
cat <<EOF >>../ansible.cfg
[defaults]
inventory = ./inventory
EOF
```

```bash
# Validate inventory from main exercise folder
ansible-inventory --list

# Validate reachability
ansible -m ping all
```

### Inventory

```bash
# Verify config location setitng
ansible --version | grep "config file"
config file = /mnt/c/Users/maros/vagrant/ansible-cookbook/exercise/ansible.cfg

# Verify config content
cat ansible.cfg
[defaults]
inventory = ./inventory
```

```bash
# Display content of inventory folder
tree .inventory
./inventory
├── groups
└── hosts
```

```json
// Verify inventory - JSON output
ansible-inventory --list
{
    "_meta": {
        "hostvars": {
            "db1": {
                "ansible_ssh_common_args": "-o StrictHostKeyChecking=no",
// ..output omitted...
```

```yml
# Verify inventory - YAML output
ansible-inventory -y --list
all:
  children:
    db_servers:
      hosts:
        db1:
          ansible_ssh_common_args: -o StrictHostKeyChecking=no
# ..output omitted...
```

```bash
# Verify if host exists in inventory
ansible web2 --list-hosts
  hosts (1):
    web2
#
ansible web3 --list-hosts
[WARNING]: Could not match supplied host pattern, ignoring: web3
[WARNING]: No hosts matched, nothing to do
  hosts (0):
```