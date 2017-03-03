import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
m = pd.read_csv('/Volumes/LabShareFolder/fitbit_project/fitbit_data/minute_data/all_min_to_day.csv')
m.rename(columns={'activities_steps':'activities_steps_min'},inplace=True)
d = pd.read_csv('/Volumes/LabShareFolder/fitbit_project/fitbit_data/summary_daily_data/all_summary_data_processed.csv')

b = pd.merge(m,d, on = ['key','date'], how = 'inner')

b = b[b.activities_steps != 0]
b = b[b.activities_steps_min != 0]

b.describe()

b['match_steps'] = np.where(b.activities_steps_min == b.activities_steps, 'yes','no')

b['match_steps'].value_counts()

b.plot.scatter(x = 'activities_steps_min',y = 'activities_steps') 
plt.show()


nos = b[b.match_steps == 'no']

nos['diff_steps'] = nos.activities_steps_x - nos.activities_steps_y 

nos.plot.scatter(x = 'activities_steps_x',y = 'activities_steps_y') 
plt.show()


nos['key'].value_counts()