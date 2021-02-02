#!/bin/sh

# Updates permissions on vagrant private keys
# This is required only if you do not change default mount options for Windows drives in wsl.conf

for TARGET in $(vagrant status --machine-readable | grep metadata | cut -d"," -f2)
do
    mv .vagrant/machines/${TARGET}/hyperv/private_key ${HOME}/.ssh/vagrant_private_key_${TARGET}
    chmod 600 ~/.ssh/vagrant_private_key_${TARGET}
    ln -s ${HOME}/.ssh/vagrant_private_key_${TARGET} .vagrant/machines/${TARGET}/hyperv/private_key
    echo "Private key update for ${TARGET}" 
done
