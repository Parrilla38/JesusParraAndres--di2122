import sys
import argparse

parser = argparse.ArgumentParser();
parser.add_argument('-t', "--title", help='Title of application')
parser.add_argument('-b', "--button-text", help='Buttpn text')
parser.add_argument('-f', "--fixed-size", help="Window fixed size")
parser.add_argument('-s', "--size", help='Size for Windows')

args = parser.parse_args()



from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton

class MainWindow(QMainWindow):
    def __init__(self, title="Title", button_text="Text"):
        super().__init__()

        self.setWindowTitle(title)

        button = QPushButton(button_text)

        self.setFixedSize(QSize(600, 150))

        self.setCentralWidget(button)


app = QApplication(sys.argv)

if (len(sys.argv) == 3):
    window = MainWindow(sys.argv[1], sys.argv[2])
else:
    window = MainWindow()

window.show()

app.exec()