# Examination 7 - MariaDB installation

To make a dynamic web site, many use an SQL server to store the data for the web site.

[MariaDB](https://mariadb.org/) is an open-source relational SQL database that is good
to use for our purposes.

We can use a similar strategy as with the _nginx_ web server to install this
software onto the correct host(s). Create the playbook `07-mariadb.yml` with this content:

    ---
    - hosts: db
      become: true
      tasks:
        - name: Ensure MariaDB-server is installed.
          ansible.builtin.package:
            name: mariadb-server
            state: present

# QUESTION A

Make similar changes to this playbook that we did for the _nginx_ server, so that
the `mariadb` service starts automatically at boot, and is started when the playbook
is run.


# QUESTION B

When you have run the playbook above successfully, how can you verify that the `mariadb`
service is started and is running?
### Answer
administrator@administrator-Precision-T1650:~/Desktop/AnsibleWorkbook$ ansible-playbook 07-mariadb-checkstatus.yml 

PLAY [Check Mariadb status] ************************************************************************************************************

TASK [Gathering Facts] *****************************************************************************************************************
ok: [192.168.121.142]

TASK [Gather service facts] ************************************************************************************************************
ok: [192.168.121.142]

TASK [Show mariadb status] *************************************************************************************************************
ok: [192.168.121.142] => {
    "ansible_facts.services['mariadb.service']": {
        "name": "mariadb.service",
        "source": "systemd",
        "state": "running",
        "status": "enabled"
    }
}

PLAY RECAP *****************************************************************************************************************************
192.168.121.142            : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

I created a new Ansible playbook that uses the service_facts module to gather info about running services and then i used a debug task to check mariadb.service .Thid wsy I was able to verify that mariadb running without having to log into the DB server manually via terminal.
# BONUS QUESTION

How many different ways can use come up with to verify that the `mariadb` service is running?

### Answer

More than two. 
1.By using Ansible playbook with service_facts as I did to check the service status
2.By connecting to the server via SSH and running systemctl status mariadb 
3.By looking for mysqld process running commando ps aux
4.By checking mariadb log files 
5.By checking if port 3306 (mariadb uses this port) is open with netstat.

Even though options 2,3 and 5 ar enormally run directly in the terminal we can also be executed through Ansible tasks using  ansible.builtin.shell.
