from util.db_helper import *
import numpy as np
import pandas as pd

# np : 크롤링 자료, dp
# df : 이전 + 오늘 데이터, today_price_data[0 ~ 4] : 시가 고가 저가 현재 거래량, purchase_price : 매입가

# 매도 조건
def check_sell(df, today_price_data, purchase_price, code):
    df['macd'] = df['close'].ewm(span=12).mean() - df['close'].ewm(span=26).mean()

    ckeck1 = (df['macd'].shift(periods=2))[-1:].values > (df['macd'].shift(periods=1))[-1:].values > df[-1:][
        'macd'].values

    ckeck2 = (purchase_price / df[-1:]["close"].values * 100 - 100) > 5

    if (ckeck1 or ckeck2) == True:
        print(df.tail(7))
        print("\033[35m", '[ 매도 ]', "\033[30m")

    return (ckeck1 or ckeck2)


def check_buy(df, today_price_data, code):
    # df['ma12'] = df['close'].ewm(span=12).mean()
    # df['ma26'] = df['close'].ewm(span=26).mean()

    df['macd'] = df['close'].ewm(span=12).mean() - df['close'].ewm(span=26).mean()
    df['macdP'] = df['macd'] / df['close'] * 100

    stochastic = [14, 5, 3]
    df['stFk'] = (df['close'] - df['low'].rolling(window=stochastic[0]).min()) / (
                df['high'].rolling(window=stochastic[0]).max() - df['low'].rolling(window=stochastic[0]).min()) * 100
    df["stFD=SK"] = df['stFk'].rolling(window=stochastic[1]).mean()

    ckeck1 = (df['macd'].shift(periods=1))[-1:].values == min((df['macd'].shift(periods=2))[-1:].values,
                                                              (df['macd'].shift(periods=1))[-1:].values,
                                                              df['macd'][-1:].values)
    ckeck2 = df[-1:]["stFD=SK"].values < 30
    ckeck3 = (df[-1:]["close"].values / (df['close'].shift(periods=1))[-1:].values * 100 - 100) < 5


    if (ckeck1 and ckeck2 and ckeck3) == True:
        print(df.tail(7))
        print("\033[35m", '[ 매수 ]', "\033[30m")
        last_order_check_db("buy", code, float(df[-1:]["macdP"].values))

    return