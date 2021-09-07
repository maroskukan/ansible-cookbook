# Ansible

- [Ansible](#ansible)
  - [Introduction](#introduction)
  - [Documentation](#documentation)
  - [Installation](#installation)
    - [Installing via PIP](#installing-via-pip)
  - [Ansible Configuration](#ansible-configuration)
    - [Settings Management](#settings-management)
    - [Host-Based Connection Variables](#host-based-connection-variables)
    - [Preparing the Control Machine](#preparing-the-control-machine)
    - [Preparing the Remote Node](#preparing-the-remote-node)
  - [Modules](#modules)
    - [Command Modules](#command-modules)
  - [Ad Hoc Mode](#ad-hoc-mode)
  - [Inventory](#inventory)
  - [Connection Parameters](#connection-parameters)
    - [Testing Connection](#testing-connection)
  - [Playbook](#playbook)
    - [Validating Playbook](#validating-playbook)
    - [Running Playbook](#running-playbook)
    - [Variables in Playbook](#variables-in-playbook)
      - [Naming Variables](#naming-variables)
      - [Scoping Variables](#scoping-variables)
      - [Managing Variables](#managing-variables)
      - [Referencing Variables](#referencing-variables)
      - [Host and Group Variables](#host-and-group-variables)
      - [Protecting Variables](#protecting-variables)
  - [Roles](#roles)
  - [Ansible Galaxy](#ansible-galaxy)
    - [Gathering information about role](#gathering-information-about-role)
    - [Installing a role](#installing-a-role)
    - [Installing a collection](#installing-a-collection)
    - [Listing installed collections](#listing-installed-collections)
  - [Ansible Console](#ansible-console)
  - [Ansible Pull](#ansible-pull)
  - [Execution](#execution)
    - [Facts gathering](#facts-gathering)
    - [Module arguments](#module-arguments)
    - [Limit](#limit)
    - [Tags](#tags)
    - [Pipelining](#pipelining)
  - [Troubleshooting](#troubleshooting)
    - [Ordering problems](#ordering-problems)
    - [Jumping to specific tasks](#jumping-to-specific-tasks)
  - [Tips](#tips)
    - [Creating Command Aliases](#creating-command-aliases)
    - [Gathering Facts](#gathering-facts)
    - [Generating dynamic inventory](#generating-dynamic-inventory)
    - [Loading private keys](#loading-private-keys)
    - [Application Configuration Pillars](#application-configuration-pillars)


## Introduction

Ansible is a tool that helps to automate IT tasks. Such task may include installing, updating and configuring software and services. 


## Documentation

- [Ansible Project](https://docs.ansible.com)
- [Modules Intro](https://docs.ansible.com/ansible/latest/user_guide/modules_intro.html)
- [Modules Index](https://docs.ansible.com/ansible/latest/collections/all_plugins.html)
- [Patterns - Targeting hosts and groups](https://docs.ansible.com/ansible/latest/user_guide/intro_patterns.html)
- [Roles](https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html)
- [Using Variables](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html)
- [Ansible Vault](https://docs.ansible.com/ansible/latest/user_guide/vault.html)
- [SSH Pipelining](https://docs.ansible.com/ansible/2.4/intro_configuration.html#pipelining)


## Installation

Installation depends on control node configuration. For example on Ubuntu the preferred way to install Ansible is to use the system package manager, in this case `apt`. Wherease on Mac OS X the preferred method is to install via python package manager `pip`.

Therefore, best way is to always consult the [Installing Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html) section of available at official documentation.

### Installing via PIP

One of the common ways is to install Ansible using Python's package manager `pip`. I highly recommend installing inside a virtual environment, for example using the [Simple Python Version Mamangement](https://github.com/pyenv/pyenv) and [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) tool.

```bash
# Download and Install Python 3.9.6
pyenv install 3.9.6

# Create and activate virtual environment
pyenv virtualenv 3.9.6 ansible-cookbook
pyenv activate ansible-cookbook

# Update pip, setuptools and install:
# - ansible
# - vagranttoansible (creates inventory from vagrant environment)
# - ansible-lint (checks for best practices)
pip install --upgrade pip setuptools
pip install -r requirements.txt

# Verify ansible installation
ansible --version
ansible [core 2.11.4]
  config file = /home/mkukan/code/maroskukan/ansible-cookbook/ansible.cfg
  configured module search path = ['/home/mkukan/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /home/mkukan/.pyenv/versions/3.9.6/envs/ansible-cookbook/lib/python3.9/site-packages/ansible
  ansible collection location = /home/mkukan/.ansible/collections:/usr/share/ansible/collections
  executable location = /home/mkukan/.pyenv/versions/ansible-cookbook/bin/ansible
  python version = 3.9.6 (default, Aug 21 2021, 19:18:25) [GCC 9.3.0]
  jinja version = 3.0.1
  libyaml = True

# Finally to deactivate virtual environment
pyenv deactivate ansible-cookbook
```

*Note: If your project directory has `.python-version` with name of the virtual environment defined, it will get automatically activated when you are in this directory.*


## Ansible Configuration

The behavior of Ansible installation can be adjusted by modifying settings in Ansible configuration file. Ansible chooses its current configuration from one of serveral possible locations. The following order applies:

- The `ANSIBLE_CONFIG` environment variable.
- The `./ansible.cfg` in ansible command current working directory
- The `~/.ansible.cfg` located in your home folder
- The `/etc/ansible/ansible.cfg` the default installation folder

To verify which location of ansible configuraiton file is being used when calling ansible commands, use the `ansible --version` command. 

To verify the content of ansible configuration file that is being used, use the `ansible-config view` command.

### Settings Management

Each ansible configuration `ansible.cfg` containes one ore more section titles enclosed in square brackets. Each section contains settings defined as key-valye pair.

Basic operations use two main sections:

- `[defaults]` sets defaults for Ansible operation, for example connection settings.
- `[privilege_escalation]` configures how Ansible performs privileges escalation on managed hosts.

```ini
[defaults]
host_key_checking = False
inventory = ./inventory
```

There are many other settings that can be defined in `[defaults]` section, for example:
- `remote_user` specifies the user you want to use on the managed hosts. If unspecified, the current user name will be used.
- `remote_port` specifies which sshd port you want to use on the managed hosts. If unspecified, the default port is 22.
- `ask_pass` controls whether Ansible will prompt you for the SSH password. If unspecified, it is assumed that you are using SSH key-based authentication.


The settings that can be defined in `[privilege_escalation]` section, for example:
- `become` controls whether you will automatically use privilege escalation. Default is `no`.
- `become_user` controls which user on the managed host Ansible should become (Default is `root`)
- `become_method` controls how Ansible will become that user (using `sudo` by default, there are other options like `su`)
- `become_ask_pass` controls whether to prompt you for a password for your become method (default is `no`)

*Please note that many settings can be overrided at inventory level if required.*

To view all available settings with their explanation use `ansible-config list` command.

To view all values (including default) for current setting use the `ansible-config dump` command. To view only values that we changed use `ansible-config dump --only-changed`.


### Host-Based Connection Variables

As mentioned in section before, settings can be overrided at inventory level by setting connection variables. There ware multiple ways to accomplish this:
- Place the settings in a file in the `host_vars` directory in the same directory as your inventory file
- These settings override the ones in `ansible.cfg`
- They also have slightly different syntax and naming. For example `remote_user` (global) vs `ansible_user` (inventory)


### Preparing the Control Machine

The Control Machine is server where Ansible is installed. In order to utilizede SSH key-based authentication it is required to generate a key pair, and distribute the public key to each remote node by storing it in `authorized_keys` file.


### Preparing the Remote Node

Although the default Ansible mode of operation which uses push model, does not require any installed agent present on the manage hosts, there are some required settings that need to be set in order for host to be managed by Ansible control node:

- SSH key-based authentication to an unprivileged account that can use `sudo` to become `root` without a password.
- Ansible allows further flexibility to meet your current security policy

More details on how to setup both, Control Machine and Remote node can be found in this [Medium article](https://medium.com/openinfo/ansible-ssh-private-public-keys-and-agent-setup-19c50b69c8c)


## Modules

From documenation, Modules (also referred to as “task plugins” or “library plugins”) are discrete units of code that can be used from the command line or in a playbook task. Ansible executes each module, usually on the remote managed node, and collects return values. In Ansible 2.10 and later, most modules are hosted in collections.

To display all installed modeles on system use the `ansible-doc -l` command. The name and the description of module is displayed. To display information about a particular module use `ansible-doc [module-name]` for example:

```yml
ansible-doc copy | bat --language yml
> ANSIBLE.BUILTIN.COPY    (/home/maros/.local/lib/python3.8/site-packages/ansible/modules/copy.py)

        The `copy' module copies a file from the local or remote
        machine to a location on the remote machine. Use the
        [ansible.builtin.fetch] module to copy files from remote
        locations to the local box. If you need variable interpolation
        in copied files, use the [ansible.builtin.template] module.
        Using a variable in the `content' field will result in
        unpredictable output. For Windows targets, use the
        [ansible.windows.win_copy] module instead.

  * note: This module has a corresponding action plugin.

OPTIONS (= is mandatory):

- attributes
        The attributes the resulting file or directory should have.
        To get supported flags look at the man page for `chattr' on
        the target system.
        This string should contain the attributes in the same order as
        the one displayed by `lsattr'.
        The `=' operator is assumed as default, otherwise `+' or `-'
        operators need to be included in the string.
        (Aliases: attr)[Default: (null)]
        type: str
        version_added: 2.3
        version_added_collection: ansible.builtin

- backup
        Create a backup file including the timestamp information so
        you can get the original file back if you somehow clobbered it
        incorrectly.
        [Default: False]
        type: bool
        version_added: 0.7
        version_added_collection: ansible.builtin
[ Output omitted ]
```

Some common ansible modules include:

- File Modules:
  - `copy` Copy a local file to the manages host
  - `file` Set permissions and other properties of files
  - `lineinfile` Ensures a particular line is or is not in a file
  - `synchronize` Synchronizes content using rsync
- Software package modules:
  - `package` Manages Packages
  - `apt` Manages Packages using APT
  - `yum` Manages Packages using YUM
  - `gem` Manages Ruby packages
- System Modules
  - `firewalld` Manages arbitrary ports and services using firewalld
  - `reboot` Reboot the machine
  - `service` Managing services
  - `user` Add, remove and manage user accounts
- Net Tools Modules
  - `get_url` Download files over HTTP, HTTPS, or FTP
  - `nmcli` Manage networking
  - `uri` Interact with web services and comminicate with APIs

### Command Modules

There are a handful of modules that run commands directly on the manage host. You can use these if no other module is available to do what you need. They are **not idempotent** you must make sure that they are safe to run twice when using them. An example of such modules are:

- `command` runs a single command on the system
- `shell` runs a command on the remote system's shell (redirection to other features work)
- `raw` simply run a command with no processing (can be dangerous but can be useful when managing systems that cannot have Python installed (for example legacy network equipment)


## Ad Hoc Mode

Ad Hoc refers to mode where ansible is used one time, often to test module or experiment as it does not require any significant configuration (such as playbooks). When calling a module, you often need to define mandatory variables. In example below the `copy` module requires that you define source and destination path for file you want to copy. 


```bash
ansible -m copy -a "src=master.gitconfig dest=~/.gitconfig" localhost
```

Dry run.
```bash
ansible -m copy -a "src=master.gitconfig dest=~/.gitconfig" --check localhost
```

Dry run with diff flag.
```bash
ansible -m copy -a "src=master.gitconfig dest=~/.gitconfig" --check --diff localhost
```

The following example demostrates the use of **homebrew** module.

```
ansible -m homebrew -a "name=bat state=latest" localhost
ansible -m homebrew -a "name=jq state=latest" localhost
```


## Inventory

Inventory files describe a collection of hosts or systems you want to manage using ansible commands. Hosts can be assigned to groups and groups can contain other child groups. Hosts can be members of multiple groups. Variables can be set that apply to hosts and groups. For example connection parameters, such as SSH username or port.

There are many different types of inventory files. They can be defined in various formats, for example ini, yaml. To see full list use the following `ansible-doc` command.
```bash
ansible-doc -t inventory --list
```

It is common to define the location of inventory file within `ansible.cfg` configuration file under `[defaults]` sections. The below example defines an inventory folder `inventory` located in same directory as ansible configuration file.
```ini
[defaults]
inventory = ./inventory
```

The content of this folder is as follows:
```bash
inventory
├── explicit-localhost
├── group-centos
├── group-ubuntu
├── group-vagrant
├── rhel-hosts.py
├── sles-host
├── ubuntu-centos-hosts.yml.orig
```

To verify if the inventory was correctly formatted and understood by ansible you can use `ansible-inventory` command with options such as `list` or `graph`. Example below shows the output of these commands.
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

Another way how to verify the inventory configuration is to use ansible command with `list-hosts` paramter. This command also supports globbing `*`. You can also specify multiple groups or hosts with comma. Indexing and negation is also supported. This is useful when you need to be usre that you are targeting the correct hosts.

```bash
ansible --list-hosts all
  hosts (8):
    localhost
    sles40
    rhel30
    rhel31
    centos20
    centos21
    ubuntu10
    ubuntu11

ansible --list-hosts "ubuntu*"
  hosts (2):
    ubuntu10
    ubuntu11

ansible --list-hosts vagrant,localhost
  hosts (5):
    centos20
    centos21
    ubuntu10
    ubuntu11
    localhost

# 
# Note: In zsh you may need to excape [0] as \[0\]
#
ansible --list-hosts all[0]
  hosts (1):
    ubuntu10

ansible --list-hosts \!ubuntu
  hosts (6):
    localhost
    sles40
    rhel30
    rhel31
    centos20
    centos21
```


## Connection Parameters

Connection parameters define a means how to interact with manage host. To display available `connection` module plugins use the following command:

```bash
ansible-doc -t connection --list
local                       execute on controller
paramiko_ssh                Run tasks via python ssh (paramiko)
psrp                        Run tasks over Microsoft PowerShell Remoting Protocol
ssh                         connect via ssh client binary
winrm                       Run tasks over Microsoft's WinRM
```

By default, ssg connection protocol is leveraged when connecting to linux hosts. By using collections and roles it is possible to expand the dafualt list of connection plugins. 

### Testing Connection

In order to conduct a simple reachability test for hosts defined in inventory you can use Ansible ad-hoc command with `ping` module. Below I am running this module agains `vagrant` host group.

```json
ansible -m ping ubuntu 
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


## Playbook

Playbook is a YAML-based text file which list one or more plays in specific order. A play is an ordered list of tasks run against a specific hosts within an inventory.

Each task runs a module that performs some simple action on or for the manage host. Most tasks are idempotent and can be safely run a second time without problems. 

The the example below, we are executing single task using `copy` module on `localhost`. 

```yml
---
- name: Description of first play
- hosts: localhost
  tasks:
    - name: Description of first task
    - copy: src="master.gitconfig" dest="~/.gitconfig"
```

The playbook below uses a different format, but results in same end state.

```yml
---
- hosts: localhost
  tasks:
    - copy: 
        src: "master.gitconfig"
        dest: "~/.gitconfig"
```

### Validating Playbook

You can use `-C` option to perform a dry run of the playbook execution. This causes Ansible to report what changes would have occurred if the playbook were executed, but does not make any actual changes to managed hosts.

```bash
ansible-playbook -C playbook.yml
```

### Running Playbook

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

### Variables in Playbook

Variables increase the code reusability by decoupling dynamic values that are unique for given project. This simplifies the creation and maitenance of code and reduces number of erros.

Variables can contain items like:
- Unique Users to create, modify or delete
- Unique Software to install and uninstall
- Unique Services to start, stop and restart
- Unique Credentials to manage

#### Naming Variables

Variables must start with a letter, and they can only contain letters, numbers and underscores. An example of valida variables include:

```bash
web_server
remote_file
file1
file_1
remote_server1
remote_server_1
```

#### Scoping Variables

There are three avaiable scopes (or reaches) where a variable exists:

- **Global**
  - The value is set for all hosts
  - Example: extra variables you set in the job template
- **Host**
  - The value is set for a particular host (or group)
  - Examples: variables set for a host in the inventory or *host_vars* directory, gathered facts
- **Play**
  - The value is set for all hosts in the context of the current play.
  - Examples: **vars** directives in a play, **include_vars** tasks and so on

There are few rules that define order of operations for variables:
- If variable is defined at more than one level, the level with the highest precedence wins. 
- A narrow scope generally takes precedence over a wider scope.
- Variables that you define in an inventory are overridden by variables that you define in the playbook.
- Variables defined in a playbook are overridden by "extra variables" defined on the command line with the `-e` option.

#### Managing Variables

Variables can be defined in multuple ways. Once common method is to place a variable in **vars** block at the beginning of a play:

```yaml
- hosts: all
  vars:
    user_name: joe
    user_state: present
```

It is also possible to define play variables in external files. Use `var_files` at the start of the play to load variables from a list of files into the play:

```yaml
- hosts: all
  vars_files:
    - vars/users.yml
```

#### Referencing Variables

After declaring variables, you can use them in tasks. Reference a variable by placing the variable name in double braces: `{{ variable_name }}`. Ansible substitutes the variable with its value when it runs the task.

When you reference one variable as another variable's value, and the curly braces start the value, you must use quotes around teh value. For example `name: "{{ user_name }}`

```yml
- name: Example play
  hosts: all
  vars:
    user_name: joe

  tasks:
    # This line wil read: Creates the user joe
    - name: Creates the user {{ user_name }}
      user:
        # This line will create the user named joe
        name: "{{ user_name }}"
        state: present
```

#### Host and Group Variables

Host variables applly to a specific host, whereas Group variables apply to all hosts in a host group or iin a group of host groups.

Host variables take precedence over group variables, but variables defined inside a play take precedence over both.

Host variables and group variables can be defined:
- In the inventory itself
- In `host_vars` and `group_vars` directories in the same directory as the inventory
- In `host_vars` and `group_vars` directories in the same directory as the playbook. These are host and group based but have higher precedence than inventory variables.


#### Protecting Variables

There are cases where you need to store sensitive data such as passwords, API keys and other secrets. These secrets are passed to Ansible thorugh variables. 

Ansible Vault provides a way to encrypt and decrypt files used by playbooks. The `ansible-vault` command is used to to manage these files.

The syntax of this command is `ansible-vault [ create | view | edit ] <filename>`

If the file already exists, you can encrypt it with `ansible-vault encrypt <filename>`. Optionally you can save the encrypted file with a new name using `--output=new_filename` option. 

To decrypt a file use `ansible-vault decrypt <filename>`.

When using playbook you with file encrypted by vault, you need to povide vault password using the `--vault-id` option. For example
```bash
ansible-playbook --ask-vault-pass <playbook>
```

The `@prompt` option will prompt user for the Ansible Vault password.

In same cases you need to use multiple passwords for different files. In such case you need to set labels during file encryption for example.

```bash
# Encrypt files using labels
ansible-vault encrypt <gvars_filename> --vault-id gvars@prompt
ansible-vault encrypt <lvars_filename> --vault-id lvars@prompt
# Specify the labels during playbook invocation
ansible-playbook --vault-id gvars@prompt --vault-id lvars@prompt playbook.yml
```

If you need to change a password on an encrypted file. You can use the `ansible-vault rekey <filename>` option.


## Roles

Ansible role is a folder that containes tasks, files, tempaltes, handlers, variables and playbooks to achieve desired state. 

For example, a base role could include shared system packages and configuration which can be applied to all targets. A service specific role (web, app, db) can be applied to only selected ones.

By using variables and encapsulation greatly increases reausability and scalability.

To create a new role skeleton, you can leverage `ansible-galaxy`.

```bash
ansible-galaxy init control
- Role control was created successfully
```


## Ansible Galaxy

[Ansible Galaxy](https://galaxy.ansible.com) privides a platform for distributing high level constructs that can be reused amoungs ansible users.

### Gathering information about role

```bash
ansible-galaxy role info geerlingguy.docker | bat -l yml
```

### Installing a role

```bash
ansible-galaxy role install geerlingguy.docker 
```

### Installing a collection

```bash
ansible-galaxy collection install -r requirements.yml
```

### Listing installed collections

```bash
ansible-galaxy collection list

# /home/maros/.ansible/collections/ansible_collections
Collection        Version
----------------- -------
community.docker  1.2.1
community.general 2.0.0
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

## Ansible Pull

A decentralized mode of operations, where self-manage nodes have scheduled job to pull playbookf from central VCS and execute it using local ansible installation.

Full documentation on this feature can be found [here](https://docs.ansible.com/ansible/latest/cli/ansible-pull.html)


## Execution

Ansible playbook execution can be optimized number of ways. In order to get a baseline measure your current execution time.

```Note: you can located these playbooks in examples/class-mastering-ansible```

```bash
time ansible-playbook site.yml
...
[Output omitted for brevity]
...
15.24s user 3.77s system 37% cpu 50.348 total

time ansible-playbook stack_status.yml
...
[Output omitted for brevity]
...
6.83s user 1.72s system 53% cpu 16.042 total
```

### Facts gathering

One of the ways to decrease execution time is to disable facts gathering when it is not used.

```yml
gather_facts: no
```


### Module arguments

Depending on module that is being used, an optimization step can be introduced at this level. For example instead of updating apt cache for each role or play, you can do it in the begining and set cache timeout like in example below.

```yml
---
- hosts: all
  become: yes
  gather_facts: no
  tasks:
    - name: update apt cache
      ansible.builtin.apt: update_cache=yes cache_valid_time=86400

- include: control.yml
- include: database.yml
- include: webserver.yml
- include: loadbalancer.yml
```

### Limit

If need to target only particular host or group instead of the ones defined in playbook, you can use the `--limit` or `-l` argument.

```bash
ansible-playbook site.yml -l app01
```

### Tags

Tags can be used to selectively run particular tasks or set of tasks. 

Start by defining a tag for particular task inside playbook.

```yml
---
- name: install tools
  ansible.builtin.apt: name="{{ item }}" state=present
  with_items:
    - curl
  tags: ['packages']
```

To list available tasks in playbook(s) use the `--list-tags` argument.

```bash
ansible-playbook site.yml --list-tags
playbook: site.yml

  play #1 (all): all    TAGS: []
      TASK TAGS: [packages]

  play #2 (control): control    TAGS: []
      TASK TAGS: [packages]

  play #3 (database): database  TAGS: []
      TASK TAGS: [configure, packages, service]

  play #4 (webserver): webserver        TAGS: []
      TASK TAGS: [configure, packages, service, system]

  play #5 (loadbalancer): loadbalancer  TAGS: []
      TASK TAGS: [configure, packages, service]
```

To run this tagged task(s).

```bash
ansible-playbook site.yml --tags "packages"
```

To run all tasks except the one with tag.

```bash
time ansible-playbook site.yml --skip-tags "packages"
...
[Output omitted for brevity]
...
11.33s user 2.77s system 49% cpu 28.544 total
```


### Pipelining

Pipelining reduces the number of operations that SSH needs to perform during connection setup. By default it is disabled but can be overided in `ansible.cfg`. There are some system prerequisites though.

```ini
...
[ssh_connection]
pipelining = True
```


## Troubleshooting

### Ordering problems

When you initial write a playbook, you likely start by installing packages and ensuring that the service is started.

However, as you add more service configuration it is required to reconsider placement of initial tasks such as service start close to end of the playbook, so the changes to configuration files are picked up. 

### Jumping to specific tasks

When you troubleshoot a specific tasks it is feasible to focus just on that particular section. You could comment out the rest of the playbook or take advantage of `list-tasks` and `start-at-task` argument.


```bash
ansible-playbook site.yml --list-tasks
ap site.yml --list-tasks

playbook: site.yml

  play #1 (all): all    TAGS: []
    tasks:
      update apt cache  TAGS: [packages]

  play #2 (control): control    TAGS: []
    tasks:
      control : install tools   TAGS: [packages]

  play #3 (database): database  TAGS: []
    tasks:
      mysql : install tools     TAGS: [packages]
      mysql : install mysql-server      TAGS: [packages]
      mysql : ensure mysql listening on eth0 port       TAGS: [configure]
      mysql : ensure mysql started      TAGS: [service]
      mysql : create database   TAGS: [configure]
      mysql : create demo user  TAGS: [configure]

  play #4 (webserver): webserver        TAGS: []
    tasks:
      apache2 : install web components  TAGS: [packages]
      apache2 : ensure mod_wsgi enabled TAGS: [configure]
      apache2 : de-activate default apache site TAGS: [configure]
      apache2 : ensure apache2 started  TAGS: [service]
      demo_app : install web components TAGS: [packages]
      demo_app : copy demo app source   TAGS: [configure]
      demo_app : copy demo.wsgi TAGS: [configure]
      demo_app : copy apache virtual host config        TAGS: [configure]
      demo_app : setup python virtualenv        TAGS: [system]
      demo_app : activate demo apache site      TAGS: [configure]

  play #5 (loadbalancer): loadbalancer  TAGS: []
    tasks:
      nginx : install nginx     TAGS: [packages]
      nginx : configure nginx sites     TAGS: [configure]
      nginx : get active sites  TAGS: [configure]
      nginx : de-activate sites TAGS: [configure]
      nginx : activate sites    TAGS: [configure]
      nginx : ensure nginx started      TAGS: [service]
```

You can also use `--step` argument to go over each task of the play answering whether you want to run it or not run it.

```bash
ansible-playbook site.yml --step
PLAY [all] *********************************************************************
Perform task: TASK: update apt cache (N)o/(y)es/(c)ontinue: Y
```


## Tips

### Creating Command Aliases

Add this to your shell rc file, e.g. `~/.zshrc`

```bash
# Ansible aliases
alias ap='ansible-playbook'
alias acl="ansible-config list"
alias ail="ansible-inventory --list"
alias aig="ansible-inventory --graph"
```

Once new aliases are loaded simple source the modified file `source ~/.zshrc` and you are ready to go.

### Gathering Facts

Facts are useful when you need to gather information about particular target which can be reaused in later steps of the playbook.

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

### Application Configuration Pillars

Any application deployment can be broken down into four pillars or stages.

1. Software Packages - Code required to run the software. Can come from software package repositories, (apt, yum, pip) as well as version control systems (git)
2. Service Handlers - Such as scripts, init.d, systemd, they may be already included with software package
3. System Configuration - Such as user permissions, firewall rules and any state that is required
4. Software Configuration - Such as appication configuration and content files.