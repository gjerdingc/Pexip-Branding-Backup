from fabric_tasks import getbrandingbackup, putbrandingbackup
from flask import Flask, jsonify, render_template, redirect
import csv
import requests
import json
import glob
import os
import time


app = Flask(__name__)


#Pexip admin user for API
username = 'INSERT USERNAME'
password = 'INSERT PASSWORD'

lastRunStatus = {"upload": "", "download": ""}

localfolder = '/home/hcsadmin/bin/flask/bbscript_new/'



@app.route('/')
def brandingbackup():
	
	list_of_logs = glob.glob(localfolder + 'logs/*')
	latest_log = max(list_of_logs, key=os.path.getctime)


	with open(latest_log) as json_log:
		d = json.load(json_log)
		json_log.close()
	
	with open(localfolder + "logs/lastrunstatus") as lastRunStatus:
		runStatus = json.load(lastRunStatus)
		lastRunStatus.close()
	
	return render_template("display_nodelist.html",
	backupStatusList=d,
	lastDownloadDate=runStatus["download"],
	lastUploadDate=runStatus["upload"],
	numberOfNodes=len(d))

@app.route('/brandingupload', methods=['POST', 'GET'])
def uploadbranding():
#Denne funksjonen brukes av fabric_tasks når noen trykker på "Upload branding"

	#refreshe listen over nodes
	response = requests.get("https://nor-pxmn1.atea-gcs.net/api/admin/configuration/v1/worker_vm/" + "?limit=200&offset=0",
	auth=(username, password), verify=False)
	nodeStatusObject = json.loads(response.text)
	nodeStatusList = nodeStatusObject["objects"]

	for node in nodeStatusList:
		node["uploadstatus"] = ""
		try:
			node["uploadstatus"] = putbrandingbackup(node)
		except Exception as e:
			node["uploadstatus"] = str(e)
			
		if node["uploadstatus"] == "" and node["alternative_fqdn"] == "":
			node["uploadstatus"] = node["name"] + ' has no FQDN'


	with open(localfolder + "logs/lastrunstatus", "r") as lastRun:
		lastRunStatus = json.load(lastRun)
		lastRun.close()
	
	lastRunStatus["upload"] = time.strftime("%Y-%m-%d")
	
	#This is the logfile for showing when upload and download script was last run
	with open(localfolder + "logs/lastrunstatus", "w+") as lastRun:
		lastRun.write(json.dumps(lastRunStatus, indent=4))

	with open(localfolder + "logs/logfile" + ' ' + time.strftime("%Y-%m-%d"),"w+") as logfile:
		logfile.write(json.dumps(nodeStatusList, indent=4))
		

	return redirect('/')


@app.route('/brandingdownload', methods=['POST' ,'GET'])
#Denne funksjonen brukes av fabric_tasks når noen trykker på "Download branding"
def server_list_users():

	#refreshe listen over nodes
	response = requests.get("https://nor-pxmn1.atea-gcs.net/api/admin/configuration/v1/worker_vm/" + "?limit=200&offset=0",
	auth=(username, password), verify=False)
	nodeStatusObject = json.loads(response.text)
	nodeStatusList = nodeStatusObject["objects"]

	for node in nodeStatusList:
		node["downloadstatus"] = ""
		try:
			node["downloadstatus"] = getbrandingbackup(node)
		except Exception as e:
			node["downloadstatus"] = str(e)
			
		if node["downloadstatus"] == "" and node["alternative_fqdn"] == "":
			node["downloadstatus"] = node["name"] + ' has no FQDN'
			
	
	with open(localfolder + "logs/lastrunstatus", "r") as lastRun:
		lastRunStatus = json.load(lastRun)
		lastRun.close()
	
	lastRunStatus["download"] = time.strftime("%Y-%m-%d")
	
	#This is the logfile for showing when upload and download script was last run
	with open(localfolder + "logs/lastrunstatus", "w+") as lastRun:
		lastRun.write(json.dumps(lastRunStatus, indent=4))
		
	#This is the logfile for showing individual node statuses	
	with open(localfolder + "logs/logfile" + ' ' + time.strftime("%Y-%m-%d"),"w+") as logfile:
		logfile.write(json.dumps(nodeStatusList, indent=4))
		
	return redirect("/")


