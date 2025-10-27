# Examination 11 - Loops

Imagine that on the web server(s), the IT department wants a number of users accounts set up:

    alovelace
    aturing
    edijkstra
    ghopper

These requirements are also requests:

* `alovelace` and `ghopper` should be added to the `wheel` group.
* `aturing` should be added to the `tape` group
* `edijkstra` should be added to the `tcpdump` group.
* `alovelace` should be added to the `audio` and `video` groups.
* `ghopper` should be in the `audio` group, but not in the `video` group.

Also, the IT department, for some unknown reason, wants to copy a number of '\*.md' files
to the 'deploy' user's home directory on the `db` machine(s).

I recommend you use two different playbooks for these two tasks. Prefix them both with `11-` to
make it easy to see which examination it belongs to.

# QUESTION A

Write a playbook that uses loops to add these users, and adds them to their respective groups.

When your playbook is run, one should be able to do this on the webserver:

    [deploy@webserver ~]$ groups alovelace
    alovelace : alovelace wheel video audio
    [deploy@webserver ~]$ groups aturing
    aturing : aturing tape
    [deploy@webserver ~]$ groups edijkstra
    edijkstra : edijkstra tcpdump
    [deploy@webserver ~]$ groups ghopper
    ghopper : ghopper wheel audio

There are multiple ways to accomplish this, but keep in mind _idempotency_ and _maintainability_.
### Answer

---
- name: Create Users and Add them in groups
  hosts: web
  become: true

  vars:
    groups_to_create:
      - wheel
      - video
      - audio
      - tape
      - tcdump

    users:
      - name: alovelace
        groups: ['wheel', 'video', 'audio']
      - name: aturing
        groups: ['tape']
      - name: edijkstra
        groups: ['tcdump']
      - name: ghopper
        groups: ['wheel', 'audio']
  tasks:

     - name: Ensure all groups exist
       ansible.builtin.group:
         name: "{{ item }}"
         state: present
       loop: "{{ groups_to_create }}"

     - name: Add user alovelace
       ansible.builtin.user:
         name: "{{ item.name }}"
         groups: "{{ item.groups | join(',') }}"
         append: yes
         state: present
       loop: "{{ users }}"

# QUESTION B

Write a playbook that uses

    with_fileglob: 'files/*.md5'

to copy all `\*.md` files in the `files/` directory to the `deploy` user's directory on the `db` server(s).

For now you can create empty files in the `files/` directory called anything as long as the suffix is `.md`:

    $ touch files/foo.md files/bar.md files/baz.md

### Answer

administrator@administrator-Precision-T1650:~/Desktop/AnsibleWorkbook$ ansible-playbook 11-db-copymd.yml 

PLAY [Copy .md files from host to dbservers] *******************************************************************************************

TASK [Gathering Facts] *****************************************************************************************************************
ok: [192.168.121.142]

