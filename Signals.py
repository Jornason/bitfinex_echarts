# ===移动平均线策略
# 简单移动均线策略，仅作为案例不具交易价值
def signal_moving_average(df, para=[50, 500, 30, 300]):
    """
    简单的移动平均线策略
    当短期均线由下向上穿过长期均线的时候，买入；然后由上向下穿过的时候，卖出。
    :param df:  原始数据
    :param para:  参数，[ma_short, ma_long]
    :return:
    """
    #signal:1 买入
    #signal: -1 卖出
    #signal: 平仓 0

    # ===计算指标
    ma_long_fast = para[0]
    ma_long_slow = para[1]

    ma_short_fast = para[1]
    ma_short_slow = para[2]
    
    # 计算均线
    df['ma_long_fast'] = df['close'].rolling(ma_long_fast, min_periods=1).mean()
    df['ma_long_slow'] = df['close'].rolling(ma_long_slow, min_periods=1).mean()
    df['ma_short_fast'] = df['close'].rolling(ma_short_fast, min_periods=1).mean()
    df['ma_short_slow'] = df['close'].rolling(ma_short_slow, min_periods=1).mean()

    # ===找出买入信号
    condition1 = df['ma_long_fast'] > df['ma_long_slow']  # 短期均线 > 长期均线
    condition2 = df['ma_long_fast'].shift(1) <= df['ma_long_slow'].shift(1)  # 之前的短期均线 <= 长期均线
    df.loc[condition1 & condition2, 'signal'] = 1  # 将产生做多信号的那根K线的signal设置为1，1代表做多

    # ===找出买入平仓信号
    condition1 = df['ma_long_fast'] < df['ma_long_slow']  # 短期均线 < 长期均线
    condition2 = df['ma_long_fast'].shift(1) >= df['ma_long_slow'].shift(1)  # 之前的短期均线 >= 长期均线
    df.loc[condition1 & condition2, 'signal'] = 0  # 将产生平仓信号当天的signal设置为0，0代表平仓

    # ===找出卖出信号
    condition1 = df['ma_short_slow'] > df['ma_short_fast']  # 短期均线 < 长期均线
    condition2 = df['ma_short_slow'].shift(1) <= df['ma_short_fast'].shift(1)  # 之前的短期均线 >= 长期均线
    df.loc[condition1 & condition2, 'signal'] = -1  # 将产生做空信号的那根K线的signal设置为-1，1代表做多

    # ===找出卖出平仓信号
    condition1 = df['ma_short_slow'] < df['ma_short_fast']  # 短期均线 < 长期均线
    condition2 = df['ma_short_slow'].shift(1) >= df['ma_short_fast'].shift(1)  # 之前的短期均线 >= 长期均线
    df.loc[condition1 & condition2, 'signal'] = 0  # 将产生平仓信号当天的signal设置为0，0代表平仓


    df.drop(['ma_long_fast', 'ma_long_fast', 'ma_short_slow', 'ma_short_fast'], axis=1, inplace=True)

    # ===由signal计算出实际的每天持有仓位
    # signal的计算运用了收盘价，是每根K线收盘之后产生的信号，到第二根开盘的时候才买入，仓位才会改变。
    df['pos'] = df['signal'].shift()
    df['pos'].fillna(method='ffill', inplace=True)
    df['pos'].fillna(value=0, inplace=True)  # 将初始行数的position补全为0
    return df
