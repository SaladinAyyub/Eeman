from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QLabel,
)

import sys
import setup


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Eeman")
        self.setFixedSize(500, 300)
        self.setStyleSheet("background-color: darkblue")
        self.setup_ui()

    def setup_ui(self):
        ask_location_label = QLabel("Do you want to set automatic location ?")
        ask_location_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(ask_location_label)
        location_yes_btn = QPushButton("Yes", self)
        location_yes_btn.resize(100, 50)
        location_yes_btn.move(50, 200)
        location_no_btn = QPushButton("No", self)
        location_no_btn.resize(100, 50)
        location_no_btn.move(350, 200)
        location_yes_btn.clicked.connect(self.auto_location)

    def auto_location(self):
        setup.get_location_auto()
        print(setup.city, setup.country)


def run():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()


if __name__ == "__main__":
    run()
