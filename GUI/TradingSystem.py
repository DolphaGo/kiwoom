import sys
from datetime import datetime, time

from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QTextBrowser, QPushButton, QLineEdit
from pykrx import stock

from 국내주식.주식기본정보요청 import fn_ka10001


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("gui.ui", self)

        # UI에서 요소 찾은 후 변수에 저장
        self.textboard = self.findChild(QTextBrowser, 'textboard')
        self.buysell_log = self.findChild(QTextBrowser, 'buysell_log')
        self.button_start = self.findChild(QPushButton, 'button_start')
        self.button_stop = self.findChild(QPushButton, 'button_stop')
        self.code_list = self.findChild(QLineEdit, 'code_list')
        self.k_value = self.findChild(QLineEdit, 'k_value')

        # 보유 종목 저장
        self.bought = set()

        # 타이머 설정
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.trading)

        # 버튼 이벤트 연결
        self.button_start.clicked.connect(self.start)
        self.button_stop.clicked.connect(self.stop)

    def start(self):
        self.textboard.append("📡 변동성 돌파 전략 시작...")
        self.timer.start(3000)

    def stop(self):
        self.timer.stop()
        self.textboard.append("⛔ 전략 중단됨.")
        self.bought.clear()

    def trading(self):
        now = datetime.now()
        current_time = now.strftime("[%H:%M:%S]")

        # 1. K값
        try:
            k = float(self.k_value.text())
        except ValueError:
            self.textboard.append("⚠️ K 값을 올바르게 입력해주세요.")
            return

        codes = [c.strip() for c in self.code_list.text().split(",") if c.strip()]
        today = now.strftime("%Y%m%d")
        prev_day = stock.get_nearest_business_day_in_a_week(today, prev=True)

        for code in codes:
            try:
                # 2. 전일 데이터 가져오기
                df = stock.get_market_ohlcv_by_date(prev_day, prev_day, code)
                if df.empty:
                    continue

                prev_high = df.iloc[0]['고가']
                prev_low = df.iloc[0]['저가']
                prev_close = df.iloc[0]['종가']
                target = prev_close + (prev_high - prev_low) * k

                # 3. 현재가 조회
                name, current_price = fn_ka10001(code)
                current_price = float(str(current_price).replace(",", "").strip())

                self.textboard.append(
                    f"{current_time} [{code}] [{name}] 현재가: {current_price} / 목표가: {round(target, 2)}"
                )

                # 4. 매수 조건
                if current_price > target and code not in self.bought and now.time() < time(15, 0):
                    self.buy_stock(code, name, current_price)

                # 5. 15시 이후 매도 조건
                if code in self.bought and now.time() >= time(15, 0):
                    self.sell_stock(code, name, current_price)

            except Exception as e:
                self.textboard.append(f"⚠️ [{code}] 오류 발생: {e}")

    def buy_stock(self, code: str, name: str, price: float):
        self.bought.add(code)
        self.buysell_log.append(f"[매수] [{code}] [{name}] [{price}] [1]")

    def sell_stock(self, code: str, name: str, price: float):
        self.bought.remove(code)
        self.buysell_log.append(f"[매도] [{code}] [{name}] [{price}] [1]")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
