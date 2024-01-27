import pandas as pd
import numpy as np
import logging
import warnings
from class_factor import Factor
from functions import *
from factor_test import ic_test, group_test
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")


open = Factor(pd.read_hdf('data/data_Ashare/open.h5'), 'open')
high = Factor(pd.read_hdf('data/data_Ashare/high.h5'), 'high')
low = Factor(pd.read_hdf('data/data_Ashare/low.h5'), 'low')
close = Factor(pd.read_hdf('data/data_Ashare/close.h5'), 'close')
volume = Factor(pd.read_hdf('data/data_Ashare/volume.h5'), 'volume')


# Alpha_2 = correlation(rank(delta(log(volume), 2)), rank((close-open)/open), 6)*-1
# Alpha_2.set_trading_price(close.data)
# ic_test(Alpha_2, save=True)
# group_test(Alpha_2, save=True)

# Alpha_3 = correlation(rank(open), rank(volume), 10)
# Alpha_3.set_trading_price(close.data)
# ic_test(Alpha_3, save=True)
# group_test(Alpha_3, save=True)

# Alpha_4 = ts_rank(rank(low), 20) * -1
# Alpha_4.set_trading_price(close.data)
# ic_test(Alpha_4, save=True)
# group_test(Alpha_4, save=True)

# Alpha_6 = correlation(open, volume, 10)*-1
# Alpha_6.set_trading_price(close.data)
# ic_test(Alpha_6, save=True)
# group_test(Alpha_6, save=True)

# Alpha_7 = where(ma(volume,20)<volume, (ts_rank(abs(delta(close, 7)), 60))*sign(delta(close,7))*-1, -1)
# Alpha_7.set_trading_price(close.data)
# ic_test(Alpha_7, save=True)
# group_test(Alpha_7, save=True)
