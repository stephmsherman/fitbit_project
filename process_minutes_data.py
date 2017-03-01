import pandas as pd
import numpy as np
import datetime as dt

data = pd.read_csv('/Volumes/LabShareFolder/fitbit_project/fitbit_data/minute_data/all_minute.csv')

##remove anyone tested before we were live
data = data[data.key >=106]

##make the stepdate column in date/time form
data['stepdate'] = pd.to_datetime(data['stepdate'])

##if want to make date/time the index
data.index = data['stepdate']

data['key'].value_counts()
data.head()

##makes a new column called hours and day
data['hours'] = data.index.hour
data['day'] = data['stepdate'].dt.date
#data['seconds'] = data.index.seconds

##creates new column called wac_dates to designate the time period associated with before, during, and after the walk
data.loc[data['stepdate'] > '2016-12-05','walk_dates'] = 'after'
data.loc[(data['stepdate'] >= '2016-10-03') & (data['stepdate'] <= '2016-12-05'), 'walk_dates'] = 'during'
data.loc[(data['stepdate'] >= '2016-09-01') & (data['stepdate'] < '2016-10-03'),'walk_dates'] = 'before'

##create new data frame to find which days participants have 0 steps
byday_key = data.groupby(['key','day'])
num_mins = byday_key['activities_steps'].size()
num_mins = num_mins.to_frame().reset_index()
num_mins.rename(columns={0:'l'},inplace=True)
num_mins[num_mins.l !=1440]
activities_day = byday_key['activities_steps'].aggregate(np.sum)
activities_day = activities_day.to_frame().reset_index()
days = activities_day
days.rename(columns={'day':'date'},inplace=True)


days.to_csv('/Volumes/LabShareFolder/fitbit_project/fitbit_data/minute_data/all_min_to_day.csv',index=None)

##remove days where all activities_step = 0
days_worn = activities_day[activities_day.activities_steps!=0]

##only merge dates that are in common across both dataframes
#meaning only merge dates of days where subject wore fitbit
min_worn = pd.merge(data,days_worn, on = ['key','day'], how = 'inner')
min_worn.to_csv('/Volumes/LabShareFolder/fitbit_project/fitbit_data/minute_data/all_minute_worn.csv',index=None)

###looking at data
min_worn.loc[min_worn['activities_steps_y'] == 0 ]

min_byday_key = min_worn.groupby(['key','day'])

min_worn['seq']= min_worn.groupby(['key','walk_dates']).cumcount()

week = min_worn.loc[min_worn['seq'] < (1440*7)]

del week['activities_steps_y']
week.rename(columns={'activities_steps_x':'activities_steps'},inplace=True)

week.to_csv('/Volumes/LabShareFolder/fitbit_project/fitbit_data/minute_data/all_week_worn.csv',index=None)
