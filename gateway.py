import database 
import easysap
import base64


#---------------------------------------------------------------------#
# Interacciones con la base de datos                                  #
#---------------------------------------------------------------------#

def getServers():
    servers_data = database.executeQuery(""" SELECT * FROM Server """)
    servers = []
    for server in servers_data:
        servers.append(server)  
    return servers 


def get_single_RFC(id):
	sql = "SELECT * FROM RFCs WHERE id = '%s' "	 % id 

	rfcs_data = database.executeQuery(sql)
	rfcs = []

	for rfc in rfcs_data:
		rfcs.append(rfc)

	return rfcs	


def get_active_RFCs():
	sql = "SELECT * FROM RFCs WHERE status = '1'"
	rfcs_data = database.executeQuery(sql)

	rfcs = []
	for rfc in rfcs_data:
		rfcs.append(rfc)

	return rfcs	

def update_rfc_status(rfc_id, status):
	sql = "UPDATE RFCs SET status = '%s' WHERE id='%s' " % (status, rfc_id) 

	print sql	
	database.executeQuery(sql, q='I' )
	
	 	
	

def getRFCs():
    rfcs_data = database.executeQuery(""" SELECT * FROM RFCs """)
    rfcs = []
    for rfc in rfcs_data:
        rfcs.append(rfc)
    return rfcs
    
def getSingleRFC(id):
    rfcs_data = database.executeQuery(" SELECT * FROM RFCs WHERE id = '"+id+"'")
    rfcs = []
    for rfc in rfcs_data:
        rfcs.append(rfc)
    return rfcs[0]


def existsRFCinDB(rfc_name):
	rfc = database.executeQuery(" SELECT * FROM RFCs WHERE name = '%s'" % rfc_name ) 
	rfcs = []
	for r in rfc:
		rfcs.append(rfc)
		
	if len(rfcs) >= 1:
		return True 
	else:
		return False 
		
				   

def isConnected():
    exists = database.checkDatabase()
    if exists:
        servers = getServers()
        if len(servers)>0:
            return True
    else:
        return False


def insert_config(name, ip, sysnr, client, user, passwd):
	passwd.strip()
	passwd = base64.encodestring(passwd)

	sql = "INSERT INTO Server(name, ip, sysnr, client, user, passwd) VALUES('%s', '%s', '%s', '%s', '%s', '%s')" % (name, ip, sysnr, client, user, passwd)

	r = database.executeQuery(sql, q= 'I')

def insert_rfc(rfc_name):
	rfcs = getRFCs()
	last_id = len(rfcs) + 1
	sql = "INSERT INTO RFCs(id, name, status) VALUES('%s', '%s', '%s');" % (str(last_id), rfc_name, '0')
	
	r = database.executeQuery(sql, q= 'I')
		

def get_connstring():
	sql = "SELECT * FROM Server"	
	result = database.executeQuery(sql)
	servers =[]
	for r in result:
		datos = r
		break
	
	ip     = datos[1]
	sysnr  = datos[2]	
	client = datos[3] 
	user   = datos[4]
	passwd = base64.decodestring(datos[5])
	
	conn = easysap.getConnString(ip, sysnr, client, user, passwd) 
	
	return conn 
	
#------------------------------------------------------------------#
#	Interacciones con SAP                                          #
#------------------------------------------------------------------#	

def existsRFCinSAP(rfc_name):
	conn = get_connstring()
	try:
		rfc = easysap.RFC(rfc_name, conn)
	except:
		print 'Ocurrio un error al tratar de conectarse con la RFC, verifique configuracion de servidor y si la RFC realmente existe'
	else:
		return True	
			

def getRFCObject(rfc_name):
	rfc_name = rfc_name.decode('latin-1').encode('utf-7')
	conn = get_connstring()
	rfc = easysap.RFC(rfc_name, conn)
	return rfc 			


def getTableDefinition(tab_name):
	conn = get_connstring()
	definition = easysap.get_table_fields(tab_name, conn)
	return definition







