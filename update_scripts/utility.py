import pandas
from datetime import timedelta
import math
import numpy as maths

ln2 = math.log(2) 	#Declaring a constant used repeatedly.
n_samples = 5		#Number of data-points to sample for per day to be predicted.

def lin_reg(*series):
	'''Fits the data (x, y) to the equation y = ax + b and returns (a, b)'''	
	if(len(series)) == 1:
		y = maths.array(series[0])
		if(y.ndim == 1):
			y = y.reshape(int(y.size / y.shape[0]), y.shape[0])
		x = maths.arange(y.shape[1])
	else:
		x, y = series

	x_ = maths.mean(x)
	y_ = maths.mean(y, axis = 1, keepdims = True)
	xy_ = maths.dot(y - y_, x - x_)
	xx_ = maths.dot(x - x_, x - x_)

	a = (xy_ / xx_).T
	b = maths.squeeze(y_) - (a * x_)
	return(a, b)

def exp_reg(y):
	'''Fits the data (y) to the equation y = b.(a^x) and returns (a, b)'''
	if(maths.array(y).ndim == 1):
		y = [y_ for y_ in y if y_ > 0]			#Clean non-zero values.
		if(len(y) == 0):		#If all entries in y are 0, then the required curve is the x-axis.
			return(0, 0)

		if(len(y) == 1):		#If there's only one entry in y, then the required curve is a line parallel to the x-axis: y = y[0]
			return(1, y[0])

	if(maths.any(maths.array(y) == 0)):
			raise ValueError("Non-zero elements required.")

	else:
		a, b = maths.exp(lin_reg(maths.log(y)))		#Fit the series to a linear model using a logarithmic scale.
		#y = b.(a^x)		=>		log(y) = x.log(a) + log(b)
		return(a, b)

def exp_predict(x, a, b):
	'''Returns a prediction for an exponenial series characterised by (a, b).'''
	return((a ** x) * b)

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
