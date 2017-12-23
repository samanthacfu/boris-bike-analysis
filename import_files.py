#Import csvs and combine 

#Imports
import glob
import os
import pandas as pd
import numpy as np
import pickle

#Get all csvs
path = '/Users/samanthafu/Boris Bike Data/'        
files = glob.glob(os.path.join(path, "*.csv"))     

#Import and append
df = pd.DataFrame()

for file in files:
    temp = pd.read_csv(file, skiprows=0)
    df = df.append(temp,ignore_index=True)

#Check out data
df.dtypes
df.head(5)

#Drop unnamed vars
df.drop([col for col in df.columns if "Unnamed" in col], axis=1, inplace=True)

#Convert dates to dt format
df["End Date"] = pd.to_datetime(df["End Date"],infer_datetime_format=True)
df["Start Date"] = pd.to_datetime(df["Start Date"],infer_datetime_format=True)

#Save down dataset
with open('boris_bike_data.pickle', 'wb') as output:
    pickle.dump(df, output)