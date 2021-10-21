# Ansible for Devops

- [Ansible for Devops](#ansible-for-devops)
  - [Documentation](#documentation)
  - [Book Notes](#book-notes)
    - [Chapter 1](#chapter-1)
    - [Chapter 2](#chapter-2)
    - [Chapter 3](#chapter-3)
    - [Chapter 4](#chapter-4)
## Documentation

- [Creating Custom Dynamic Inventories](https://www.jeffgeerling.com/blog/creating-custom-dynamic-inventories-ansible)
- [Ansible Vagrant Dynamic Inventory](https://charlesreid1.com/wiki/Ansible/Vagrant/Dynamic_Inventory)
- [Ansible YAML Callback plugin for better CLI experience](https://www.jeffgeerling.com/blog/2018/use-ansibles-yaml-callback-plugin-better-cli-experience)
- [Centos 7 Default Python Interpreter](https://britishgeologicalsurvey.github.io/devops/centos7-python2-end-of-life/)
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

### Chapter 4

For starters, you can easily converting any existing shell script into a playbook. For example, the following script will install Apache on RHEL based server:

```bash
# Install Apache.
yum install --quite -y httpd httpd-devel
# Copy configuration files.
cp httpd.conf /etc/httpd/conf/httpd.conf
cp httpd-vhosts.conf /etc/httpd/conf/httpd-vhosts.conf
# Start Apache and configure it to run at boot
service httpd start
chkconfig httpd on
```

To execute the script assuming exection flag is set with `chmod +x`. You simple run it as:

```bash
./shell-script.sh
```

The basic playbook with same logic would look like follows:

```yml
- hosts: all

  tasks:
    - name: Install Apache.
      ansible.builtin.command: yum install --quite -y httpd httpd-devel
    - name: Copy configuration files.
      ansible.builtin.command: >
        cp httpd.conf /etc/httpd/conf/httpd.conf
    - ansible.builtin.command: >
        cp httpd-vhosts.conf /etc/httpd/conf/httpd-vhosts.conf
    - name: Start Apache and configure it to run at boot.
      ansible.builtin.command: service httpd start
    - ansible.builtin.command: chkconfig httpd on
```
To execute the playbook you would simply run it as:

```bash
ansible-playbook main.yml
```

This is just a start, the next step would be refactor this playbook to take advantage of more suitable modules for task that add idempotence.

```yml
---
- hosts: all
  become: yes

  tasks:
    - name: Install Apache.
      ansible.builtin.yum:
        name:
          - httpd
          - httpd-devel

    - name: Copy configuration files.
      ansible.builtin.copy:
        src: "{{ item.src }}"
        dest: "{{ item.dest }}"
        owner: root
        group: root
        mode: 0644
      with_items:
        - src: httpd.conf
          dest: /etc/httpd/conf/httpd.conf
        - src: httpd-vhosts.conf
          dest: /etc/httpd/conf/httpd-vhosts.conf

    - name: Make sure Apache is started now and at boot.
      ansible.builtin.service:
        name: httpd
        state: started
        enabled: true
```

The above playbook targets all defined hosts. In order to limit the exeuction scope you can use the `--limit` argument.

```bash
ansible-playbook main.yml --limit webservers
```

Other used ansible-playbook arguments include:
- `--inventory=PATH (-i PATH)` which defines custom inventory file.
- `--verbose (-v)` which displays output in more detail. `-vvvv` is the most compherensive.
- `--extra-vars=VARS (-e VARS)` which defines variables used in playbook in `"key=value, key=value"` format.
- `--forks=NUM (-f NUM)` which defines number of cuncurent executions


It is good idea to use quotation for parameters in these cases:
- If you have a Jinja variable (e.g. `{{ variable_name }}`) at the benining or end of the line
- If you have any colons (`:`) in the string, for example in URLs.

