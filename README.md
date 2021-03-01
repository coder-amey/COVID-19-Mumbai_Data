# COVID-19-Mumbai_Data
## Data regarding region-wise spread of COVID-19 in India.

### Introduction:
* This repository stores data pertaining to the spread of COVID-19 in Mumbai.
* The data are arranged in a date-wise *time-series*.
* I thank the **[STCS, TIFR](https://www.tcs.tifr.res.in/)** for allowing me to access their source of raw data.
* I also thank each and every on-duty personnel on the frontlines of this battle against COVID-19. Let's help them by staying indoors.

### Functional Details:
* The *time-series* directory houses the CSV file storing the trends of the COVID-19 spread in Mumbai over time.
* The *update_scripts* directory contains the python scripts used for fetching data from the sources and updating the datasets accordingly.
* All the dates are represented in *'%d-%m-%Y'* format. Use the *dayfirst = True* argument of *pandas.read_csv()* function to correctly read the dates while loading the dataset into a dataframe.

### Sources:
* The primary source of these data is a Google Sheet of the **[STCS, TIFR](https://www.tcs.tifr.res.in/)**. Daily and historic updates are retrieved from this source since 1st March, 2021.

### Licensing:
This project is entirely from and for the public domain.  
Please feel free to utilise and distribute these datasets without any restrictions. (See MIT License)  

