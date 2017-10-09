import subprocess
import re
import os
import time
import sh
import time
from docker_digitalocean_db import *

ssh_con_str = "root@67.205.147.105"

print "NOTICE: this script has to be run as a user with access to SSH keys."
print "Deployment to remote server (" + ssh_con_str + ") started."

ssh = sh.ssh.bake('-oStrictHostKeyChecking=no', ssh_con_str)

print "Successfully connected to remote server."

kill_and_remove_all_containers(ssh, 'biketimer-web-db')

cassandra_container_id = start_cassandra_container(ssh)
print "Wait for cassandra to warm up."
time.sleep(20) # wait for cassandra to init.

print "Setup cassandra schema."
copy_cassandra_scripts_to_remote_host(cassandra_container_id, ssh_con_str)
copy_cassandra_scripts_to_docker_container(ssh, cassandra_container_id)
run_cassandra_migration_scripts_in_docker_container(ssh, cassandra_container_id)

