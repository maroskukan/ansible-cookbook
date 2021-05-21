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

```bash
# Targeting a specific host from a group
ansible db_servers --limit db01 -m ping
db01 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/libexec/platform-python"
    },
    "changed": false,
    "ping": "pong"
}
```

### Configuration

```bash
# Display all configuration
ansible-config dump

# Display only overrides
ansible-cofnig dump --only-changed
DEFAULT_HOST_LIST(/mnt/c/Users/maros/vagrant/ansible-cookbook/exercise/ansible.cfg) = ['/mnt/c/Users/maros/vagrant/ansible-cookbo
ok/exercise/inventory']
```

*Tip: Ansible can access the hosts fine using names and key based authentication, but your system may not without prior configuration. To overcome this you can dump the ssh config from vagrant into `~/.ssh` folder and include in your main cofiguration file.*


```bash
cd provision && vagrant ssh-config > ~/.ssh/vagrants/ansible-exercise.config

# Verify the file location
/home/maros/.ssh/vagrants
├── ansible-exercise.config

# Verify main ssh config
grep include ~/.ssh/config
# Include Vagrant generated files
Include vagrants/*
```

Now `ssh web01` will work automatically from your main machine.

### Modules

```bash
# List all modules
ansible-doc -l

# Describe a module
ansible-doc ping
ansible-doc service
```

#### System Modules

```bash
ansible all --limit web01 -m service -a "state=restarted name=sshd"
```
#### 
```bash
ansible web_servers -b -m user -a "name=test password=secure_password state=present"
[WARNING]: The input password appears not to have been hashed. The 'password' argument must be encrypted for this module to work
properly.
web02 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/libexec/platform-python"
    },
    "changed": true,
    "comment": "",
    "create_home": true,
    "group": 1001,
    "home": "/home/test",
    "name": "test",
    "password": "NOT_LOGGING_PASSWORD",
    "shell": "/bin/bash",
    "state": "present",
    "system": false,
    "uid": 1001
}
web01 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/libexec/platform-python"
    },
    "changed": true,
    "comment": "",
    "create_home": true,
    "group": 1001,
    "home": "/home/test",
    "name": "test",
    "password": "NOT_LOGGING_PASSWORD",
    "shell": "/bin/bash",
    "state": "present",
    "system": false,
    "uid": 1001
}
```

#### Command Modules

- Modules that run commands directly on the managed host
- You can use these if no other module is available to do what you need
- They are not idempotent therefore you must make sure that they are safe to run twice
- **shell** - runs a command on the rmeote systems's shell, redirection works
- **command** - runs a sinle command on the remote system
- **raw** - runs a command with no processing, does not require Python to be installed on managed host (e.g. older network equipment)

There are other modules available - expect, psexec, script, telnet.

```bash
ansible web_servers -m shell -a "uname -a"
web01 | CHANGED | rc=0 >>
Linux web01 4.18.0-240.22.1.el8_3.x86_64 #1 SMP Thu Apr 8 19:01:30 UTC 2021 x86_64 x86_64 x86_64 GNU/Linux
web02 | CHANGED | rc=0 >>
Linux web02 4.18.0-240.22.1.el8_3.x86_64 #1 SMP Thu Apr 8 19:01:30 UTC 2021 x86_64 x86_64 x86_64 GNU/Linux
```

```bash
ansible web_servers -m command -a "id"
web01 | CHANGED | rc=0 >>
uid=1000(vagrant) gid=1000(vagrant) groups=1000(vagrant) context=unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023
web02 | CHANGED | rc=0 >>
uid=1000(vagrant) gid=1000(vagrant) groups=1000(vagrant) context=unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023
```

#### Generic Modules

```bash
ansible web_servers -b -m package -a "name=httpd state=present"
web02 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/libexec/platform-python"
    },
    "changed": true,
    "msg": "",
    "rc": 0,
    "results": [
        "Installed: apr-1.6.3-11.el8.x86_64",
        "Installed: apr-util-1.6.1-6.el8.x86_64",
        "Installed: mod_http2-1.15.7-2.module_el8.3.0+477+498bb568.x86_64",
        "Installed: apr-util-bdb-1.6.1-6.el8.x86_64",
        "Installed: mailcap-2.1.48-3.el8.noarch",
        "Installed: apr-util-openssl-1.6.1-6.el8.x86_64",
        "Installed: httpd-2.4.37-30.module_el8.3.0+561+97fdbbcc.x86_64",
        "Installed: httpd-filesystem-2.4.37-30.module_el8.3.0+561+97fdbbcc.noarch",
        "Installed: centos-logos-httpd-80.5-2.el8.noarch",
        "Installed: httpd-tools-2.4.37-30.module_el8.3.0+561+97fdbbcc.x86_64"
    ]
}
web01 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/libexec/platform-python"
    },
    "changed": true,
    "msg": "",
    "rc": 0,
    "results": [
        "Installed: apr-1.6.3-11.el8.x86_64",
        "Installed: apr-util-1.6.1-6.el8.x86_64",
        "Installed: mod_http2-1.15.7-2.module_el8.3.0+477+498bb568.x86_64",
        "Installed: apr-util-bdb-1.6.1-6.el8.x86_64",
        "Installed: mailcap-2.1.48-3.el8.noarch",
        "Installed: apr-util-openssl-1.6.1-6.el8.x86_64",
        "Installed: httpd-2.4.37-30.module_el8.3.0+561+97fdbbcc.x86_64",
        "Installed: httpd-filesystem-2.4.37-30.module_el8.3.0+561+97fdbbcc.noarch",
        "Installed: centos-logos-httpd-80.5-2.el8.noarch",
        "Installed: httpd-tools-2.4.37-30.module_el8.3.0+561+97fdbbcc.x86_64"
    ]
}
```