# Examination 12 - Roles

So far we have been using separate playbooks and ran them whenever we wanted to make
a specific change.

With Ansible [roles](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse_roles.html) we
have the capability to organize tasks into sets, which are called roles.

These roles can then be used in a single playbook to perform the right tasks on each host.

Consider a playbook that looks like this:

    ---
    - name: Configure the web server(s) according to specs
      hosts: web
      roles:
        - webserver

    - name: Configure the database server(s) according to specs
      hosts: db
      roles:
        - dbserver

This playbook has two _plays_, each play utilizing a _role_.

This playbook is also included in this directory as [site.yml](site.yml).

Study the Ansible documentation about roles, and then start work on [QUESTION A](#question-a).

# QUESTION A

Considering the playbook above, create a role structure in your Ansible working directory
that implements the previous examinations as two separate roles; one for `webserver`
and one for `dbserver`.

Copy the `site.yml` playbook to be called `12-roles.yml`.

HINT: You can use

    $ ansible-galaxy role init [name]

to create a skeleton for a role. You won't need ALL the directories created by this,
but it gives you a starting point to fill out in case you don't want to start from scratch.


### Answer

administrator@administrator-Precision-T1650:~/Desktop/AnsibleWorkbook$ ansible-playbook 12-roles.yml --vault-password-file 11-vault_passwd.txt 

PLAY [Configure the web server(s) according to specs] **********************************************************************************

TASK [Gathering Facts] *****************************************************************************************************************
ok: [192.168.121.209]

TASK [webserver : Ensure all groups exist] *********************************************************************************************
ok: [192.168.121.209] => (item=wheel)
ok: [192.168.121.209] => (item=video)
ok: [192.168.121.209] => (item=audio)
ok: [192.168.121.209] => (item=tape)
ok: [192.168.121.209] => (item=tcdump)

TASK [webserver : Add user alovelace] **************************************************************************************************
changed: [192.168.121.209] => (item={'name': 'alovelace', 'groups': ['wheel', 'video', 'audio'], 'gecos': 'Ada Lovelace'})
changed: [192.168.121.209] => (item={'name': 'aturing', 'groups': ['tape'], 'gecos': 'Alan Turing'})
changed: [192.168.121.209] => (item={'name': 'edijkstra', 'groups': ['tcdump'], 'gecos': 'Edsger Dijkstra'})
changed: [192.168.121.209] => (item={'name': 'ghopper', 'groups': ['wheel', 'audio'], 'gecos': 'Grace Hopper'})

PLAY [Configure the database server(s) according to specs] *****************************************************************************

TASK [Gathering Facts] *****************************************************************************************************************
ok: [192.168.121.142]

TASK [dbserver : Ensure deploy's home directory exists] ********************************************************************************
ok: [192.168.121.142]

TASK [dbserver : Show found .md files] *************************************************************************************************
ok: [192.168.121.142] => (item=/home/administrator/Desktop/AnsibleWorkbook/files/baz.md) => {
    "ansible_loop_var": "item",
    "item": "/home/administrator/Desktop/AnsibleWorkbook/files/baz.md"
}
ok: [192.168.121.142] => (item=/home/administrator/Desktop/AnsibleWorkbook/files/bar.md) => {
    "ansible_loop_var": "item",
    "item": "/home/administrator/Desktop/AnsibleWorkbook/files/bar.md"
}
ok: [192.168.121.142] => (item=/home/administrator/Desktop/AnsibleWorkbook/files/foo.md) => {
    "ansible_loop_var": "item",
    "item": "/home/administrator/Desktop/AnsibleWorkbook/files/foo.md"
}

TASK [dbserver : Copy .md files to deploy's home directory] ****************************************************************************
ok: [192.168.121.142] => (item=/home/administrator/Desktop/AnsibleWorkbook/files/baz.md)
ok: [192.168.121.142] => (item=/home/administrator/Desktop/AnsibleWorkbook/files/bar.md)
ok: [192.168.121.142] => (item=/home/administrator/Desktop/AnsibleWorkbook/files/foo.md)

PLAY RECAP *****************************************************************************************************************************
192.168.121.142            : ok=4    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
192.168.121.209            : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0 