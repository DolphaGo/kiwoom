import matplotlib.pyplot as plt
import numpy as np
from pykrx import stock

# 파라미터 설정
ticker = "005930"  # 삼성전자
start = "20240101"
end = "20241231"
k = 0.3  # 변동성 비율
fee = 0.001  # 수수료 0.1% (매수+매도 왕복)

# 데이터 로딩
df = stock.get_market_ohlcv_by_date(start, end, ticker)

# 변동성 돌파 전략 계산
df['target'] = (df['고가'].shift(1) - df['저가'].shift(1)) * k
df['buy'] = df['시가'] + df['target']
df['sell'] = np.where(df['고가'] > df['buy'], df['종가'], np.nan)

# 수익률 계산
df['return'] = np.where(df['고가'] > df['buy'], df['sell'] / df['buy'] - 1 - fee, 0)

# 그래프: 일별 수익률 막대 그래프
plt.figure(figsize=(14, 6))
plt.bar(df.index, df['return'] * 100, color='skyblue')  # 일별 수익률을 퍼센트로 변환하여 그래프
plt.xlabel("Date")
plt.ylabel("일별 수익률")
plt.title("삼성전자 - 변동성 돌파 전략 (일별 수익률)")
plt.grid(True)
plt.tight_layout()
plt.show()
