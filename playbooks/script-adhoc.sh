#!/usr/bin/env bash

# Ensure ~/.gitconfig is based on master.gitconfig
ansible -m copy -a "src=../adhoc/master.gitconfig dest=~/.gitconfig" localhost

# Ensure `bat` is installed
ansible -m homebrew -a "name=bat state=latest" localhost

# Ensure `jq` is installed
ansible -m homebrew -a "name=jq state=latest" localhost