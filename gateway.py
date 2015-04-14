import database 
import easysap
import base64


#---------------------------------------------------------------------#
# DB Access
#---------------------------------------------------------------------#
def getServers():
    servers_data = database.executeQuery('s_server')
    servers = []
    for server in servers_data:
        servers.append(server)  
    return servers 


def get_single_RFC(id):
    sql = " "     % id 

    rfcs_data = database.executeQuery('s_rfcs_w_id', pars=(id))
    rfcs = []

    for rfc in rfcs_data:
        rfcs.append(rfc)

    return rfcs    


def get_active_RFCs():
    rfcs_data = database.executeQuery('s_rfc_w_s', pars=('1'))

    rfcs = []
    for rfc in rfcs_data:
        rfcs.append(rfc)

    return rfcs    

def update_rfc_status(rfc_id, status):
    database.executeQuery('u_rfcs_s_status_w_id', q='I', pars= (status, rfc_id))
    

def getRFCs():
    rfcs_data = database.executeQuery('s_rfcs')
    rfcs = []
    for rfc in rfcs_data:
        rfcs.append(rfc)
    return rfcs
    
def getSingleRFC(id):
    rfcs_data = database.executeQuery('s_rfcs_w_id', pars=(id))
    rfcs = []
    for rfc in rfcs_data:
        rfcs.append(rfc)
    return rfcs[0]


def existsRFCinDB(rfc_name):
    rfc = database.executeQuery('s_rfc_w_name', pars= (rfc_name) ) 
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
    r = database.executeQuery('i_server', q= 'I', pars=(name, ip, sysnr, client, user, passwd))

def insert_rfc(rfc_name):
    rfcs = getRFCs()
    last_id = len(rfcs) + 1

    r = database.executeQuery('i_rfcs', q= 'I', pars = (str(last_id), rfc_name, '0'))
        

def get_connstring():
    result = database.executeQuery('s_server')
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
#   Access to SAP
#------------------------------------------------------------------#    

def existsRFCinSAP(rfc_name):
    conn = get_connstring()
    try:
        rfc = easysap.RFC(rfc_name, conn)
    except:
        return None
        #print 'Ocurrio un error al tratar de conectarse con la RFC, verifique configuracion de servidor y si la RFC realmente existe'
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







