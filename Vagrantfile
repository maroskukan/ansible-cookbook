# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  ## 2 ubuntu VMs 
  (10..11).each do |i|
    config.vm.define "ubuntu#{i}" do | ubuntu |
      ubuntu.vm.box = "generic/ubuntu2004"
      ubuntu.vm.network "private_network", ip: "192.168.137.#{i}"
    end
  end 

  ## 2 centos VMs
  (20..21).each do |i|
    config.vm.define "centos#{i}" do | centos |
      centos.vm.box = "generic/centos8"
      centos.vm.network "private_network", ip: "192.168.137.#{i}"
    end
  end
  config.vm.provision "shell", path: "provision.sh"
end
