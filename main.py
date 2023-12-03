from PyQt6.QtCore import QSize, QCoreApplication
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Eeman")
        self.setFixedSize(QSize(500, 300))
        self.setup_ui()

    def setup_ui(self):
        btn = QPushButton("Yes", self)
        btn.resize(100, 50)
        btn.move(50, 200)
        btn.clicked.connect(QCoreApplication.instance().quit)


def run():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()


if __name__ == "__main__":
    run()
