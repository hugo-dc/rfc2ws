import soaplib
from soaplib.core import Application
from soaplib.core.server import wsgi
import new


import base64
import gateway


def_imports = """
# Code generated automatically by rfc2py 

from soaplib.core.service import DefinitionBase
from soaplib.core.model.clazz import ClassModel, Array
import easysap
from soaplib.core.model.primitive import String, Integer, Float
from soaplib.core.service import soap
"""
def_types = "class Export_"
def_class = "\n\n\nclass Server(DefinitionBase):\n"



def sap2ws_type(sap_type):
	sap2ws = {
        	'C' : 'String',
	        'I' : 'Integer'
	}	
    
	if sap_type.find('C')>= 0:
		return 'String'
	if sap_type.find('I')>= 0:
		return 'Integer'
	if sap_type.find('P')>= 0:
		return 'Float'
	if sap_type.find('D')>= 0:
		return 'String'
	if sap_type.find('T')>= 0:
		return 'String'		
	if sap_type.find('N')>= 0:
		return 'Integer'	
	if sap_type.find('B')>= 0:
		return 'Integer'	
		
	print 'Warning: unknown type ', sap_type		
	return 'String'


def generate_method(rfc):
	rfc = gateway.getRFCObject(rfc)

	if rfc != False:
		has_exports = False
		has_tables = False 

		soap = "\t@soap("
		method = "\n\tdef "+rfc.get_name()+'(self, '
		implementation = '\t\t\tconn = r"%s"\n' % gateway.get_connstring() 
		implementation += "\t\t\trfc = easysap.RFC('"+rfc.get_name()+"', conn)\n"

		for imp in rfc.imports.keys():
			# getting datatype
			d = rfc.imp_def[imp]['datatype'] 
			soap   += sap2ws_type(d)  + ', '
			method += imp + ', '

			implementation += "\t\t\trfc.imports['%s'] = %s\n" % (imp, imp)


		# For import tables 
		for tab in rfc.tables.keys():
			d = rfc.tab_def[tab]['reftype']
			fields = gateway.getTableDefinition(d)

			implementation += '\t\t\tif '+tab+'!= None and len('+tab+') > 0:\n'
			implementation += "\t\t\t\trfc.init_table('"+tab+"')\n"
			implementation += "\t\t\t\tline = rfc.tables['"+tab+"'].struc()\n"
			
			implementation += "\t\t\t\tfor row in "+tab+":\n"

			for field in fields:
				implementation += "\t\t\t\t\tline['"+field[0]+"'] = row."+field[0] + "\n"
				implementation += "\t\t\t\t\trfc.tables['"+tab+"'].append(line)\n"	

		implementation += '\n\t\t\trfc.run()\n'

		datatypes = def_types + rfc.get_name()+"(ClassModel):\n\t"
		datatypes += '__namespace__ = "export" \n'
		
		if len(rfc.exports) > 0 or len(rfc.tables) > 0:
			implementation += '\t\t\texport = Export_'+rfc.get_name()+'()\n' 

		for exp in rfc.exports.keys():
			has_exports = True
			d = rfc.exp_def[exp]['datatype']
			datatypes += '\t' + exp + ' = ' + sap2ws_type(d) + '\n'
			implementation += '\t\t\texport.'+exp+ " = rfc.exports['"+exp+"']\n"  


		tab_types = ""



		# For export-tables
		for tab in rfc.tables.keys():
			implementation += '\t\t\ttable = []\n'
			method += tab+', '

			has_tables = True
			d = rfc.tab_def[tab]['reftype']
			fields = gateway.getTableDefinition(d)
			
			soap += 'Array('+d+'_'+rfc.get_name()+'), '
			implementation += '\t\t\trow = '+d+'_'+rfc.get_name()+'()\n'
			implementation += "\t\t\tfor line in rfc.tables['%s']:\n" % tab 

			tab_types += '\nclass '+d+'_'+rfc.get_name()+'(ClassModel):'
			tab_types += '\n\t__namespace__ = "'+d+'"'

			datatypes += '\t' + tab + ' = Array(' +d+'_'+rfc.get_name()+')\n' 

			for field in  fields:
				tab_types += '\n\t'+field[0] + ' = ' + sap2ws_type(field[1])	
				implementation += "\t\t\t\trow."+field[0]+" = line['"+field[0]+"']\n"
			implementation += '\t\t\t\ttable.append(row)\n'

			implementation += '\t\t\texport.'+tab+' = table\n'
		implementation += '\t\t\treturn export\n\n'
				

			#print '>'+e+'<'	



		soap += " _returns=Export_"+rfc.get_name()+")"

		tab_types += '\n\n\n'

		datatypes = tab_types + datatypes
	
		method = method[0:-2] + '):\n'

		method = soap + method + implementation
		return method, datatypes  	

	return '', ''			
	

    
if __name__ == '__main__':
	print '\n\nGenerating services...'
	active_rfcs = gateway.get_active_RFCs()
	definition = ""
	methods = ''
	datatypes = ''
	for rfc in active_rfcs:
		m, d = generate_method(rfc[1])
		methods   += m
		datatypes += d

	definition = def_imports
	definition += datatypes
	definition += def_class 
	definition += methods 


	#f = open('definition.py', 'w')
	#f.write(definition	)
	#f.close()

	module = new.module('definition')
	exec definition in module.__dict__


	#import definition
	
	try:
		from wsgiref.simple_server import make_server
		soap_application = soaplib.core.Application([module.Server], 'tns')
		wsgi_application = wsgi.Application(soap_application)
		server = make_server('localhost', 7789, wsgi_application)
		server.serve_forever()
	except ImportError:
		print "Error: example server code requires Python >= 2.5"	
