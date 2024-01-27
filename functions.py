"""储存了所有计算因子时可能用到的函数"""

import pandas as pd
import numpy as np
import logging
import warnings
from class_factor import Factor
warnings.filterwarnings("ignore")


def stddev(f: Factor, n):
    """标准差"""
    std_data = f.data.rolling(n).std()
    std_expr = f"stddev({f.expr}, {n})"

    return Factor(std_data, std_expr)


def signed_power(f: Factor, power):
    """次方函数"""
    sp_data = np.sign(f.data) * np.power(np.abs(f.data), power)
    sp_expr = f"SignedPower({f.expr}, {power})"

    return Factor(sp_data, sp_expr)


def ts_argmax(f: Factor, window):
    """
    返回最大值所在位置
    例如最大值在n天前，则返回n
    """
    max_values = pd.DataFrame(index=f.data.index, columns=f.data.columns)

    for i in range(len(f.data)):
        if i < window - 1:
            max_values.iloc[i] = np.nan
        else:
            max_values.iloc[i] = f.data.iloc[i - window + 1:i + 1].max()

    expr = f"Ts_ArgMax({f.expr}, {window})"

    return Factor(max_values, expr)


def rank(f: Factor):
    """
    截面排序，返回排名，参数中的ascending指升序排名，method='min'指值相同时，取较小的作为并列排名。例如并列第二，而不是并列第三。
    :param f:
    :return:
    """
    ranked_data = f.data.rank(axis=1, method='min')
    ranked_data.index = pd.to_datetime(ranked_data.index)

    ranked_expr = f"rank({f.expr})"

    return Factor(ranked_data, ranked_expr)


def where(condition, x, y):
    """
    三元表达式：如果条件满足，则结果为x，否则结果为y
    :param condition: Factor or boolean
    :param x: Factor or numeric value
    :param y: Factor or numeric value
    :return:
    """
    if isinstance(condition, Factor) and isinstance(y, Factor):
        result_data = x.data.where(condition.data, y.data)
        result_expr = f'{condition.expr} ? {x.expr} : {y.expr}'
        return Factor(result_data, result_expr)
    elif isinstance(condition, Factor) and isinstance(y, int):
        result_data = x.data.where(condition.data, y)
        result_expr = f'{condition.expr} ? {x.expr} : {str(y)}'
        return Factor(result_data, result_expr)


def correlation(f1: Factor, f2: Factor, window):
    """
    计算两个指标间的相关性
    :param f1: Factor
    :param f2: Factor
    :param window: Integer
    """
    df1 = f1.data
    df2 = f2.data
    # 确保两个DataFrame的行和列是对齐的
    if not (df1.index.equals(df2.index) and df1.columns.equals(df2.columns)):
        raise ValueError("两个DataFrame的索引（行）和列必须对齐")

    # 初始化一个空的DataFrame来存储相关性数据
    correlations = pd.DataFrame(index=df1.index)

    # 对每只股票计算相关性
    for stock in df1.columns:
        # 提取每只股票的数据
        series1 = df1[stock]
        series2 = df2[stock]

        # 计算滚动相关性
        roll_corr = series1.rolling(window=window).corr(series2)

        # 将结果存入新的DataFrame
        correlations[stock] = roll_corr
    expr = f'correlation({f1.expr}, {f2.expr}, {window})'
    return Factor(correlations, expr)


def delta(f: Factor, delay):
    """计算当天的值减去delay天前的值"""
    data = f.data - f.data.shift(delay)
    expr = f'delta({f.expr}, {delay})'
    return Factor(data, expr)


def log(factor: Factor):
    """
    计算 Factor 实例的因子值的自然对数。
    """
    if not isinstance(factor, Factor):
        raise TypeError("The argument must be a Factor instance")

    new_data = np.log(factor.data)
    new_expr = f'log({factor.expr})'
    return Factor(new_data, new_expr, factor.trading_price)


def ts_rank(factor: Factor, window: int):
    """
    计算时序上的排名
    """
    if not isinstance(factor, Factor):
        raise TypeError("The argument must be a Factor instance")
    new_data = factor.data.rolling(window).rank(axis=0, ascending=True)
    new_expr = f'ts_rank({factor.expr}, {window})'
    return Factor(new_data, new_expr, factor.trading_price)


def abs(factor: Factor):
    """
    绝对值函数
    :param factor: Factor
    :return: Factor
    """
    if not isinstance(factor, Factor):
        raise TypeError("The argument must be a Factor instance")
    new_data = factor.data.abs()
    new_expr = f'abs({factor.expr})'
    return Factor(new_data, new_expr, factor.trading_price)


def ma(factor: Factor, window: int):
    """
    移动平均
    :param factor:
    :param window: 移动平均窗口长度
    :return:
    """
    if not isinstance(factor, Factor):
        raise TypeError("The argument must be a Factor instance")
    new_data = factor.data.rolling(window).mean()
    new_expr = f'ma({factor.expr}, {window})'
    return Factor(new_data, new_expr, factor.trading_price)


def sign(factor: Factor):
    """
    指示函数（大于0则为1，小于0则为-1）
    :param factor:
    :return:
    """
    if not isinstance(factor, Factor):
        raise TypeError("The argument must be a Factor instance")
    new_data = np.sign(factor.data)
    new_expr = f'sign({factor.expr})'
    return Factor(new_data, new_expr, factor.trading_price)


# if __name__ == '__main__':
#     # 给出一个使用实例
#     # 一般步骤是：1.先用用到的基本数据创建Factor对象。
#     # 2.再调用functions中的方法进行计算。
#     close = pd.read_hdf('data/hs300/hs300-20100101-20220101_price.h5', key='data')
#     returns = close.pct_change()
#     returns = Factor(returns, 'returns')
#     # 波动率因子
#     factor_std = stddev(returns, 20)
#     print(factor_std.expr)
