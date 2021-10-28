# Ansible for Devops

- [Ansible for Devops](#ansible-for-devops)
  - [Documentation](#documentation)
  - [Book Notes](#book-notes)
    - [Chapter 1](#chapter-1)
    - [Chapter 2](#chapter-2)
    - [Chapter 3](#chapter-3)
    - [Chapter 4](#chapter-4)
    - [Chapter 5](#chapter-5)
      - [Handlers](#handlers)
      - [Environment variables](#environment-variables)
      - [Task environment variable](#task-environment-variable)
      - [Extra Variables](#extra-variables)
      - [Vault](#vault)
      - [Blocks](#blocks)
    - [Chapter 6](#chapter-6)
      - [Imports](#imports)
      - [Ansible Galaxy](#ansible-galaxy)
    - [Chapter 13 - Testing and CI for Ansible Content](#chapter-13---testing-and-ci-for-ansible-content)
      - [Yamllint](#yamllint)
      - [ansible-playbook --syntax-check](#ansible-playbook---syntax-check)
      - [ansible-lint](#ansible-lint)
## Documentation

- [Creating Custom Dynamic Inventories](https://www.jeffgeerling.com/blog/creating-custom-dynamic-inventories-ansible)
- [Ansible Vagrant Dynamic Inventory](https://charlesreid1.com/wiki/Ansible/Vagrant/Dynamic_Inventory)
- [Ansible YAML Callback plugin for better CLI experience](https://www.jeffgeerling.com/blog/2018/use-ansibles-yaml-callback-plugin-better-cli-experience)
- [Centos 7 Default Python Interpreter](https://britishgeologicalsurvey.github.io/devops/centos7-python2-end-of-life/)
- [Configuring your login session with dotfiles](http://mywiki.wooledge.org/DotFiles)
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

### Chapter 5

#### Handlers

To notify a single handler.

```yml
handlers:
  - name: restart apache
    service:
      name: apache2
      state: restart

tasks:
  - name: Enable Apache rewrite module.
    apache2_module:
      name: rewrite
      state: present
    notify: restart apache
```

To nofify multiple handlers.

```yml
tasks:
  - name: Rebuild application configuration
    command: /opt/app/rebuild.sh
  notify:
    - restart apache
    - restart memcached
```

```yml
handlers:
  - name: restart apache
    service:
      name: apache2
      state: restarted
    notify: restart memcached

  - name: restart memcached
    service:
      name: memcached
      state: restarted
```

#### Environment variables

To set variable for remote user account.

```yml
- name: Add an environment variable to the remote user's shell.
  lineinfile:
    dest: ~/.bash_profile
    regexp: '^ENV_VAR='
    line: "ENV_VAR=value"
```

Subsequent tasks will have access to this variable. However only `shell` module will understand commands that use variables.
To use an variable in further tasks, it is recommended to use taks's `register` option to store the environment variable.

```yml
- name: Add an environment variable to the remote user's shell.
  lineinfile:
    dest: ~/.bash_profile
    regexp: '^ENV_USER_VAR='
    line: "ENV_USER_VAR=value"

- name: Get the value of the environment variable we just added.
  shell: 'source ~/.bash_profile && echo $ENV_USER_VAR'
  register: foo

- name: Print the value of the environment variable.
  debug:
    msg: "The variable is {{ foo.stdout }}"
```

Global environment variables

```yml
- name: Add a global environment variable.
  lineinfile:
    dest: /etc/environment
    regexp: '^ENV_GLOBAL_VAR='
    line: "ENV_GLOBAL_VAR=value"
  become: true
```

If your application requires many environmental vairables consider using `copy` or `template` to set them accordingly.

#### Task environment variable

To set proxy server value inside a task.

```yml
- name: Downlaod a file, using example-proxy as a proxy.
  get_url:
    url: http://www.example.com/file.tar.gz
    dest: /tmp/file.tar.gz
  environment:
    http_proxy: http://example-proxy:80/
```

To set proxy server value as a reusable variable.

```yml
vars:
  proxy_vars:
    http_proxy: http://example-proxy:80/
    https_proxy: https://example-proxy:443/

tasks:
  - name: Download a file, using example proxy as a proxy.
    get_url:
      url: http://example.com/file.tar.gz
      dest: /tmp/file.tar.gz
    environment: proxy_vars
```

To set proxy settings using `/etc/environmnet`.

```yml
vars:
  proxy_state: present

tasks:
- name: Configure the proxy.
  lineinfile:
    dest: /etc/environment
    regexp: "{{ item.regexp }}"
    line: "{{ item.line }}"
    state: "{{ proxy_state }}"
  with_items:
    - regexp: "^http_proxy="
      line: "http_proxy=http://example-proxy:80/"
    - regex: "^https_proxy="
      line: "https_proxy=https://example-proxy:443/"
    - regexp: "^ftp_proxy="
      line: "ftp_proxy=http://example-proxy:80/"
```

You can test remote environment variable using ansible test command.

```bash
ansible centos -m shell -a 'echo $ENV_GLOBAL_VAR' -i inventory
centos | CHANGED | rc=0 >>
value
```

#### Extra Variables

Passing a single playbook variable:

```bash
ansible-playbook main.yml --extra-vars "foo=bar"
```

Passing multiple variables from file.

```bash
ansible-playbook main.yml --extra-vars "@even_more_vars.json"
ansible-playbook main.yml --extra-vars "@even_more_vars.yml"
```

Variables included in playbook:

```yml
---
- hosts: all

  vars:
    foo: bar

  tasks:
    # Prints "Variable 'foo' is set to bar".
    - debug:
        msg: "Variable 'foo' is set to {{ foo }}"
```

Variables included in separate file using `var_files` section.

```yml
- hosts: all

  vars_file:
    - vars.yml

  tasks:
    - debug:
        msg: "Variable 'foo' is set to {{ foo }}"
```

The above playbook uses this `vars.yml` file:

```yml
---
foo: bar
```

You can also stores variables in inventory files.

```ini
# Host-specific variables.
[washington]
app1.example.com proxy_state=present
app2.example.com proxy_state=absent

# Variables defined for the entire group.
[washington:vars]
cdn_host=washington.static.example.com
api_version=3.0.1
```

If you need to defined more variables, it is recommneded to store these in specific path e.g. `host_vars` or `group_vars`.

To capture output of one module and use it in later steps within playbook you can use `register` option.

```yml
- name: "Node: Check list of Node.js apps running."
  command: forever list
  register: forever_list
  changed_when: false

- name: "Node: Start example Node.js app"
  command: forever start {{ node_apps_location }}/app/app.js
  when: "forever_list.stdout.find(node_apps_location + '/app/app.js') == -1"
```

For larger and more structured arrays you can access any part of the array by drilling through the array keys using bracked `[]` or dot `.` syntax.
Start by inspecting the entire variable.

```yml
tasks:
  - debug:
      var: ansible_eth0
```

Then you can extract the required values.

```yml
{{ ansible_eth0.ipv4.address }}
{{ ansible_eth0['ipv4']['address'] }}
```

#### Vault

Ansible Vault is used to stored secrets in secure way. For example in the playbook you define.

```yml
---
- hosts: localhost
  connection: local
  gather_facts: false

  var_files:
    - vars/api_key.yml

  tasks:
    - name: Echo the API key which was injected into the env.
      shell: echo $API_KEY
      environment:
        API_KEY: "{{ myapp_api_key }}":
      register: echo_result

    - name: Show the result.
      debug: var=echo_result.stdout
```

The `api_key.yml` vars file, contains the following:

```yml
myapp_api_key: "fiaAHLIJFjiJHAFIWjfaJHWILjhFWLIAJHL"
```

Encrypt the file using Vault.

```bash
ansible-vault encrypt vars/api_key.yml
```

There are multiple ways how to supply password. When running the playbook interactively you can use the
`--ask-vault-pass` argument.

For automated playbook runs you can supply vault password via a password file. For example `~/.ansible/vault_pass.txt` with
chmod of `600`.

```bash
ansible-playbook main.yml --vault-password-file ~/.ansible/vault_pass.txt
```

#### Blocks

Blocks can be used to introduce try, except, finally logic in playbooks.

### Chapter 6

Ansible allows you to organize tasks in more efficient way than having everything in single playbook by using **imports**, **includes** and **roles**.

#### Imports

```yml
tasks:
  - import_tasks: user.yml
    vars:
      username: johndoe
      ssh_private_keys:
        - { src: /path/to/johndoe/key1, dest: id_rsa }
        - { src: /path/to/johndoe/key2, dest: id_rsa2 }

```

Tasks are formatted in a flat list in the included file `user.yml`.

```yml
- name: Add profile info for a user.
  copy:
    src: example_profile
    dest: "/home/{{ username }}/.profile
    owner: "{{ username }}"
    group: "{{ username }}"
    mode: 0744

- name: Add private keys for user.
  copy:
    src: "{{ item.src }}"
    dest: "/home/{{ username }}/.ssh/{{ item.dest }}"
    owner: "{{ username }}"
    group: "{{ username }}"
    mode: 0600
  with_items: "{{ ssh_private_keys }}"
```

#### Ansible Galaxy

Ansible Galaxy provides a platform to publish and share Ansible content such as collections and roles.

To help keep roles isolated between projects, you need to define custom role path inside project `ansible.cfg` configuration file.

```ini
[defaults]
roles_path = ./roles
```

Then you can download and install a particular role use the `role install` argument, followed by role name.

```bash
ansible-galaxy role install geerlingguy.solr
```

In order to list existing roles use the `role list` argument.

```bash
ansible-galaxy role list
# /mnt/c/Users/maros_kukan/vagrant/ansible-cookbook/examples/ansible-for-devops/chap6/roles
- geerlingguy.solr, 5.2.0
```

To remove installed role use the `role remove` argument, followed by the role name.

```bash
ansible-galaxy role remove geerlingguy.solr
```

You can also provide required collections using `requirements.yml` file inside the project directory and then install them via ansible-galaxy.

```yml
---
roles:
  - name: geerlinggiy.homebrew
    varsion: 3.1.0
```

```bash
ansible-galaxy install -r requirements.yml
```

### Chapter 13 - Testing and CI for Ansible Content

Ansible testing spectrum from least to most complex.

1. yamllint
2. ansible-playbook --syntax-check
3. ansible-lint
4. molecule test (integration)
5. ansible-playbook --check (against prod)
6. parallel infrastructure

#### Yamllint

```bash
yamllint chap13/03-yamllint/lint-example.yml
chap13/03-yamllint/lint-example.yml
  1:1       warning  missing document start "---"  (document-start)
  1:81      error    line too long (103 > 80 characters)  (line-length)
  2:17      warning  truthy value should be one of [false, true]  (truthy)
  6:81      error    line too long (101 > 80 characters)  (line-length)
  7:22      error    trailing spaces  (trailing-spaces)
  8:31      warning  too few spaces before comment  (comments)
  8:81      error    line too long (86 > 80 characters)  (line-length)
  13:1      warning  comment not indented like content  (comments-indentation)
  13:59     error    no new line character at the end of file  (new-line-at-end-of-file)
```

You can override some settings for example truthy values in `.yamllint`

```yml
---
extends: default

rules:
  truthy:
    allowed-values:
      - 'true'
      - 'false'
      - 'yes'
      - 'no'
```

#### ansible-playbook --syntax-check

```bash
ansible-playbook --syntax-check chap13/04-syntax-check/syntax-check.yml
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost
does not match 'all'
ERROR! Unable to retrieve file contents
Could not find or access '/mnt/c/Users/maros_kukan/vagrant/ansible-cookbook/examples/ansible-for-devops/chap13/04-syntax-check/free.yml' on the Ansible Controller.
If you are using a module and expect the file to exist on the remote, see the remote_src option
```

#### ansible-lint

```bash
ansible-lint chap13/05-ansible-lint/main.yml
WARNING  Overriding detected file kind 'yaml' with 'playbook' for given positional argument: chap13/05-ansible-lint/main.yml
WARNING  Listing 3 violation(s) that are fatal
command-instead-of-shell: Use shell only when shell functionality is required
chap13/05-ansible-lint/main.yml:7 Task/Handler: shell  uptime

no-changed-when: Commands should not change things if nothing needs doing
chap13/05-ansible-lint/main.yml:7 Task/Handler: shell  uptime

unnamed-task: All tasks should be named
chap13/05-ansible-lint/main.yml:7 Task/Handler: shell  uptime

You can skip specific rules or tags by adding them to your configuration file:
# .ansible-lint
warn_list:  # or 'skip_list' to silence them completely
  - command-instead-of-shell  # Use shell only when shell functionality is required
  - no-changed-when  # Commands should not change things if nothing needs doing
  - unnamed-task  # All tasks should be named

Finished with 3 failure(s), 0 warning(s) on 1 files.
```