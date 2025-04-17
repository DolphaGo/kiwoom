from pykrx import stock
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 파라미터 설정
ticker = "005930"  # 삼성전자
start = "20240101"
end = "20241231"
k = 0.5  # 변동성 비율
fee = 0.001  # 수수료 0.1% (매수+매도 왕복)

# 데이터 로딩
df = stock.get_market_ohlcv_by_date(start, end, ticker)

# 변동성 돌파 전략을 위한 대상 계산 (전일 고가 - 전일 저가) * k
df['target'] = (df['고가'].shift(1) - df['저가'].shift(1)) * k

# 매매 시뮬레이션
df['buy'] = df['시가'] + df['target']
df['sell'] = np.where(df['고가'] > df['buy'], df['종가'], np.nan)

# 백테스팅 수익률 계산
df['return'] = np.where(df['고가'] > df['buy'], df['sell'] / df['buy'], 1)

# 누적 수익률 계산
df['cumulative return'] = df['return'].cumprod()

# 그래프 출력
plt.figure(figsize=(12, 6))
plt.plot(df['cumulative return'], label ="누적 수익률")
plt.xlabel("Date")
plt.ylabel("누적 수익률")
plt.title("삼성전자 - 변동성 돌파 전략")
plt.legend()
plt.show()
