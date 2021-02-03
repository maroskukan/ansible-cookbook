# Ansible

## Installation

Installation depends on control node configuration. For example on Ubuntu the preferred way to install Ansible is to use the system package manager. Wherease on Mac OS X the preferred method is to install via pip.

## Documentation

### Web
- [Ansible Project](https://docs.ansible.com)
- [Modules Intro](https://docs.ansible.com/ansible/latest/user_guide/modules_intro.html)


### Cli 

```bash
# List the plugins for particular type (shell)
ansible-doc -t shell --list

# Retrieve more information about plugin gor given type
ansible-doc -t shell powershell
```

```bash
# Without specifying type, default `module` type is assumed
ansible-doc git 
```


## Ad Hoc Configuration

The following example demostrates the use of **copy** module.

```
ansible -m copy -a "src=master.gitconfig dest=~/.gitconfig" localhost
```

Dry run.
```
ansible -m copy -a "src=master.gitconfig dest=~/.gitconfig" --check localhost
```

Dry run with diff flag.
```
ansible -m copy -a "src=master.gitconfig dest=~/.gitconfig" --check --diff localhost
```

The following example demostrates the use of **homebrew** module.

```
ansible -m homebrew -a "name=bat state=latest" localhost
ansible -m homebrew -a "name=jq state=latest" localhost
```

## Playbook

Simple playbook.yml syntax examples.

```yml
---
- hosts: localhost
  tasks:
    - copy: src="master.gitconfig" dest="~/.gitconfig"
```

```yml
---
- hosts: localhost
  tasks:
    - copy: 
        src: "master.gitconfig"
        dest: "~/.gitconfig"
```

## Inventory

Inventory files describe a collection of hosts or systems you want to manage using ansible commands. Hosts can be assigned to groups and groups can contain child groups. Hosts can be members of multiple groups. Variables can be set that apply to hosts and groups. For example connection parameters, such as SSH username or port.

There are many different types of inventory files, to see full list use the following `ansible-doc` command.
```bash
ansible-doc -t inventory --list
```

It is common to define the inventory file within `ansible.cfg` configuration file under `[defaults]` sections. For example.
```ini
[defaults]
inventory = ./inventory
```

To verify if the inventory was correctly formatted and understood by ansible you can use `ansible-inventory` command with options such as `list` or `graph`
```json
ansible-inventory --list
{
    "_meta": {
        "hostvars": {
            "192.168.137.106": {
                "ansible_port": 22,
                "ansible_user": "vagrant"
            },
            "192.168.137.137": {
                "ansible_port": 22,
                "ansible_user": "vagrant"
            },
            "192.168.137.162": {
                "ansible_port": 22,
                "ansible_user": "vagrant"
            },
            "192.168.137.245": {
                "ansible_port": 22,
                "ansible_user": "vagrant"
            }
        }
    },
    "all": {
        "children": [
            "ungrouped",
            "vagrant"
        ]
    },
    "centos": {
        "hosts": [
            "192.168.137.106",
            "192.168.137.162"
        ]
    },
    "ubuntu": {
        "hosts": [
            "192.168.137.137",
            "192.168.137.245"
        ]
    },
    "vagrant": {
        "children": [
            "centos",
            "ubuntu"
        ]
    }
}
```
```bash
ansible-inventory --graph [--vars]
@all:
  |--@ungrouped:
  |--@vagrant:
  |  |--@centos:
  |  |  |--192.168.137.106
  |  |  |--192.168.137.162
  |  |--@ubuntu:
  |  |  |--192.168.137.137
  |  |  |--192.168.137.245
```

## Connection Parameters

To display available `connection' module plugins use the following command:
```bash
ansible-doc -t connection --list
```

### Testing Connection

In order to conduct a simple reachability test for hosts defined in inventory you can use Ansible ad-hoc command with `ping` module. Below I am running this module agains `vagrant` host group.

```json
ansible ubuntu -m ping
192.168.137.137 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
192.168.137.245 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
```

Another way is to leverage `command` module and execute a command on manage host. In this case below, git is not installed on hosts that are part of centos group.

```json
ansible -m command -a "git config --global --list" centos
192.168.137.106 | FAILED | rc=2 >>
[Errno 2] No such file or directory: b'git': b'git'
192.168.137.162 | FAILED | rc=2 >>
[Errno 2] No such file or directory: b'git': b'git'
```

## Running Playbook

```ini
ansible-playbook playbooks/playbook.yml
PLAY [Ensure git installed] *****************************************************************************************************************************

TASK [Gathering Facts] **********************************************************************************************************************************
ok: [192.168.137.106]
ok: [192.168.137.162]

TASK [package] ******************************************************************************************************************************************
ok: [192.168.137.162]
ok: [192.168.137.106]

PLAY [Ensure ~/.gitconfig copied from master.gitconfig] *************************************************************************************************

TASK [Gathering Facts] **********************************************************************************************************************************
ok: [192.168.137.106]
ok: [192.168.137.162]
ok: [192.168.137.137]
ok: [192.168.137.245]

TASK [first show no config in targets] ******************************************************************************************************************
fatal: [192.168.137.137]: FAILED! => {"changed": true, "cmd": ["git", "config", "--global", "--list"], "delta": "0:00:00.002296", "end": "2021-02-02 14:57:03.018818", "msg": "non-zero return code", "rc": 128, "start": "2021-02-02 14:57:03.016522", "stderr": "fatal: unable to read config file '/home/vagrant/.gitconfig': No such file or directory", "stderr_lines": ["fatal: unable to read config file '/home/vagrant/.gitconfig': No such file or directory"], "stdout": "", "stdout_lines": []}
[Output omitted]
```
## Ansible Galaxy

```bash
ansible-galaxy collection install -r requirements.yml
```


## Ansible Console

From documentation, `ansible-console` is a REPL that allows for running ad-hoc tasks against a chosen inventory (based on dominis’ ansible-shell).

```bash
ansible-console [intentory] --module-path=~/.ansible/plugins/modules:/usr/share/ansible/plugins/modules:~/.ansible/collections/ansible_collections/community/general/plugins/modules
ansible_container_test2 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
ansible_container_test3 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
ansible_container_test1 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
maros@containers (3)[f:5]$ git_config list_all=yes scope=global
ansible_container_test3 | SUCCESS => {
    "changed": false,
    "config_values": {
        "user.email": "maros.kukan@gmail.com",
        "user.name": "Maros"
    },
    "msg": ""
}
ansible_container_test1 | SUCCESS => {
    "changed": false,
    "config_values": {
        "user.email": "maros.kukan@gmail.com",
        "user.name": "Maros"
    },
    "msg": ""
}
ansible_container_test2 | SUCCESS => {
    "changed": false,
    "config_values": {
        "user.email": "maros.kukan@gmail.com",
        "user.name": "Maros"
    },
    "msg": ""
}
```

You can verify the changes by running bash on a sample container.

```bash
docker container exec -it ansible_container_test1 bash
root@19e8d86a26b1:/# git config --global --list
user.email=maros.kukan@gmail.com
user.name=Maros
```


## Tips

### Creating Command Aliases

Add this to your shell rc file, e.g. `~/.zshrc`

```bash
# Ansible aliases
alias ap='ansible-playbook'
alias acl="ansible-config list"
alias ail="ansible-inventory --list"
```

Once new aliases are loaded simple source the modified file `source ~/.zshrc` and you are ready to go.

### Gathering Facts

Gathering Facts about localhost
```bash
ansible -m setup localhost
```

Pretty printed module documentation
```bash
ansible-doc copy | bat --language yml
```

### Generating dynamic inventory

If you are using Vagrant with machines that have IP address assigned dynamicaly through DHCP, you may want to generate inventory file from `vagrant ssh-config`. Good tool to leverage is [Vagrant-to-ansible-inventory](https://github.com/haidaraM/vagrant-to-ansible-inventory) project.

I recommend creating a Python virtual environment and install the required package using pip before running the tool.

### Loading private keys

If private keys are not explicitly defined within hosts file they need to be loaded before Ansible can connect to machines provisioned by Vagrant.

```bash
for IdentityFile in $(vagrant ssh-config | grep IdentityFile | cut -d" " -f4)
do
    ssh-add ${IdentityFile}
done
```