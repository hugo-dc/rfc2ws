Rfc2ws
======

### Required Python Modules:
	easysap/pysap       https://github.com/hugo-dc/easysap
	soaplib             https://github.com/soaplib/soaplib

#### Important
You need to install zddif_field_info_get in your SAP System in order to run this program.
The file zzdif_field_info_get is included in the easysap library, the code should be implemented as a SAP RFC.



Un programa para exponer una RFC como Servicio Web.

El programa tendr� las siguientes opciones:

#### 1. Configurar servidor SAP. 

#### 2. Configurar la RFC.

	Se pregunta el nombre de la RFC 
	Se busca la definici�n de la RFC 
	Se debe configurar qu� parametros de la RFC ser�n expuestos en el web service.

#### 3. Generacion de codigo python para el WebService de esa RFC
	
	Este codigo debe implementar el webservice y tener una funcion principal para mandarse a llamar desde el servidor WS Python  

#### 4. Servidor de WS Python.	

	Este servidor leer� de la base de datos qu� RFCs deben estar expuestas como WebService. Y deber� crear un metodo para cada una.


Ejemplo:
========

python cli.py

