#!/usr/bin/env python3
# NOTE: this file must be executable `chmod +x centos.py`
	# challenge: make this file not executable and see what `ansible-inventory --list` prints
# TEST this with a json formatter like `jq`:
    # `./inventory_dir/centos.py | jq `
# Great docs on how to build an inventory script
# albeit an inventory plugin is preferrable
# https://docs.ansible.com/ansible/latest/dev_guide/developing_inventory.html
    # specifically about inventory scripts: https://docs.ansible.com/ansible/latest/dev_guide/developing_inventory.html#developing-inventory-scripts
# https://docs.ansible.com/ansible/latest/user_guide/intro_dynamic_inventory.html
import json
import os
# must print a json dictionary, otherwise you'll get an error:
#   " needs to be a json dict"
inventory = {
    # more about meta here https://docs.ansible.com/ansible/latest/dev_guide/developing_inventory.html#id16
    "_meta": {
        "hostvars": {}
    },
    "rhel": {"hosts": []}
}

provider = (os.environ['VAGRANT_DEFAULT_PROVIDER'])
# programatically add hosts to inventory to show scripting benefits
# challenge: increase range & Vagrantfile VMs to see how we can dynamically add more targets
# challenge: port ubuntu static inventory to script too
# challenge: port centos.py script (this file) back into static inventory 
for i in range(2):
    host = f"rhel3{i}"
    inventory["_meta"]["hostvars"][host] = {
        "ansible_host": f"192.168.50.3{i}",
        "ansible_private_key_file": f".vagrant/machines/{host}/{provider}/private_key"
    }
    inventory["rhel"]["hosts"].append(host)

# python json API https://docs.python.org/3/library/json.html
# script returns inventory formatted as json to ansible
print(json.dumps(inventory))