# Examination 5 - Handling Configuration Changes

Today, plain HTTP is considered insecure. Most public facing web sites use the encrypted HTTPS
protocol.

In order to set up our web server to use HTTPS, we need to make a configuration change in nginx.

## Preparations

Begin by running the [install-cert.yml](install-cert.yml) playbook to generate a self-signed certificate
in the correct location on the webserver.
### Answer
I did a file install-cert and I ran the playbook

administrator@administrator-Precision-T1650:~/Desktop/AnsibleWorkbook$ ansible-playbook install-cert.yml 

PLAY [Set up self-signed certificates for HTTPS] ***************************************************************************************

TASK [Gathering Facts] *****************************************************************************************************************
ok: [192.168.121.209]

TASK [Ensure the /etc/pki/nginx directory exists] **************************************************************************************
changed: [192.168.121.209]

TASK [Ensure we have a /etc/pkig/nginx/private directory] ******************************************************************************
changed: [192.168.121.209]

TASK [Ensure we have necessary software installed] *************************************************************************************
changed: [192.168.121.209]

TASK [Ensure we have a private key for our certificate] ********************************************************************************
changed: [192.168.121.209]

TASK [Create a self-signed certificate] ************************************************************************************************
changed: [192.168.121.209]

PLAY RECAP *****************************************************************************************************************************
192.168.121.209            : ok=6    changed=5    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   


You may need to install the Ansible `community.crypto` collection first, unless you have
already done so earlier.

In the `lab_environment` folder, there is a file called `requirements.yml` that can be used like this:

    $ ansible-galaxy collection install -r requirements.yml

Or, if you prefer, you can install the collection directly with

    $ ansible-galaxy collection install community.crypto

# HTTPS configuration in nginx

