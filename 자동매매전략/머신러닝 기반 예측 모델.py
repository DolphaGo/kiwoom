import matplotlib.pyplot as plt
import pandas as pd
from pykrx import stock
from sklearn.ensemble import RandomForestRegressor

# 1. 데이터 불러오기
ticker = "005930"
train_start = "20230101"
train_end = "20250131"
test_start = "20250201"
test_end = "20250228"

train_df = stock.get_market_ohlcv_by_date(train_start, train_end, ticker)
test_df = stock.get_market_ohlcv_by_date(test_start, test_end, ticker)


# 2. 전일 기준으로 예측
def make_supervised_data(df):
    X = df.shift(1).dropna()[['시가', '고가', '저가', '종가', '거래량']]
    y = df['고가'].iloc[1:]  # 다음날 고가
    print(len(X), len(y))
    return X, y


X_train, y_train = make_supervised_data(train_df)
X_test, y_test = make_supervised_data(test_df)

# 3. 랜덤 포레스트 모델 학습 및 예측
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
predictions = model.predict(X_test)

# 4. 결과 정리
results = test_df.iloc[1:].copy()
results['예측_고가'] = predictions
results['실제_고가'] = y_test

# 5. 시각화
full_df = pd.concat([train_df[['고가']], results[['실제_고가', '예측_고가']]], axis=0)

plt.figure(figsize=(14, 6))
plt.plot(full_df.index, full_df['고가'], label='실제 고가 (Train)', color='blue')
plt.plot(results.index, results['실제_고가'], label='실제 고가 (2025)', color='black')
plt.plot(results.index, results['예측_고가'], label='예측 고가 (2025)', linestyle='--', color='orange')
plt.xlabel("날짜")
plt.ylabel("고가")
plt.title("삼성전자 고가 예측 (2023~2025, Random Forest)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
