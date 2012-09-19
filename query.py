import os 

def get(query_name):
	if os.path.exists('sql/'+query_name+'.sql'):
		query_file = open('sql/'+query_name+'.sql', 'r')
		query = query_file.read()
		query_file.close()
		return query 
		