The default nginx configuration file suggests something like the following to be added to its
configuration:

    server {
        listen       443 ssl;
        http2        on;
        server_name  _;
        root         /usr/share/nginx/html;

        ssl_certificate "/etc/pki/nginx/server.crt";
        ssl_certificate_key "/etc/pki/nginx/private/server.key";
        ssl_session_cache shared:SSL:1m;
        ssl_session_timeout  10m;
        ssl_ciphers PROFILE=SYSTEM;
        ssl_prefer_server_ciphers on;

        # Load configuration files for the default server block.
        include /etc/nginx/default.d/*.conf;
    }

*IMPORTANT*: If you happen to run an earlier version of
`nginx`, such as one in AlmaLinux9, it will not recognize
the "http2" directive. You can simply comment it out with
a `#`, or remove the line completely.

There are many ways to get this configuration into nginx, but we are going to copy
this as a file into `/etc/nginx/conf.d/https.conf` with Ansible with the
[ansible.builtin.copy](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/copy_module.html)
module.

If you have gone through the preparation part for this examinination, the certificate and the key for the
certificate has already been created so we don't need to worry about that.

In this directory, there is already a file called `files/https.conf`. Copy this directory to your Ansible
working directory, with the contents intact.

Now, we will create an Ansible playbook that copies this file via the `ansible.builtin.copy` module
to `/etc/nginx/conf.d/https.conf`.

# QUESTION A

Create a playbook, `05-web.yml` that copies the local `files/https.conf` file to `/etc/nginx/conf.d/https.conf`,
and acts ONLY on the `web` group from the inventory.

Refer to the official Ansible documentation for this, or work with a classmate to
build a valid and working playbook, preferrably that conforms to Ansible best practices.
 
Run the playbook with `ansible-playbook` and `--verbose` or `-v` as option:

    $ ansible-playbook -v 05-web.yml

### Answer
administrator@administrator-Precision-T1650:~/Desktop/AnsibleWorkbook$ ansible-playbook -v 05-web.yml
Using /home/administrator/Desktop/AnsibleWorkbook/ansible.cfg as config file

PLAY [HTTPS configuration in nginx] ****************************************************************************************************

TASK [Gathering Facts] *****************************************************************************************************************
ok: [192.168.121.209]

TASK [copy a path to the webserver] ****************************************************************************************************
changed: [192.168.121.209] => {"changed": true, "checksum": "6b7873c361aae1ca7921740ed7d6118c1046d84a", "dest": "/etc/nginx/conf.d/https.conf", "gid": 0, "group": "root", "md5sum": "f313640b42d6b9d97e1d496bb82fac6d", "mode": "0644", "owner": "root", "secontext": "system_u:object_r:httpd_config_t:s0", "size": 465, "src": "/home/deploy/.ansible/tmp/ansible-tmp-1761211273.294847-35983-46109165243569/source", "state": "file", "uid": 0}

PLAY RECAP *****************************************************************************************************************************
192.168.121.209            : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0 

[deploy@webserver ~]$ ls -l /etc/nginx/conf.d/
total 4
-rw-r--r--. 1 root root 465 Oct 23 09:21 https.conf
[deploy@webserver ~]$ 

The output from the playbook run contains something that looks suspiciously like JSON, and that contains
a number of keys and values that come from the output of the Ansible module.

What does the output look like the first time you run this playbook?
### Answer
changed: [192.168.121.209] => {"changed": true, "checksum": "6b7873c361aae1ca7921740ed7d6118c1046d84a", "dest": "/etc/nginx/conf.d/https.conf", "gid": 0, "group": "root", "md5sum": "f313640b42d6b9d97e1d496bb82fac6d", "mode": "0644", "owner": "root", "secontext": "system_u:object_r:httpd_config_t:s0", "size": 465, "src": "/home/deploy/.ansible/tmp/ansible-tmp-1761211273.294847-35983-46109165243569/source", "state": "file", "uid": 0}

What does the output look like the second time you run this playbook?
### Answer
ASK [copy a path to the webserver] ****************************************************************************************************
ok: [192.168.121.209] => {"changed": false, "checksum": "6b7873c361aae1ca7921740ed7d6118c1046d84a", "dest": "/etc/nginx/conf.d/https.conf", "gid": 0, "group": "root", "mode": "0644", "owner": "root", "path": "/etc/nginx/conf.d/https.conf", "secontext": "system_u:object_r:httpd_config_t:s0", "size": 465, "state": "file", "uid": 0}
in green color

The second time, the output says "changed": false which means the file already existed and had the same content so Ansible did not copy it again.
# QUESTION B

Even if we have copied the configuration to the right place, we still do not have a working https service
on port 443 on the machine, which is painfully obvious if we try connecting to this port:

    $ curl -v https://192.168.121.10
    *   Trying 192.168.121.10:443...
    * connect to 192.168.121.10 port 443 from 192.168.121.1 port 56682 failed: Connection refused
    * Failed to connect to 192.168.121.10 port 443 after 0 ms: Could not connect to server
    * closing connection #0
    curl: (7) Failed to connect to 192.168.121.10 port 443 after 0 ms: Could not connect to server

The address above is just an example, and is likely different on your machine. Make sure you use the IP address
of the webserver VM on YOUR machine.
### Answer

administrator@administrator-Precision-T1650:~/Desktop/AnsibleWorkbook$ curl -v https://192.168.121.209
*   Trying 192.168.121.209:443...
* connect to 192.168.121.209 port 443 from 192.168.121.1 port 40264 failed: Connection refused
* Failed to connect to 192.168.121.209 port 443 after 0 ms: Couldn't connect to server
* Closing connection
curl: (7) Failed to connect to 192.168.121.209 port 443 after 0 ms: Couldn't connect to server

In order to make `nginx` use the new configuration by restarting the service and letting `nginx` re-read
its configuration.

On the machine itself we can do this by:

    [deploy@webserver ~]$ sudo systemctl restart nginx.service

Given what we know about the [ansible.builtin.service](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/service_module.html),
how can we do this through Ansible?

### Answer
We can add an extra task after the conf file is copied using the ansible.builtin.service module with state: restarted, to restart nginx and load the new HTTPS settigns.

Add an extra task to the `05-web.yml` playbook to ensure the service is restarted after the configuration
file is installed.

When you are done, verify that `nginx` serves web pages on both TCP/80 (http) and TCP/443 (https):

    $ curl http://192.168.121.10
    $ curl --insecure https://192.168.121.10

Again, these addresses are just examples, make sure you use the IP of the actual webserver VM.

Note also that `curl` needs the `--insecure` option to establish a connection to a HTTPS server with
a self signed certificate.

# QUESTION C

What is the disadvantage of having a task that _always_ makes sure a service is restarted, even if there is
no configuration change?

### Answer
It can cause unnecessary downtime and interrupt users connections and waste system resources. It is not idempotent as well.

# BONUS QUESTION

There are at least two _other_ modules, in addition to the `ansible.builtin.service` module that can restart
a `systemd` service with Ansible. Which modules are they?

### Answer

Ansible.builtin.systemd , use a command like ansible.builtin.command: systemctl restart nginx , We can also use handlers.