TASK [Ensure deploy's home directory exists] *******************************************************************************************
changed: [192.168.121.142]

TASK [Copy .md files to deploy's home directory] ***************************************************************************************
changed: [192.168.121.142] => (item=/home/administrator/Desktop/AnsibleWorkbook/files/baz.md)
changed: [192.168.121.142] => (item=/home/administrator/Desktop/AnsibleWorkbook/files/bar.md)
changed: [192.168.121.142] => (item=/home/administrator/Desktop/AnsibleWorkbook/files/foo.md)

PLAY RECAP *****************************************************************************************************************************
192.168.121.142            : ok=3    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0  

Check:

[deploy@webserver ~]$ ssh deploy@192.168.121.142 "ls -l ~/*.md"
-rw-r--r--. 1 deploy deploy 0 Oct 26 12:27 /home/deploy/bar.md
-rw-r--r--. 1 deploy deploy 0 Oct 26 12:27 /home/deploy/baz.md
-rw-r--r--. 1 deploy deploy 0 Oct 26 12:27 /home/deploy/foo.md


# BONUS QUESTION

Add a password to each user added to the playbook that creates the users. Do not write passwords in plain
text in the playbook, but use the password hash, or encrypt the passwords using `ansible-vault`.

There are various utilities that can output hashed passwords, check the FAQ for some pointers.

### Answer
I updated the playbook

---
- name: Create Users and Add them in groups
  hosts: web
  become: true

  vars:
    groups_to_create:
      - wheel
      - video
      - audio
      - tape
      - tcdump

    users:
      - name: alovelace
        groups: ['wheel', 'video', 'audio']
      - name: aturing
        groups: ['tape']
      - name: edijkstra
        groups: ['tcdump']
      - name: ghopper
        groups: ['wheel', 'audio']

  vars_files:
      - 11-vault.yml

  tasks:

     - name: Ensure all groups exist
       ansible.builtin.group:
         name: "{{ item }}"
         state: present
       loop: "{{ groups_to_create }}"

     - name: Add user alovelace
       ansible.builtin.user:
         name: "{{ item.name }}"
         groups: "{{ item.groups | join(',') }}"
         password: "{{ user_passwords[item.name] | password_hash('sha512') }}"
         append: yes
         state: present
       loop: "{{ users }}"


administrator@administrator-Precision-T1650:~/Desktop/AnsibleWorkbook$ ansible-playbook 11-web-addusers.yml --vault-password-file 11-vault_passwd.txt

PLAY [Create Users and Add them in groups] *********************************************************************************************

TASK [Gathering Facts] *****************************************************************************************************************
ok: [192.168.121.209]

TASK [Ensure all groups exist] *********************************************************************************************************
ok: [192.168.121.209] => (item=wheel)
ok: [192.168.121.209] => (item=video)
ok: [192.168.121.209] => (item=audio)
ok: [192.168.121.209] => (item=tape)
ok: [192.168.121.209] => (item=tcdump)

TASK [Add user alovelace] **************************************************************************************************************
changed: [192.168.121.209] => (item={'name': 'alovelace', 'groups': ['wheel', 'video', 'audio']})
changed: [192.168.121.209] => (item={'name': 'aturing', 'groups': ['tape']})
changed: [192.168.121.209] => (item={'name': 'edijkstra', 'groups': ['tcdump']})
changed: [192.168.121.209] => (item={'name': 'ghopper', 'groups': ['wheel', 'audio']})

PLAY RECAP *****************************************************************************************************************************
192.168.121.209            : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

Check:

[deploy@webserver ~]$ sudo grep alovelace /etc/shadow
alovelace:$6$rounds=656000$C3JfE1Xt4Cv.fWpt$Nb8yQGzErIrOruh0zSWdAJePiZBrsZVWjZULNihOxNeIl50z.DWLyu4rVqF4YJGdRZr/8ngWmJrYDHmMRRGvn.:20387:0:99999:7:::


# BONUS BONUS QUESTION

Add the real names of the users we added earlier to the GECOS field of each account. Google is your friend.

### Answer
alovelace is Ada Lovelace
aturing is Alan Turing
edijkstra is Edsger Dijkstra
ghopper is Grace Hopper

administrator@administrator-Precision-T1650:~/Desktop/AnsibleWorkbook$ ansible-playbook 11-web-addusers.yml --vault-password-file 11-vault_passwd.txt

PLAY [Create Users and Add them in groups] *********************************************************************************************

TASK [Gathering Facts] *****************************************************************************************************************
ok: [192.168.121.209]

TASK [Ensure all groups exist] *********************************************************************************************************
ok: [192.168.121.209] => (item=wheel)
ok: [192.168.121.209] => (item=video)
ok: [192.168.121.209] => (item=audio)
ok: [192.168.121.209] => (item=tape)
ok: [192.168.121.209] => (item=tcdump)

TASK [Add user alovelace] **************************************************************************************************************
changed: [192.168.121.209] => (item={'name': 'alovelace', 'groups': ['wheel', 'video', 'audio'], 'gecos': 'Ada Lovelace'})
changed: [192.168.121.209] => (item={'name': 'aturing', 'groups': ['tape'], 'gecos': 'Alan Turing'})
changed: [192.168.121.209] => (item={'name': 'edijkstra', 'groups': ['tcdump'], 'gecos': 'Edsger Dijkstra'})
changed: [192.168.121.209] => (item={'name': 'ghopper', 'groups': ['wheel', 'audio'], 'gecos': 'Grace Hopper'})

PLAY RECAP *****************************************************************************************************************************
192.168.121.209            : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

[deploy@webserver ~]$ getent passwd alovelace
alovelace:x:1002:1003:Ada Lovelace:/home/alovelace:/bin/bash

# Resources and Documentation

* [loops](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_loops.html)
* [ansible.builtin.user](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/user_module.html)
* [ansible.builtin.fileglob](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/fileglob_lookup.html)
* https://docs.ansible.com/ansible/latest/reference_appendices/faq.html#how-do-i-generate-encrypted-passwords-for-the-user-module

