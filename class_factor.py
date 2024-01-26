import pandas as pd
import numpy as np
import logging
from datetime import datetime


class Factor:
    """
    因子类：
    类中储存了因子值和计算因子值的表达式。
    类中还可以储存用于交易的价格。
    """

    def __init__(self, data, expr='', trading_price=None):
        """
        类中储存三个对象
        data为dataframe格式，index是日期，column是股票代码，表示目前的因子值
        expr为字符串格式，表示计算因子的公式
        以上两项在调用function中函数对因子进行计算后都会更新
        """
        self.data = data
        self.expr = expr
        self.trading_price = trading_price

    def _generate_expr(self, operation, other):
        if isinstance(other, Factor):
            return f'({self.expr}) {operation} ({other.expr})'
        elif isinstance(other, (int, float)):
            return f'({self.expr}) {operation} {other}'
        else:
            raise TypeError("Unsupported type for expression generation")

    def __add__(self, other):
        if isinstance(other, Factor):
            new_data = self.data + other.data
            new_expr = self._generate_expr('+', other)
        elif isinstance(other, (int, float)):
            new_data = self.data + other
            new_expr = self._generate_expr('+', other)
        else:
            raise TypeError("Unsupported type for addition")
        return Factor(new_data, new_expr, self.trading_price)

    def __sub__(self, other):
        if isinstance(other, Factor):
            new_data = self.data - other.data
            new_expr = self._generate_expr('-', other)
        elif isinstance(other, (int, float)):
            new_data = self.data - other
            new_expr = self._generate_expr('-', other)
        else:
            raise TypeError("Unsupported type for subtraction")
        return Factor(new_data, new_expr, self.trading_price)

    def __mul__(self, other):
        if isinstance(other, Factor):
            new_data = self.data * other.data
            new_expr = self._generate_expr('+', other)
        elif isinstance(other, (int, float)):
            new_data = self.data * other
            # 乘法时把常数放在前面
            new_expr = f'{str(other)}* {self.expr}'
        else:
            raise TypeError("Unsupported type for multiplication")
        return Factor(new_data, new_expr, self.trading_price)

    def __truediv__(self, other):
        if isinstance(other, Factor):
            new_data = self.data / other.data
            new_expr = self._generate_expr('/', other)
        elif isinstance(other, (int, float)):
            new_data = self.data / other
            new_expr = self._generate_expr('/', other)
        else:
            raise TypeError("Unsupported type for division")
        return Factor(new_data, new_expr, self.trading_price)

    def set_trading_price(self, trading_price):
        """
        设置因子的交易价格，方便后续环节
        这个dataframe应该与data的index和column都一致
        :param trading_price:
        :return:
        """
        self.trading_price = trading_price

    def standardize(self):
        """
        在截面上对因子进行标准化
        :return:
        """
        self.data = self.data.apply(lambda x: (x-x.mean())/x.std(), axis=1)

    def mad(self, n=3):
        """
        中位数偏差法去极值
        :param n: 阈值大小
        :return:
        """
        def mad_based_outlier(data, n):
            med = data.median()
            mad = (abs(data-med)).median()
            high = med + (n * 1.4826 * mad)
            low = med - (n * 1.4826 * mad)

            return data.clip(lower=low, higher=high)

        self.data = self.data.apply(mad_based_outlier, axis=1)
