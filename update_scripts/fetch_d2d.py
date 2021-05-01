'''This script loads the worksheet of the TIFR for updates on COVID-19 spread in Mumbai and stores the latest tally in the time-series dataset and regenerates the corresponding CSV file.'''

import pandas as data
import os.path
from utility import *

base_dir = os.path.join(os.path.dirname(__file__), "../")		#Obtain the path to the base directory for absosulte addressing.

#Load the time-series.
time_series = data.read_csv(base_dir + "time-series/Mumbai_aggregated.csv")
time_series.Date = data.to_datetime(time_series.Date, dayfirst =True)

#Create the days-to-double dataframe.
days_to_double = data.DataFrame(columns = ["Date", "Confirmed", "Deceased"])

#Append rows to the new dataframe.
days_to_double = days_to_double.append(
	[{"Date": row.Date,
	"Confirmed": find_d2d(time_series, row, "Confirmed"),
	"Deceased": find_d2d(time_series, row, "Deceased")}
		for _, row in time_series.iterrows()], ignore_index = True)

#Format the columns.
days_to_double.Date = data.to_datetime(days_to_double.Date, dayfirst = True)
days_to_double = days_to_double.astype({"Confirmed": int, "Deceased": int})

#Store the days-to-double series to a CSV file.
days_to_double.to_csv(base_dir + "time-series/Mumbai_days_to_double.csv", index = False)