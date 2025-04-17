import sys
from datetime import datetime

from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QTextBrowser, QPushButton, QLineEdit

from 국내주식.주식기본정보요청 import fn_ka10001


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("gui.ui", self)

        # UI에서 요소 찾은 후 변수에 저장
        self.textboard = self.findChild(QTextBrowser, 'textboard')
        self.button_start = self.findChild(QPushButton, 'button_start')
        self.button_stop = self.findChild(QPushButton, 'button_stop')
        self.code_list = self.findChild(QLineEdit, 'code_list')

        # 타이머 설정
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_prices)

        # 버튼 이벤트 연결
        self.button_start.clicked.connect(self.start)
        self.button_stop.clicked.connect(self.stop)

    def start(self):
        self.textboard.append("📡 실시간 조회 시작...")
        self.timer.start(1000)  # 1초마다 호출

    def stop(self):
        self.timer.stop()
        self.textboard.append("⛔ 실시간 조회 중단됨.")

    def update_prices(self):
        codes = [c.strip() for c in self.code_list.text().split(",") if c.strip()]
        now = datetime.now().strftime("[%H:%M:%S]")
        for code in codes:
            name, price = fn_ka10001(code)
            log = f"{now} [{code}] [{name}] [{price}]"
            self.textboard.append(log)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
