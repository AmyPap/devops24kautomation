# Examination 10 - Templating

With the installation of the web server earlier in Examination 6, we set up
the `nginx` web server with a static configuration file that listened to all
interfaces on the (virtual) machine.

What we really want is for the webserver to _only_ listen to the external
interface, i.e. the interface with the IP address that we connect to the machine to.

Of course, we can statically enter the IP address into the file and upload it,
but if the IP address of the machine changes, we have to do it again, and if the
playbook is meant to be run against many different web servers, we have to be able
to do this manually.

Make a directory called `templates/` and put the `nginx` configuration file from Examination 6
into that directory, and call it `example.internal.conf.j2`.

If you look at the `nginx` documentation, note that you don't have to enable any IPv6 interfaces
on the web server. Stick to IPv4 for now.

# QUESTION A

Copy the finished playbook from Examination 6 (`06-web.yml`) and call it `10-web-template.yml`.

Make the static configuration file we used earlier into a Jinja template file,
and set the values for the `listen` parameters to include the external IP
address of the virtual machine itself.

Use the `ansible.builtin.template` module to accomplish this task.

# Resources and Documentation

* https://docs.ansible.com/ansible/latest/collections/ansible/builtin/template_module.html
* https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html
* https://nginx.org/en/docs/http/ngx_http_core_module.html#listen

### Answer

I did all the steps and then inside the template , I added the variable {{ ansible_default_ipv4.address }}. I also updated the playbook to use the ansible.builtin.template module instead of copy.

I check if it works

administrator@administrator-Precision-T1650:~/Desktop/AnsibleWorkbook$ ansible-playbook 10-web-template-check.yml 

PLAY [Check IPs] ***********************************************************************************************************************

TASK [Gathering Facts] *****************************************************************************************************************
ok: [192.168.121.209]

TASK [Show generated nginx conf] *******************************************************************************************************
changed: [192.168.121.209]

TASK [Print nginx conf] ****************************************************************************************************************
ok: [192.168.121.209] => {
    "nginx_conf.stdout": "server {\n    listen 192.168.121.209:80;\n    listen 192.168.121.209:443 ssl;\n    root /var/www/example.internal/html;\n    index index.html;\n    server_name example.internal;\n\n    ssl_certificate \"/etc/pki/nginx/server.crt\";\n    ssl_certificate_key \"/etc/pki/nginx/private/server.key\";\n    ssl_session_cache shared:SSL:1m;\n    ssl_session_timeout  10m;\n    ssl_ciphers PROFILE=SYSTEM;\n    ssl_prefer_server_ciphers on;\n\n    location / {\n        try_files $uri $uri/ =404;\n    }\n}"
}

PLAY RECAP *****************************************************************************************************************************
192.168.121.209            : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0  