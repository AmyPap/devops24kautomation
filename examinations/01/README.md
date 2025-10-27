# Examination 1 - Understanding SSH and public key authentication

Connect to one of the virtual lab machines through SSH, i.e.

    $ ssh -i deploy_key -l deploy webserver

Study the `.ssh` folder in the home directory of the `deploy` user:

    $ ls -ld ~/.ssh

Look at the contents of the `~/.ssh` directory:

    $ ls -la ~/.ssh/

## QUESTION A

What are the permissions of the `~/.ssh` directory?
### Answer
The permissions are 
``` ini
drwx------ deploy deploy 
```
This means only the owner **deploy** has full read,write and execute permissions (700) while the group and all others users have no permissions at all.


Why are the permissions set in such a way?
### Answer
For security reasons. The directory contains the authentication keys that let us log in without a password. If anyone else could access the directory, SSH would consider it unsafe and would block the login because the SSH system insists on these strict permissions (700 on the directory).

## QUESTION B

What does the file `~/.ssh/authorized_keys` contain?
### Answer
The file contains the Public key that matches the private login key **deploy_key**. This is a trusted list. If a client connects with a private key that matches the public key in this file the client can log in as *deploy* without needing a password.

## QUESTION C

When logged into one of the VMs, how can you connect to the
other VM without a password?
### Answer
To connect from the **webserver** to the **dbserver** without a password, i created a new key pair on the **webserver** and copied its public key to the **dbserver's** trusted list *authourized_keys*.
 
```bash
ssh-keygen -t rsa
cat ~/.ssh/id_rsa.pub | ssh -i /vagrant/deploy_key deploy@192.168.121.142 'cat >> ~/.ssh/authorized_keys'
ssh deploy@dbserver
```
The connection worked instantly.


### Hints:

* man ssh-keygen(1)
* ssh-copy-id(1) or use a text editor

## BONUS QUESTION

Can you run a command on a remote host via SSH? How?
### Answer
Yes, I run a command on the remote host **dbserver** from **webserver** using SSH. I used the command
```bash
ssh deploy@dbserver "pwd"
```
But this is a non-interactive connection. The SSH client **webserver** connects, run only the specific command (pwd for example), sends the result back to webserver's terminal and immediately disconnects. It's faster and doesn't require opening a full session.