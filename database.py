import os
import sqlite3
import query 

DB_NAME = 'rfc2ws.db'

# database
def executeQuery(query, q = 'S', val=True):
    r = None
    if val:
        checkDatabase()
            
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute(query) 
    if q == 'S':
        r = cur.fetchall()
    if q == 'I':
        r = con.commit()
    cur.close()
    con.close()
    return r

def checkDatabase():
    exists = False
    if os.path.exists(DB_NAME):
        exists = True
        
    if not exists:
        print "\nDatabase doesn't exists"
        print "Creating database..."

        print "Creating Table 'Server'..."
        sql = query.get('ct_server')
        executeQuery(sql, 'I', False)

        print "Creating Table 'RFCs'..."
        sql = query.get('ct_rfcs')
        executeQuery(sql, 'I', False)
        exists = True

        print "Creating Table 'Signals'..."
        sql = query.get('ct_signals')
        executeQuery(sql, 'I', False)

    return exists 




