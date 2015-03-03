import getpass
import gateway
import subprocess 
import os
import text


ws_server_pid = None

# Web Services Server 
def stop_ws_server():
    print text.STOPPING_WS % ws_server_pid  
    if ws_server_pid != None:
        os.system('taskkill /F     /PID ' + str(ws_server_pid))
        print text.SRV_STP
    else:
        print text.SRV_NR

def start_ws_server():        
    print text.SRV_STR,
    global ws_server_pid
    ws_server_pid = subprocess.Popen(r'Python ws_server.py').pid
    print text.SRV_ID % ws_server_pid 

def restart_ws_server():
    stop_ws_server()
    start_ws_server()

# Commands 
#--
def start_ws():
    show_services()
    
    wsid = raw_input(text.CLI_ID)
    
    rfc = gateway.get_single_RFC(wsid)
    
    if len(rfc) == 0:
        print text.ERR_WID            
        return False 

    gateway.update_rfc_status(wsid, '1')
    restart_ws_server()
    

# --
def show_services():
    status = { '0' : 'Not running',
               '1' : 'Running'
    }

    services = gateway.getRFCs() 
    print text.SRV_HEAD
    for service in services:
        print text.SRV_LINE % (service[0], service[1], service[2])


#--        
def conf_sap_server():
    print text.SRV_CFG_HD
    name   = raw_input(text.SRV_NAME)
    ip     = raw_input(text.SRV_HOST)
    sysnr  = raw_input(text.SRV_SYSNR)
    client = raw_input(text.SRV_MANDT)
    user   = raw_input(text.SRV_USER)
    passwd = getpass.getpass(text.SRV_PASS)

    gateway.insert_config(name, ip, sysnr, client, user, passwd)


#--    
def new_ws():
    if not gateway.isConnected():
        print text.MSG_CFSAP
        return False

    print text.NWS_HEAD
    rfc = raw_input(text.RFC_NAME)
    rfc = rfc.upper().strip()

    if gateway.existsRFCinDB(rfc):
        print text.ERR_RFCEXS
        return False 
        
    if not      gateway.existsRFCinSAP(rfc):
        print text.ERR_RFCDNE # rfc does not exist!
        return False 

        
    gateway.insert_rfc(rfc)    

    print text.MSG_WSCR # Service have been created




#--
def exit():
    stop_ws_server()
    print text.MSG_BYE
    return True 
    

#--
def help_():
    print text.CLI_HELP
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
    print 
    exit = False 
    while(exit != True):
        command = raw_input('\n>>> ')
        command = command.replace(' ', '').lower()

        if command in execute_command.keys():
            exit = execute_command[command]()
        else:
            if len(command.strip()) > 1:        
                print text.ERR_CMNF % command


