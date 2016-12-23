#!/usr/bin/env python

import subprocess
import datetime
import threading
import time

list_process_ids = []
list_process_names = []
list_valid_processes = ['backtype.storm.ui.core',
			'backtype.storm.daemon.nimbus',
			'org.apache.zookeeper.server.quorum.QuorumPeerMain',
			'backtype.storm.daemon.worker',
			'backtype.storm.daemon.supervisor']
now = datetime.datetime.now()
file_name_const = str(now.year) + '-'   + str(now.month) + '-' + str(now.day) + '_' + str(now.hour) + '-' + str(now.minute) + '_'

def main():
	from subprocess import call
	global list_process_ids
	print ('================================================================================================')
	print ('Diagnostic Command Requests with jcmd Utility')
	print ('================================================================================================')
	p = subprocess.Popen(['jcmd'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	jcmd_out, err = p.communicate()
	filter_jcmd_processes(jcmd_out)
	threading.Thread(target=profile).start()
	print ('================================================================================================')

def filter_jcmd_processes(jcmd_out):
	global list_process_ids
	list_lines = (str(jcmd_out)).split('\n')
	print ('Number of running processes = ' + str(len(list_lines) - 1) + '\n')
	count = 0 
	for line in list_lines:
		count = count + 1
		if(count < len(list_lines)):
			get_process_id(line)

def get_process_id(line):
	global list_process_ids
	global list_process_names
	global list_valid_processes
	list_elements = (str(line)).split(' ')
	count = 0	
	print (list_elements[0] + '\t' + list_elements[1])
	if(list_elements[1] in list_valid_processes):
		list_process_ids.append(list_elements[0])
		list_process_names.append(list_elements[1])

def profile():
	from subprocess import call
	global list_process_ids
	global list_process_names
	global file_name_const
	for i in range(0, len(list_process_ids)):
		file_name = 'filename=/home/ubuntu/eranga/developments/Dev10-storm-0.x.x/jfr/' + file_name_const + "-test1-" + str(i + 1) + '-' + list_process_names[i] + '.jfr'
        	call(['jcmd', list_process_ids[i], 'VM.unlock_commercial_features'])
        	call(['jcmd', list_process_ids[i], 'JFR.start duration=180s', file_name])
        	print (file_name)
		time.sleep(.5)

main()