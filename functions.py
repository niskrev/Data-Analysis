import numpy as np
import matplotlib.pyplot as plt

def find_station(s):
    found = {code: name for code, name in stations.items() if s in name}

    return found


dly_delimiter = [11, 4, 2, 4] + [5, 1, 1, 1] * 31
dly_usecols = [1, 2, 3] + [4*i for i in range(1, 32)]
dly_dtype = [np.int32, np.int32, (np.str_, 4)] + [np.int32]*31
dly_names = ['year','month', 'obs'] + [str(i) for i in range(1,32)]

def parsefile(filename):
    """
    parses the downloaded raw weather files using np genfromtxt method
    :param filename:
    :return:
    """
    return np.genfromtxt(filename,
                        delimiter = dly_delimiter,
                        usecols = dly_usecols,
                        dtype = dly_dtype,
                        names = dly_names)


def unroll(record):
    """
    utility function to reformat the row of raw data
    :param record: a row in the raw data file
    :return: np array with reformated data
    """
    startdate = np.datetime64('{}-{:02}'.format(record['year'], record['month']))
    dates = np.arange(startdate, startdate + np.timedelta64(1, 'M'), np.timedelta64(1, 'D'))

    rows = [(date, record[str(i + 1)] / 10) for i, date in enumerate(dates)]

    # return np.array(rows)
    return np.array(rows, dtype=[('date', 'M8[D]'), ('value', 'd')])


def get_obs(fname='USW00022536.dly', obs='TMAX'):
    """
    USAGE: tmax = get_obs('USW00022536.dly', 'TMAX')
    :param fname: .dly file with daily weather data
    :param obs: type of observations: e.g. TMAX
    :return: np array with the observations indexed by date
    """
    data = np.concatenate([unroll(row) for row in parsefile(fname) if row[2] == obs])
    data['value'][data['value'] == -999.9] = np.nan

    return data


def fill_nans(data):
    dates_float = data['date'].astype(np.float64)

    nan = np.isnan(data['value'])
    data['value'][nan] = np.interp(dates_float[nan], dates_float[~nan], data['value'][~nan])

    return data


def plot_smoothed(data, win=10):
    smoothed = np.correlate(data['value'], np.ones(win) / win, 'same')

    plt.plot(data['date'], smoothed)

def selectyear(data, year):
    start = np.datetime64('{}'.format(year))
    end = start + np.timedelta64(1,'Y')
    return data[(data['date']>= start) & (data['date'] < end)]['value']
