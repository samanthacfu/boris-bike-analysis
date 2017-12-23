#Get list of stations and locations

#Impots
import requests
import pandas as pd

#Get data from TfL's API
response = requests.get("https://api.tfl.gov.uk/BikePoint")

bike_stations = pd.read_json(response.content)
bike_stations.head(5)

#Extract info from additionalProperties
for index, row in bike_stations.iterrows():
    bike_stations.loc[index,'install_date'] = row['additionalProperties'][3]['value']
    bike_stations.loc[index,'docks'] = row['additionalProperties'][8]['value']

#Export to csv
bike_stations.to_csv('stations.csv')