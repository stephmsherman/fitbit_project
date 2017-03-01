import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
m = pd.read_csv('/Volumes/LabShareFolder/fitbit_project/fitbit_data/minute_data/all_min_to_day.csv')
d = pd.read_csv('/Volumes/LabShareFolder/fitbit_project/fitbit_data/summary_daily_data/all_summary_data_processed.csv')

b = pd.merge(m,d, on = ['key','date'], how = 'inner')

b['match_steps'] = np.where(b.activities_steps_x == b.activities_steps_y, 'yes','no')

b['match_steps'].value_counts()

nos = b[b.match_steps == 'no']

nos['diff_steps'] = nos.activities_steps_x - nos.activities_steps_y 

nos.plot.scatter(x = 'activities_steps_x',y = 'activities_steps_y') 
plt.show()


nos['key'].value_counts()