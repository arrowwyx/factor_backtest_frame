from new_alphalens import performance
from new_alphalens import plotting
from new_alphalens import tears
from new_alphalens import utils
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


# 因子的实现部分
close = pd.read_hdf('data/data_Ashare/close.h5', key='data')
returns = close.pct_change()
returns = Factor(returns, 'returns')
# 以波动率因子(20天日收益率标准差)为例
factor_std = stddev(returns, 20)
factor_std.set_trading_price(close)
# 这里经过处理的的factor_return是一个包含未来收益率，因子值和因子分组的dataframe。
# 后续要使用alphalens中的其他函数，必须先经过utils.get_clean_factor_and_forward_returns
# 因子构建完成后，只需要调用ic_test和group_test即可看到结果
ic_test(factor_std, save=False)
group_test(factor_std, save=False)
