import pandas
from datetime import timedelta
import math

ln2 = math.log(2) 	#Declaring a constant used repeatedly.

def find_d2d(time_series, row, col):
	prev_date = row["Date"] - timedelta(days = 1)
	if(prev_date in time_series.Date.tolist()):
		N_t = row[col]
		N_0 = time_series.loc[time_series.Date == prev_date, col].item()
		if(N_0 == 0):
			return(0)
		elif((N_t / N_0) == 1.0):		#Handle values with no increment.
			return(ln2 / math.log(1.000001))
		else:
			return(ln2 / math.log(N_t / N_0))
	else:		
		return(0)