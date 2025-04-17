from pykrx import stock
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# 설정
ticker = "005930"
train_start = "20230101"
train_end = "20250131"
test_start = "20250201"
test_end = "20250228"

# 데이터 로딩
train_df = stock.get_market_ohlcv_by_date(train_start, train_end, ticker)
test_df = stock.get_market_ohlcv_by_date(test_start, test_end, ticker)

# 전처리 함수
def make_data_with_high(df):
    df_shifted = df.shift(1).dropna()
    X = df_shifted[['시가', '고가', '저가', '종가', '거래량']]
    y = df['고가'].iloc[1:]
    return X, y

def make_data_without_high(df):
    df_shifted = df.shift(1).dropna()
    X = df_shifted[['시가', '저가', '종가', '거래량']]
    y = df['고가'].iloc[1:]
    return X, y

# 데이터 준비
X_train_1, y_train = make_data_with_high(train_df)
X_test_1, y_test = make_data_with_high(test_df)

X_train_2, _ = make_data_without_high(train_df)
X_test_2, _ = make_data_without_high(test_df)

# 모델 학습 및 예측
model1 = RandomForestRegressor(n_estimators=100, random_state=42)
model1.fit(X_train_1, y_train)
pred1 = model1.predict(X_test_1)

model2 = RandomForestRegressor(n_estimators=100, random_state=42)
model2.fit(X_train_2, y_train)
pred2 = model2.predict(X_test_2)

# 평가
mse1 = mean_squared_error(y_test, pred1)
r2_1 = r2_score(y_test, pred1)

mse2 = mean_squared_error(y_test, pred2)
r2_2 = r2_score(y_test, pred2)

# 결과 출력
result = pd.DataFrame({
    '모델': ['고가 포함', '고가 미포함'],
    'MSE': [mse1, mse2],
    'R2 Score': [r2_1, r2_2]
})

print("\n📊 모델 성능 비교:")
print(result)