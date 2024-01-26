import pandas as pd
import numpy as np
import logging
from datetime import datetime
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


Alpha_2 = correlation(rank(delta(volume, 2)), rank((close-open)/open), 6)*-1
Alpha_2.set_trading_price(close.data)

ic_test(Alpha_2, save=True)
group_test(Alpha_2, save=True)

