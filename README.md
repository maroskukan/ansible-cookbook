# Ansible

## Installation

Installation depends on control node configuration. For example on Ubuntu the preferred way to install Ansible is to use the system package manager. Wherease on Mac OS X the preferred method is to install via pip.

## Documentation

[Modules Intro] https://docs.ansible.com/ansible/latest/user_guide/modules_intro.html


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

## Tips

Add this to your rc file, e.g. `~/.zshrc`
```bash
# Ansible aliases
alias ap='ansible-playbook'
```

Gathering Facts about localhost
```bash
ansible -m setup localhost
```

Pretty printed module documentation
```bash
ansible-doc copy | bat --language yml
```