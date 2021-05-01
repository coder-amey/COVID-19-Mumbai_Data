'''This script loads the worksheet of the TIFR for updates on COVID-19 spread in Mumbai and stores the latest tally in the time-series dataset and regenerates the corresponding CSV file.'''

import pandas as data
import requests
import os.path
from utility import *

base_dir = os.path.join(os.path.dirname(__file__), "../")		#Obtain the path to the base directory for absosulte addressing.

#Tabulate the Worksheet data.
raw_data = requests.get('https://docs.google.com/spreadsheet/ccc?key=1-OYukZzMlRcRKfMqh-pAle0JYAjLjUy08N9V6S51sq0&output=csv')
raw_data = raw_data.content.decode().split('\r\n')
time_series = data.DataFrame([row.split(',') for row in raw_data[1:]], columns = raw_data[0].split(','))

#Rename and format the required columns and drop the rest.
time_series = time_series.rename(columns = {"Cumulative Cases": "Confirmed", "Cumulative Recovered": "Recovered", "Cumulative Deaths": "Deceased"})
time_series = time_series[["Date", "Confirmed", "Recovered", "Deceased"]]
time_series.Date = data.to_datetime(time_series.Date, dayfirst = True)
time_series = time_series.astype({"Confirmed": int, "Recovered": int, "Deceased": int})

#Store the time-series to a CSV file.
time_series.to_csv(base_dir + "time-series/Mumbai_aggregated.csv", index = False)

#Load the days-to-double series.
days_to_double = data.read_csv(base_dir + "time-series/Mumbai_days_to_double.csv")
#Iterate over new rows.
days_to_double = days_to_double.append(
	[{"Date": row.Date,
	"Confirmed": find_d2d(time_series, row, "Confirmed"),
	"Deceased": find_d2d(time_series, row, "Deceased")}
		for _, row in time_series[~time_series.Date.isin(days_to_double.Date)].iterrows()], ignore_index = True)

#Format and store the days-to-double series into a CSV file.
days_to_double.Date = data.to_datetime(days_to_double.Date, dayfirst = True)
days_to_double = days_to_double.astype({"Confirmed": int, "Deceased": int})
days_to_double.to_csv(base_dir + "time-series/Mumbai_days_to_double.csv", index = False)