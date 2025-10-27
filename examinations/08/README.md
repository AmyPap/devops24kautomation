# Examination 8 - MariaDB configuration

MariaDB and MySQL have the same origin (MariaDB is a fork of MySQL, because of... Oracle...
it's a long story.) They both work the same way, which makes it possible to use Ansible
collections that handle `mysql` to work with `mariadb`.

To be able to manage MariaDB/MySQL through the `community.mysql` collection, you also
need to make sure the requirements for the collections are installed on the database VM.

See https://docs.ansible.com/ansible/latest/collections/community/mysql/mysql_db_module.html#ansible-collections-community-mysql-mysql-db-module-requirements

HINT: In AlmaLinux, the correct package to install on the VM host is called `python3-PyMySQL`.

### Answer

administrator@administrator-Precision-T1650:~/Desktop/AnsibleWorkbook$ ansible-playbook 08-mariadb-config.yml 

PLAY [db] ******************************************************************************************************************************

TASK [Gathering Facts] *****************************************************************************************************************
ok: [192.168.121.142]

TASK [Ensure MariaDB-server is installed.] *********************************************************************************************
ok: [192.168.121.142]

TASK [Ensure PyMySQL is installed] *****************************************************************************************************
changed: [192.168.121.142]

TASK [Ensure MariaDB is started and enabled] *******************************************************************************************
ok: [192.168.121.142]

PLAY RECAP *****************************************************************************************************************************
192.168.121.142            : ok=4    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

# QUESTION A

Copy the playbook from examination 7 to `08-mariadb-config.yml`.

Use the `community.mysql` module in this playbook so that it also creates a database instance
called `webappdb` and a database user called `webappuser`.

Make the `webappuser` have the password "secretpassword" to access the database.

HINT: The `community.mysql` collection modules has many different ways to authenticate
users to the MariaDB/MySQL instance. Since we've just installed `mariadb` without setting
any root password, or securing the server in other ways, we can use the UNIX socket
to authenticate as root:

* The socket is located in `/var/lib/mysql/mysql.sock`
* Since we're authenticating through a socket, we should ignore the requirement for a `~/.my.cnf` file.
* For simplicity's sake, let's grant `ALL` privileges on `webapp.*` to `webappuser` 

# Documentation and Examples
https://docs.ansible.com/ansible/latest/collections/community/mysql/index.html


### Answer

administrator@administrator-Precision-T1650:~/Desktop/AnsibleWorkbook$ ansible-playbook 08-mariadb-config.yml 

PLAY [db] ******************************************************************************************************************************

TASK [Gathering Facts] *****************************************************************************************************************
ok: [192.168.121.142]

TASK [Ensure MariaDB-server is installed.] *********************************************************************************************
ok: [192.168.121.142]

TASK [Ensure PyMySQL is installed] *****************************************************************************************************
ok: [192.168.121.142]

TASK [Ensure MariaDB is started and enabled] *******************************************************************************************
ok: [192.168.121.142]

TASK [Create webappdb database] ********************************************************************************************************
ok: [192.168.121.142]

TASK [Create webappuser with full access to webappdb] **********************************************************************************
[WARNING]: Option column_case_sensitive is not provided. The default is now false, so the column's name will be uppercased. The default
will be changed to true in community.mysql 4.0.0.
changed: [192.168.121.142]

PLAY RECAP *****************************************************************************************************************************
192.168.121.142            : ok=6    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0  


### Check

administrator@administrator-Precision-T1650:~/Desktop/AnsibleWorkbook$ ansible-playbook 08-mariadb-checkstatus.yml 

PLAY [Check database and user] *********************************************************************************************************

TASK [Gathering Facts] *****************************************************************************************************************
ok: [192.168.121.142]

TASK [Check if webappuser exists] ******************************************************************************************************
ok: [192.168.121.142]

TASK [Show user query result] **********************************************************************************************************
ok: [192.168.121.142] => {
    "user_info": {
        "changed": false,
        "executed_queries": [
            "SELECT User, Host FROM mysql.user WHERE User='webappuser';"
        ],
        "failed": false,
        "query_result": [
            [
                {
                    "Host": "localhost",
                    "User": "webappuser"
                }
            ]
        ],
        "rowcount": [
            1
        ]
    }
}

TASK [Check if webappdb database exists] ***********************************************************************************************
ok: [192.168.121.142]

TASK [Print result] ********************************************************************************************************************
ok: [192.168.121.142] => {
    "db_info": {
        "changed": false,
        "executed_queries": [
            "SHOW DATABASES;"
        ],
        "failed": false,
        "query_result": [
            [
                {
                    "Database": "information_schema"
                },
                {
                    "Database": "webappdb"
                }
            ]
        ],
        "rowcount": [
            2
        ]
    }
}

PLAY RECAP *****************************************************************************************************************************
192.168.121.142            : ok=5    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0 