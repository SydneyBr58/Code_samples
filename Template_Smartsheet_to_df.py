import smartsheet 
import pandas as pd
import json
import requests

###############################################################################################
'Author: SydneyBr58'

'''
Purpose: This script logs into Smartsheet and download the entire content of a sheet into a DataFrame
'''
#################Credentials#########################
access_token = '' #Your access token, tied to your account, requires a license. You can only access sheet you manage.       
smartsheeturl = 'https://api.smartsheet.com/2.0/sheets/'
header = {'Authorization': "Bearer " + access_token,
          'Content-Type': 'application/json'}
smartsheet_client = smartsheet.Smartsheet(access_token)

def main():
    sheetid = '' #Specify the unique sheet ID of the sheet you wish to access, you can find it on Smartsheet, under File > Property
    uri = smartsheeturl + sheetid 
    req = requests.get(uri, headers=header)
    data = json.loads(req.text) #loads data from a json file
 
    for col in data['columns']: #This loop collects the column headers
        cols.append(col['title'])
    df = pd.DataFrame(columns=cols)
             
    for row in data['rows']:
        values = [] #re-initilise the values list for each row
        for cell in row['cells']:
            if cell.get('value'): #handle the empty values
                values.append( cell['value'])
            else:
                values.append('') 
        df = df.append(dict(zip(cols, values)), ignore_index=True, sort=False)
     
main()




