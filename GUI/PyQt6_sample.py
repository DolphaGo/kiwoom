import sys

from PyQt6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QHBoxLayout


def main():
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("PyQt6 Sample")
    window.setGeometry(100, 100, 300, 200)

    label = QLabel('Hello, PyQt6!')

    lineEdit = QLineEdit()

    button = QPushButton('Click me')
    button.clicked.connect(lambda: label.setText(lineEdit.text()))

    hbox = QHBoxLayout()
    hbox.addWidget(lineEdit)
    hbox.addWidget(button)

    vbox = QVBoxLayout(window)
    vbox.addWidget(label)
    vbox.addLayout(hbox)

    window.setLayout(vbox)
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
