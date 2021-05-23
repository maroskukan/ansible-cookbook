#!/usr/bin/bash

OS_RELEASE=$(awk -F= '/^NAME/{print $2}' /etc/os-release)

if [ "${OS_RELEASE}" = '"Ubuntu"' ]; then
    echo "Ubuntu Detected. Starting provisioning."
    apt-get -y update
    apt-get install -y lxc

elif [ "${OS_RELEASE}" = '"CentOS Linux"' ]; then
    echo "CentOS Detected. Starting provisioning."
    yum -y update
else
    echo "Unknown OS. Provisioning skipped."
fi