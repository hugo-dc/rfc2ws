import getpass
import gateway
import subprocess 
import os


ws_server_pid = None

# Web Services Server 
def stop_ws_server():
	print 'Stopping Web Server...   [', ws_server_pid, ']'
	if ws_server_pid != None:
		os.system('taskkill /F 	/PID ' + str(ws_server_pid))
		print 'Server stopped.'
	else:
		print 'Server was not running.'	

def start_ws_server():		
	print 'Starting Web Server...',
	global ws_server_pid
	ws_server_pid = subprocess.Popen(r'Python ws_server.py').pid
	print '[',ws_server_pid , ']'


def restart_ws_server():
	stop_ws_server()
	start_ws_server()

# Commands 
#--
def start_ws():
	show_services()
	
	wsid = raw_input('\n\nId: ')
	
	rfc = gateway.get_single_RFC(wsid)
	
	if len(rfc) == 0:
		print '[Error] Wrong ID'			
		return False 

	gateway.update_rfc_status(wsid, '1')
	restart_ws_server()
	

# --
def show_services():
	status = { '0' : 'Not running',
			   '1' : 'Running'
	}

	services = gateway.getRFCs() 
	print """
+==============================================================	
| Services    \t\t|     Status  
+============================================================== """
	for service in services:
		print ' ', service[0] +':', service[1], '\t\t', status[service[2]]


#--		
def conf_sap_server():
	print """
New SAP Server configuration
============================
	"""

	name   = raw_input('Server name: ')
	ip     = raw_input('IP/Hostname: ')
	sysnr  = raw_input('System number: ')
	client = raw_input("Mandant: ")
	user   = raw_input('User: ')
	# passwd = raw_input('Password: ')
	passwd = getpass.getpass('Password: ')

	gateway.insert_config(name, ip, sysnr, client, user, passwd)



#--	
def new_ws():
	if not gateway.isConnected():
		print 'You must configure a SAP connection first, type `config` '
		return False

	print """
New Web Service
===============	
	"""

	rfc = raw_input('RFC Name: ')
	rfc = rfc.upper().strip()

	if gateway.existsRFCinDB(rfc):
		print 'RFC Existente en la base de datos'
		return False 
		
	if not 	 gateway.existsRFCinSAP(rfc):
		print 'RFC no existe en SAP'
		return False 

		
	gateway.insert_rfc(rfc)	

	print 'Se ha creado el servicio para la RFC'




#--
def exit():
	stop_ws_server()
	print 'Bye'
	return True 
	
	 


#--
def help_():
	print """
Available commands:
===================

	exit   - Exit 
	config - Configure SAP Connection 
	new    - Create a new Web Service	
	"""
	return False	

execute_command = {
	'config'   : conf_sap_server,
	'configure': conf_sap_server,
	'show'     : show_services,
	'start'    : start_ws,	
	'new'      : new_ws,
	'help'     : help_,
	'exit'     : exit,
	'quit'     : exit
	}


# Starts command line interface 
if __name__ == '__main__':
	print """
--------------------------------------------------------------	
rfc2ws v0.05 [2012] - @hugo_dc
==============================================================

Crea servicios webs a partir de RFCs.
Escribe `help` para ver la lista de comandos disponibles.

--------------------------------------------------------------
	"""

	exit = False 
	while(exit != True):
		command = raw_input('\n>>> ')
		command = command.replace(' ', '').lower()

		if command in execute_command.keys():
			exit = execute_command[command]()
		else:
			if len(command.strip()) > 1:		
				print "Command `"+command+"` not found"	


