'''This script loads the worksheet of the TIFR for updates on COVID-19 spread in Mumbai and stores the latest tally in the time-series dataset and regenerates the corresponding CSV file.'''

import pandas as data
import requests
import os.path
from utility import *

def compute_predictions(matrix, pred_index):
	"""Get predictions for a matrix of region-wise incremental entries."""
	if(len(matrix) == 0):
		return(list())		#Important to send an empty list as predictions.
	else:
		return(maths.rint(exp_predict(pred_index, *exp_reg(matrix))))

base_dir = os.path.join(os.path.dirname(__file__), "../")		#Obtain the path to the base directory for absosulte addressing.

#Tabulate the Worksheet data.
time_series = data.read_csv(base_dir + "update_scripts/Mumbai COVID-19 Daily Statistics - Daily Statistics.csv")
#raw_data = requests.get('https://docs.google.com/spreadsheet/ccc?key=1-OYukZzMlRcRKfMqh-pAle0JYAjLjUy08N9V6S51sq0&output=csv')
#raw_data = raw_data.content.decode().split('\r\n')
#time_series = data.DataFrame([row.split(',') for row in raw_data[1:]], columns = raw_data[0].split(','))

#Rename and format the required columns and drop the rest.
time_series = time_series.rename(columns = {"Cumulative Cases": "Confirmed", "Cumulative Recovered": "Recovered", "Cumulative Deaths": "Deceased"})
time_series = time_series[["Date", "Confirmed", "Recovered", "Deceased"]]
time_series.Date = data.to_datetime(time_series.Date, dayfirst = True)
time_series = time_series.astype({"Confirmed": int, "Recovered": int, "Deceased": int})

#Store the time-series to a CSV file.
time_series.to_csv(base_dir + "time-series/Mumbai_aggregated.csv", index = False)

#Load the days-to-double series.
days_to_double = data.read_csv(base_dir + "time-series/Mumbai_days_to_double.csv")
days_to_double.Date = data.to_datetime(days_to_double.Date, dayfirst = True)
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

#Load the predictions series.
predictions = data.read_csv(base_dir + "time-series/Mumbai_predictions.csv")
predictions.Date = data.to_datetime(predictions.Date, dayfirst = True)
dates_to_predict = time_series[~time_series.Date.isin(predictions.Date)].Date.tolist()		#Dates in time-series which are not present in predictions.
#Append new rows.
for date in dates_to_predict:
	predictions = predictions.append({"Date": date, "CNF_1D": 0,"CNF_1W": 0,"CNF_2W": 0,"DCS_1D": 0,"DCS_1W": 0,"DCS_2W": 0}, ignore_index = True)
#Insert predictions.
for samples, suffix in zip([n_samples, 7 * n_samples, 14 * n_samples], ["1D", "1W", "2W"]):
	cnf_predictables = []
	cnf_matrix =[]
	dcs_matrix = []
	dcs_predictables = []
	for date in dates_to_predict:
		vector = time_series[time_series.Date <= date].Confirmed.tolist()
		if(vector[-samples] > 0):		#Ensure that only non-zero entries are passed.
			cnf_predictables.append(date)
			cnf_matrix.append(vector[-samples:])

		vector = time_series[time_series.Date <= date].Deceased.tolist()
		if(vector[-samples] > 0):		#Ensure that only non-zero entries are passed.
			dcs_predictables.append(date)
			dcs_matrix.append(vector[-samples:])

	pred_index = samples + (samples / n_samples) - 1		#Input index for querying a prediction.
	#Predict new infections:
	raw_predictions = compute_predictions(cnf_matrix, pred_index)
	for date, pred in zip(cnf_predictables, raw_predictions):
		predictions.loc[predictions.Date == date, f"CNF_{suffix}"] = pred

	#Predict new deaths:
	raw_predictions = compute_predictions(dcs_matrix, pred_index)
	for date, pred in zip(dcs_predictables, raw_predictions):
		predictions.loc[predictions.Date == date, f"DCS_{suffix}"] = pred

#Format the columns.
predictions.Date = data.to_datetime(predictions.Date, dayfirst = True)
predictions = predictions.astype({"CNF_1D": int,"CNF_1W": int,"CNF_2W": int,"DCS_1D": int,"DCS_1W": int,"DCS_2W": int})

#Store the days-to-double series to a CSV file.
predictions.to_csv(base_dir + "time-series/Mumbai_predictions.csv", index = False)
