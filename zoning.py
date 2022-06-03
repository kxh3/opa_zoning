import requests
import json
import os
import numpy as np
import pandas as pd

#Create code that iterates through addresses in df and inserts each into api address
def get_json(filepath):
    json_file = [] 
    df = pd.read_csv(filepath)
    for addresses in df['Address']:
        urlcall = f'https://api.phila.gov/ais/v1/search/{addresses}?gatekeeperKey=82fe014b6575b8c38b44235580bc8b11&include_units=true'
        urlcallJSON = requests.get(urlcall).json()
        json_file.append(urlcallJSON)
    return json_file

#Turn JSON file into a dataframe that returns the needed information
def create_df(filepath):
    zone = get_json(filepath)

    new_df = []
    for index in range(len(zone)):
        try:
            opa = zone[index]['features'][0]['properties']['opa_account_num']
            address = zone[index]['query']
            district_zone = zone[index]['features'][0]['properties']['zoning']

            new_df.append({
                'OPA' : opa,
                'Address' : address,
                'County' : 'Philadelphia',
                'Base District Zoning' : district_zone
            })
        
        except KeyError:
            pass
    
    return pd.DataFrame(new_df)