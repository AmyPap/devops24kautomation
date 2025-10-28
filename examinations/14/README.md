# Examination 14 - Firewalls (VG)

The IT security team has noticed that we do not have any firewalls enabled on the servers,
and thus ITSEC surmises that the servers are vulnerable to intruders and malware.

As a first step to appeasing them, we will install and enable `firewalld` and
enable the services needed for connecting to the web server(s) and the database server(s).

# QUESTION A

Create a playbook `14-firewall.yml` that utilizes the [ansible.posix.firewalld](https://docs.ansible.com/ansible/latest/collections/ansible/posix/firewalld_module.html) module to enable the following services in firewalld:

* On the webserver(s), `http` and `https`
* On the database servers(s), the `mysql`

You will need to install `firewalld` and `python3-firewall`, and you will need to enable
the `firewalld` service and have it running on all servers.

When the playbook is run, you should be able to do the following on each of the
servers:

## dbserver

    [deploy@dbserver ~]$ sudo cat /etc/firewalld/zones/public.xml
    <?xml version="1.0" encoding="utf-8"?>
    <zone>
      <short>Public</short>
      <description>For use in public areas. You do not trust the other computers on networks to not harm your computer. Only selected incoming connections are accepted.</description>
      <service name="ssh"/>
      <service name="dhcpv6-client"/>
      <service name="cockpit"/>
      <service name="mysql"/>
    <forward/>
    </zone>

## webserver

    [deploy@webserver ~]$ sudo cat /etc/firewalld/zones/public.xml
    <?xml version="1.0" encoding="utf-8"?>
    <zone>
      <short>Public</short>
      <description>For use in public areas. You do not trust the other computers on networks to not harm your computer. Only selected incoming connections are accepted.</description>
      <service name="ssh"/>
      <service name="dhcpv6-client"/>
      <service name="cockpit"/>
      <service name="https"/>
      <service name="http"/>
      <forward/>
    </zone>

# Resources and Documentation

https://firewalld.org/


### Answer

administrator@administrator-Precision-T1650:~/Desktop/devops24kautomation/AnsibleWorkbook$ ansible-playbook 14-firewall.yml --vault-password-file 11-vault_passwd.txt 

PLAY [Configure the web server with firewall , webserver roles] ************************************************************************

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

TASK [webserver : Copy https config to nginx] ******************************************************************************************
ok: [192.168.121.209]

TASK [firewall : Ensure firewalld and dependencies are installed] **********************************************************************
ok: [192.168.121.209]

TASK [firewall : Enable and start firewalld] *******************************************************************************************
ok: [192.168.121.209]

TASK [firewall : Open firewall services  based on host group] **************************************************************************
changed: [192.168.121.209] => (item=http)
changed: [192.168.121.209] => (item=https)

PLAY [Configure the database server with firewall , dbserver roles] ********************************************************************

TASK [Gathering Facts] *****************************************************************************************************************
ok: [192.168.121.142]

TASK [dbserver : Ensure deploy's home directory exists] ********************************************************************************
ok: [192.168.121.142]

TASK [dbserver : Show found .md files] *************************************************************************************************
ok: [192.168.121.142] => (item=/home/administrator/Desktop/devops24kautomation/AnsibleWorkbook/files/baz.md) => {
    "ansible_loop_var": "item",
    "item": "/home/administrator/Desktop/devops24kautomation/AnsibleWorkbook/files/baz.md"
}
ok: [192.168.121.142] => (item=/home/administrator/Desktop/devops24kautomation/AnsibleWorkbook/files/bar.md) => {
    "ansible_loop_var": "item",
    "item": "/home/administrator/Desktop/devops24kautomation/AnsibleWorkbook/files/bar.md"
}
ok: [192.168.121.142] => (item=/home/administrator/Desktop/devops24kautomation/AnsibleWorkbook/files/foo.md) => {
    "ansible_loop_var": "item",
    "item": "/home/administrator/Desktop/devops24kautomation/AnsibleWorkbook/files/foo.md"
}

TASK [dbserver : Copy .md files to deploy's home directory] ****************************************************************************
ok: [192.168.121.142] => (item=/home/administrator/Desktop/devops24kautomation/AnsibleWorkbook/files/baz.md)
ok: [192.168.121.142] => (item=/home/administrator/Desktop/devops24kautomation/AnsibleWorkbook/files/bar.md)
ok: [192.168.121.142] => (item=/home/administrator/Desktop/devops24kautomation/AnsibleWorkbook/files/foo.md)

TASK [firewall : Ensure firewalld and dependencies are installed] **********************************************************************
changed: [192.168.121.142]

TASK [firewall : Enable and start firewalld] *******************************************************************************************
changed: [192.168.121.142]

TASK [firewall : Open firewall services  based on host group] **************************************************************************
changed: [192.168.121.142] => (item=mysql)

PLAY RECAP *****************************************************************************************************************************
192.168.121.142            : ok=7    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
192.168.121.209            : ok=7    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0  

### Check
[deploy@webserver ~]$ sudo cat /etc/firewalld/zones/public.xml
<?xml version="1.0" encoding="utf-8"?>
<zone>
  <short>Public</short>
  <description>For use in public areas. You do not trust the other computers on networks to not harm your computer. Only selected incoming connections are accepted.</description>
  <service name="ssh"/>
  <service name="dhcpv6-client"/>
  <service name="cockpit"/>
  <service name="http"/>
  <service name="https"/>
  <forward/>
</zone>
[deploy@webserver ~]$ ssh deploy@192.168.121.142 "sudo cat /etc/firewalld/zones/public.xml"
<?xml version="1.0" encoding="utf-8"?>
<zone>
  <short>Public</short>
  <description>For use in public areas. You do not trust the other computers on networks to not harm your computer. Only selected incoming connections are accepted.</description>
  <service name="ssh"/>
  <service name="dhcpv6-client"/>
  <service name="cockpit"/>
  <service name="mysql"/>
  <forward/>
</zone>
[deploy@webserver ~]$ 
