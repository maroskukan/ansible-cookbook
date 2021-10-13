# Ansible for Devops

- [Ansible for Devops](#ansible-for-devops)
  - [Documentation](#documentation)
  - [Book Notes](#book-notes)
    - [Chapter 1](#chapter-1)
    - [Chapter 2](#chapter-2)
    - [Chapter 3](#chapter-3)
## Documentation

- [Creating Custom Dynamic Inventories](https://www.jeffgeerling.com/blog/creating-custom-dynamic-inventories-ansible)
- [Ansible Vagrant Dynamic Inventory](https://charlesreid1.com/wiki/Ansible/Vagrant/Dynamic_Inventory)
- [Ansible YAML Callback plugin for better CLI experience](https://www.jeffgeerling.com/blog/2018/use-ansibles-yaml-callback-plugin-better-cli-experience)

## Book Notes

### Chapter 1

My preferered way of installing ansible is using pip within a virtual environment.

```bash
pip install ansible
```
### Chapter 2

Vagrant file can be used for quick VM provisioning using ansible.

```ruby
# ...
  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "playbook.yml"
  end
# ...
```

### Chapter 3

Some useful ansible ad-hoc commands.

```bash
# Display hostname for group multi
ansible -i ./inventory -a "hostname" multi

# Display disk usage for group multi
ansible -i ./inventory -a "df -h" multi

# Display memory usage for group multi
ansible -i ./inventory -a "free -h" multi

# Display date for group multi
 ansible -i ./inventory -a "date"multi

# Display gathered facts for host db
ansible -i ./inventory -m setup db

# Install a package with become option on group multi
ansible -i ./inventory -b -m yum -a "name=ntp state=present" multi

# Ensure ntpd service is started and enable on group multi
ansible -i ./inventory -b -m service -a "name=ntpd state=started enabled=yes" multi

# Stop NTP, resync time and start service
ansible -i ./inventory -b -a "service ntpd stop" multi
ansible -i ./inventory -b -a "ntpdate -q 0.rhel.pool.ntp.org" multi
ansible -i ./inventory -b -a "service ntpd start" multi
```