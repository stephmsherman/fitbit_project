import pandas as pd
import numpy as np
import datetime as dt

##PURPOSE: examining personal fitbit data to check whether minute-by-minute data matches 24 hour data

data = pd.read_csv('/Volumes/LabShareFolder/fitbit_project/fitbit_data/minute_data/all_minute.csv')

mydata = data[data.key ==105]
mydata['date'] = pd.to_datetime(mydata['stepdate'])
mydata['day'] = mydata['date'].dt.date
byday_key = mydata.groupby(['key','day'])
activities_day = byday_key['activities_steps'].aggregate(np.sum)
activities_day = activities_day.to_frame().reset_index()
activities_day['day'] = pd.to_datetime(activities_day['day'])
#days = activities_day
activities_day.rename(columns={'activities_steps':'activities_steps_minute'},inplace=True)

day = pd.read_csv('/Volumes/LabShareFolder/fitbit_project/fitbit_data/summary_daily_data/all_daily_data.csv')
day = day[day.key == 105]
day['day'] = pd.to_datetime(day['stepdate'])

m=pd.merge(activities_day,day, on = ['key','day'],how ='inner')
#m['diff_steps'] = m.activities_steps_x - m.activities_steps_y 
b = pd.read_csv('/Volumes/LabShareFolder/fitbit_project/fitbit_data/device_all.csv')
b['date'] = pd.to_datetime(b['lastsynctime'])
b['day'] = b['date'].dt.date
b['day'] = pd.to_datetime(b['day'])
all = pd.merge(m,b, on = ['key','day'], how = 'inner')

all['diff_steps'] = all.activities_steps_x - all.activities_steps_y 

no=all[all.diff_steps !=0]

df = no[['key','date', 'battery','activities_steps_x','activities_steps_y','diff_steps']]
df_Empty = df[(df.battery == 'Empty') | (df.battery == 'Low')]