import pandas as pd
import urllib
import pyodbc
from sqlalchemy import create_engine
import datetime
import csv

#################################################################################################
'Author: SydneyBr58'
# Template to log in to a SQL server, get the result of a query and print it in an excel file. Write an error message in an excel file if the process fails.

#Connection to the SQL server
server='' #server name
database='' #database name
username=''
password=''

sql_conn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = sql_conn.cursor()
params = urllib.parse.quote_plus('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password) #adjust the engine if you are using another database
engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params) #adjust the engine if you are using another database


def get_data():
    
    df = pd.read_sql_query('''
    write your SQL query here
    ''', engine) #Read SQL query, save it in a dataframce

    df.to_excel('name_of_the_file.xlsx') #If you do not specify a complete file path, the file will be created in Python default folder
  

def notification(error_message):

    now = datetime.datetime.now()
    text = 'The desired task has failed. Please fix it. It happened on the '+str(now)+'\n Error message: '+str(error_message)
  
	with open('error_log.csv', mode='a') as error_log:
        log_writer = csv.writer(error_log, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        log_writer.writerow([text])


def main():
    try:
        get_data()
    except Exception as e:
        notification(e)

main()


