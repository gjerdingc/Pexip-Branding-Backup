from fabric.api import *
from fabric.contrib.files import exists
import time
import json
import os


USER = 'INSERT USERNAME'
PASSWORD = 'INSERT PASSWORD'
localfolder = '/home/hcsadmin/bin/flask/bbscript_new/Backups/'

def list_servers(server_ip):
    # `warn_only` if set to true will make sure your whole module does not error 
    # out inside the with block
    # in `host_string` you can pass user@hostname as well instead of including
    # the `user` argument
    with settings(warn_only='true', host_string=server_ip, user=USER,
                  password=PASSWORD, connection_attempts=5, keepalive=10,
                  timeout=15):
        output = run("hostname")
        return output

def getbrandingbackup(node):
	if("nor-pxcm" in node["name"]):
		node["downloadstatus"] = "This is a media load node. It has no branding"
		return node["downloadstatus"]
	else:
		with settings(warn_only='true', host_string=node["address"], user=USER,password=PASSWORD, connection_attempts=5, keepalive=10, timeout=15):
			try:
				if exists('/opt/pexip/share/web/static/app/configuration/themes'):
					get(remote_path="/opt/pexip/share/web/static/app/configuration", local_path=localfolder +  node["alternative_fqdn"])
					
					node["downloadstatus"] = "OK"
					
				else:
					node["downloadstatus"] = "Empty folder on node "

			except Exception as e:
				node["downloadstatus"] = str(e)
					
		return node["downloadstatus"]

def putbrandingbackup(node):
	if("nor-pxcm" in node["name"]):
		node["uploadstatus"] = "This is a media load node. It has no branding"
		return node["uploadstatus"]
	else:
		try:
			with settings(warn_only='true', host_string=node["address"], user=USER, password=PASSWORD, connection_attempts=5, keepalive=10,timeout=15):
				if os.path.exists(localfolder + node["alternative_fqdn"] + '/configuration/'):
					sudo("chown -R admin:admin /opt/pexip/share/web/static/app/configuration/")
					put(remote_path="/opt/pexip/share/web/static/app/", local_path=localfolder +  node["alternative_fqdn"] + '/configuration/')
					node["uploadstatus"] = "OK"
				else:
					node["uploadstatus"] = "Backupfolder missing"

		except Exception as e:
			node["uploadstatus"] = str(e)
		
	return node["uploadstatus"]

