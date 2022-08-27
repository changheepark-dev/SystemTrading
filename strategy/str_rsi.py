from datetime import datetime
import numpy as np
import pandas as pd

# np : 크롤링 자료, dp
# df : 이전 + 오늘 데이터, today_price_data[0 ~ 4] : 시가 고가 저가 현재 거래량, purchase_price : 매입가

# 매도 조건
def check_sell(df, today_price_data, purchase_price, code):
    # RSI(N) 계산
    period = 2  # 기준일 설정
    date_index = df.index.astype('str')
    # df.diff를 통해 (기준일 종가 - 기준일 전일 종가)를 계산하여 0보다 크면 증가분을 넣고, 감소했으면 0을 넣어줌
    U = np.where(df['close'].diff(1) > 0, df['close'].diff(1), 0)
    # df.diff를 통해 (기준일 종가 - 기준일 전일 종가)를 계산하여 0보다 작으면 감소분을 넣고, 증가했으면 0을 넣어줌
    D = np.where(df['close'].diff(1) < 0, df['close'].diff(1) * (-1), 0)
    AU = pd.DataFrame(U, index=date_index).rolling(window=period).mean()  # AU, period=2일 동안의 U의 평균
    AD = pd.DataFrame(D, index=date_index).rolling(window=period).mean()  # AD, period=2일 동안의 D의 평균
    RSI = AU / (AD + AU) * 100  # 0부터 1로 표현되는 RSI에 100을 곱함
    df['RSI(2)'] = RSI

    # 금일의 RSI(2) 구하기
    rsi = df[-1:]['RSI(2)'].values[0]

    # 매도 조건 두 가지를 모두 만족하면 True
    return rsi > 80 and today_price_data[3] > purchase_price



def check_bay(df, today_price_data, code):
    # RSI(N) 계산
    period = 2  # 기준일 설정
    date_index = df.index.astype('str')
    # df.diff를 통해 (기준일 종가 - 기준일 전일 종가)를 계산하여 0보다 크면 증가분을 넣고, 감소했으면 0을 넣어줌
    U = np.where(df['close'].diff(1) > 0, df['close'].diff(1), 0)
    # df.diff를 통해 (기준일 종가 - 기준일 전일 종가)를 계산하여 0보다 작으면 감소분을 넣고, 증가했으면 0을 넣어줌
    D = np.where(df['close'].diff(1) < 0, df['close'].diff(1) * (-1), 0)
    AU = pd.DataFrame(U, index=date_index).rolling(window=period).mean()  # AU, period=2일 동안의 U의 평균
    AD = pd.DataFrame(D, index=date_index).rolling(window=period).mean()  # AD, period=2일 동안의 D의 평균
    RSI = AU / (AD + AU) * 100  # 0부터 1로 표현되는 RSI에 100을 곱함
    df['RSI(2)'] = RSI

    # 종가(close)를 기준으로 이동 평균 구하기
    df['ma20'] = df['close'].rolling(window=20, min_periods=1).mean()
    df['ma60'] = df['close'].rolling(window=60, min_periods=1).mean()

    rsi = df[-1:]['RSI(2)'].values[0]
    ma20 = df[-1:]['ma20'].values[0]
    ma60 = df[-1:]['ma60'].values[0]

    # 2 거래일 전 날짜(index)를 구함
    idx = df.index.get_loc(datetime.now().strftime('%Y%m%d')) - 2

    # 위 index로부터 2 거래일 전 종가를 얻어옴
    close_2days_ago = df.iloc[idx]['close']

    # 2 거래일 전 종가와 현재가를 비교함
    price_diff = (today_price_data[3] - close_2days_ago) / close_2days_ago * 100


    return ma20 > ma60 and rsi < 5 and price_diff < -2