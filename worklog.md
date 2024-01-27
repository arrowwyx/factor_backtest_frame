# Alpha101量价因子复现

- Alpha2: -1*correlation(rank(delta(log(volume), 2)), rank((close-open)/open), 6

反转类，刻画量价关系，如果最近成交量上升，且股票上涨，可能有不理性追涨现象，后续可能发生反转。
- Alpha3: correlation(rank(open), rank(volume), 10)

反转类，同样是量价关系。
- Alpha4: ts_rank(rank(low), 20) * -1

反转类，（原文参数是6）如果最近20天最低价走低，后续可能反转。
- Alpha6: correlation(open, volume, 10)*-1

反转类，量价关系

- Alpha7: where(ma(volume,20)<volume, (ts_rank(abs(delta(close, 7)), 60))*sign(delta(close,7))*-1, -1)

反转类，如果成交量大于二十天移动成交量，因子被激活，最近股价加速上涨时，因子值为负，可能发生反转。