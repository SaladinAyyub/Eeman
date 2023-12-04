from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QLabel,
)

import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Eeman")
        self.setFixedSize(500, 300)
        self.setStyleSheet("background-color: darkblue")
        self.setup_ui()

    def setup_ui(self):
        label = QLabel("Do you want to set automatic location ?")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(label)
        yes_btn = QPushButton("Yes", self)
        yes_btn.resize(100, 50)
        yes_btn.move(50, 200)
        no_btn = QPushButton("No", self)
        no_btn.resize(100, 50)
        no_btn.move(350, 200)


def run():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()


if __name__ == "__main__":
    run()
