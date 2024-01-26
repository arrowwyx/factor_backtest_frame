from new_alphalens import performance
from new_alphalens import plotting
from new_alphalens import tears
from new_alphalens import utils
import pandas as pd
import numpy as np
from datetime import datetime
from class_factor import Factor
from functions import *
import matplotlib.pyplot as plt
import os


def ic_test(f: Factor, save=False):
    """
    IC分析，生成IC时序图
    :param f:
    :param save: boolean, 是否保存
    :return:
    """
    price = f.trading_price
    factor_return = utils.get_clean_factor_and_forward_returns(f.data.stack(), price)
    IC = performance.factor_information_coefficient(factor_return)
    ax = plotting.plot_ic_ts(IC)
    fig = ax[0].get_figure()  # 从任一轴对象获取图形对象
    fig.suptitle(f'{f.expr}')  # 设置总标题
    if save:
        if 'ic_plots' not in os.listdir():
            os.makedirs('ic_plots')
        plt.savefig(f'ic_plots/{f.expr}.png')
    plt.show()


def group_test(f: Factor, save=False):
    """
    我这里把group_test部分的代码单独拆出来画图
    图中的cumulative return就是cumprod得到的复利。
    :param f:
    :param save: boolean, 是否保存
    :return:
    """
    price = f.trading_price
    factor_return = utils.get_clean_factor_and_forward_returns(f.data.stack(), price)
    mean_quant_ret_bydate, std_quant_daily = performance.mean_return_by_quantile(
        factor_return,
        by_date=True,
        by_group=False,
        demeaned=False,
        group_adjust=False,
    )

    ax = plotting.plot_cumulative_returns_by_quantile(
        mean_quant_ret_bydate["1D"], period="1D")

    fig = ax.get_figure()  # 从任一轴对象获取图形对象
    fig.suptitle(f'{f.expr}')  # 设置总标题

    if save:
        if 'group_test_plots' not in os.listdir():
            os.makedirs('group_test_plots')
        plt.savefig(f'group_test_plots/{f.expr}.png')

    plt.show()


def small_summary(f: Factor):
    """
    :param f: 生成好的因子
    :return: 生成有关的文字性说明，具体如下：
            1.分组因子数值上的统计量
            2.收益分析
            3.IC分析（均值，标准差，t统计量等）
            4.换手率分析
            5.因子自相关系数
    """
    price = f.trading_price
    factor_return = utils.get_clean_factor_and_forward_returns(f.data.stack(), price)
    tears.create_summary_tear_sheet(factor_return)
    plt.show()


def return_summary(f: Factor):
    """
    alphalens自带的returns summary, 我觉得东西太多了
    :param f: 生成好的因子
    :return: 生成有关的文字性说明，具体如下：
            1.分组因子数值上的统计量
            2.收益分析
            3.IC分析（均值，标准差，t统计量等）
            4.换手率分析
            5.因子自相关系数
    """
    price = f.trading_price
    factor_return = utils.get_clean_factor_and_forward_returns(f.data.stack(), price)
    tears.create_returns_tear_sheet(factor_return)
    plt.show()


if __name__ == '__main__':
    open = Factor(pd.read_hdf('data/data_Ashare/open.h5'), 'open')
    volume = Factor(pd.read_hdf('data/data_Ashare/volume.h5'), 'volume')
    factor_3 = correlation(rank(open), rank(volume), 10)
    # 在写完因子表达式后，需要明确交易的价格
    factor_3.set_trading_price(pd.read_hdf('data/data_Ashare/close.h5'))
    ic_test(factor_3, save=True)
    group_test(factor_3)
