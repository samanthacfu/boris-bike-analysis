#Clean and analyze data

#Imports
import pickle
import numpy as np
import datetime as dt
import pandas as pd

#Load dataset
with open('boris_bike_data.pickle', 'rb') as data:
    df = pickle.load(data)

df.dtypes
df.describe()

#Check on obs w any missing values
df_missing = df[df.isnull().any(axis=1)]
df_missing.sample(5)

#Check on obs with missing ids
df_missing_id = df[df['End Station Id'].isnull()] 
df_missing_id.sample(5)

#Fix 2017 data with different variable names ugh
df['Duration'] = np.where(df['Duration'].isnull(),df['Duration_Seconds'],df['Duration'])
df['EndStation Id'] = np.where(df['EndStation Id'].isnull(),df['End Station Id'],df['EndStation Id'])
df['StartStation Id'] = np.where(df['StartStation Id'].isnull(),df['Start Station Id'],df['StartStation Id'])
df['EndStation Name'] = np.where(df['EndStation Name'].isnull(),df['End Station Name'],df['EndStation Name'])
df['StartStation Name'] = np.where(df['StartStation Name'].isnull(),df['Start Station Name'],df['StartStation Name'])

#Create start and end date years to explore messed up dates
df['Start Date Year'] = df['Start Date'].dt.year
df['End Date Year'] = df['End Date'].dt.year

#Create duration variable in minutes as a time delta
df['Duration_Mins'] = pd.to_timedelta(df['Duration']/60, unit='m')

#Check on obs with weird start dates
df_weirdstartdates = df[ (df['Start Date Year']==1900) | (df['Start Date Year']==1901) | (df['Start Date Year']==1969)]
df_weirdstartdates.describe()

#Check on obs with weird end dates
df_weirdenddates = df[(df['End Date Year']==1970) | (df['End Date Year']==2011)]
df_weirdenddates.describe()

#Fix messed up dates
df['Start Date Fixed'] = np.where((df['Start Date Year']==1900) | (df['Start Date Year']==1901),df['End Date']-df['Duration_Mins'],df['Start Date']) 
df['End Date Fixed'] = np.where((df['End Date Year']==2011) | (df['End Date Year']==1970),df['Start Date']+df['Duration_Mins'],df['End Date'])                                 

#Double check that stuff was fixed!
df['Start Date Fixed Year'] = df['Start Date Fixed'].dt.year
df['End Date Fixed Year'] = df['End Date Fixed'].dt.year

df_weirdstartdates = df[(df['Start Date Fixed Year']==1900)|(df['Start Date Fixed Year']==1901)|(df['Start Date Fixed Year']==1969)]
df_weirdstartdates.describe()

df_weirdenddates = df[(df['End Date Fixed Year']==2011) | (df[('End Date Fixed Year')]==1970)]
df_weirdenddates.describe()

#It wasn't, so drop obs with negative durations (~200k)
df.drop(df[df['Duration'] < 0].index, inplace=True)

#Drop obs with weird start AND end dates (26)
df.drop(df[((df['Start Date Year'] == 1900) | (df['Start Date Year'] == 1901)) & (df['End Date Year'] == 1970)].index, inplace=True)

#Extract date, week, month, day, time, and hour from datetime
df["Date"] = pd.DatetimeIndex(df["Start Date Fixed"]).date
df["Week"] = df["Start Date Fixed"].dt.to_period('W')
df["Month"] = df["Start Date Fixed"].dt.to_period('M')
df["Day"] = df["Start Date Fixed"].dt.dayofweek
df["Time"] = df["Start Date Fixed"].dt.time
df["Hour"] = df["Start Date Fixed"].dt.hour

#Convert ids to numeric
df['StartStation Id'] = pd.to_numeric(df['StartStation Id'], errors='coerce')
df['EndStation Id'] = pd.to_numeric(df['EndStation Id'], errors='coerce')

#Average weekly rides
df["Week"].value_counts(sort=True).to_csv('weekly_rides.csv')

#Average weekly riders
weekly_riders = df['Rental Id'].groupby(df['Week']).nunique()
weekly_riders.to_csv('weekly_riders.csv')

#Average daily rides in 2017
df2017 = df[df['Start Date Fixed Year']==2017]
df2017["Date"].value_counts().mean()

#Average length of trips in 2017
df2017["Duration_Mins"].mean()

#Most popular stations in 2017
df2017["StartStation Id"].value_counts().to_csv('start_stations.csv')
df2017["EndStation Id"].value_counts().to_csv('end_stations.csv')

#Total rides by day of week
df["Day"].value_counts(sort=True).to_csv('daily_rides.csv')

#Convert timedelta to float to calculate groupby means 
df['Duration_Mins_Float'] = df['Duration_Mins'].dt.total_seconds()/60
#Duration of rides by day of week
df["Duration_Mins_Float"].groupby(df["Day"]).mean().to_csv('daily_rides_duration.csv')

#Capacity calculations: what % of bikes are out at any given time? 
df_capacity = df['Hour'].groupby(df['Date']).value_counts() #number of rides per day per hour
df_capacity.to_csv('hourly_capacity.csv')

#Usage at different times of day
#Average number of journeys started and ended at a station in 2017
df2017['StartStation Id'].groupby(df2017['Hour']).value_counts().to_csv('hourly_start_stations.csv')
df2017['EndStation Id'].groupby(df2017['Hour']).value_counts().to_csv('hourly_end_stations.csv')

#Most common routes in 2017
df2017_stations['Month'].groupby([df2017_stations['StartStation Id'],df2017_stations['EndStation Area']]).value_counts().to_csv("2017journeys.csv",header=True)

#Rides exceeding 30 minutes
df_duration30 = df[df['Duration_Mins_Float']>30]
df_duration30['Duration_Mins'].count().astype('float')/df['Duration_Mins_Float'].count().astype('float')

#Merge in station details
file = '/Users/samanthafu/stations_clean.csv' 
stations = pd.read_csv(file, skiprows=0)

df_stations = pd.merge(df,
      			stations[['area', 'borough']],
                left_on=df['StartStation Id'], 
                right_on=stations['id'],
                how='left')

df_stations.rename(columns={"area": "StartStation Area", "borough":"StartStation Borough"}, inplace=True)

df_stations = pd.merge(df_stations,
                 stations[['area', 'borough']],
                 left_on=df_stations['EndStation Id'], 
                 right_on=stations['id'],
                 how='left')

df_stations.rename(columns={"area": "EndStation Area", "borough":"EndStation Borough"}, inplace=True)

#Get total monthly journeys to adjust for seasonality
df['Month'].value_counts().to_csv("monthly_journeys.csv")

#Start and ends by station
df['Month'].groupby(df['StartStation Id']).value_counts().to_csv("journeys_starts.csv")
df['Month'].groupby(df['EndStation Id']).value_counts().to_csv("journeys_ends.csv")

#Save down clean dataset
with open('boris_bike_data_clean.pickle', 'wb') as output:
    pickle.dump(df, output)


