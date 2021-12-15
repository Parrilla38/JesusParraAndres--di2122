from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QVBoxLayout
from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton
from PySide6.QtGui import Qt
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calculadora')
        self.widgetCentral = QWidget(self)
        self.LayoutGeneral = QVBoxLayout(self.widgetCentral)
        self.setCentralWidget(self.widgetCentral)
        self.widgetCentral.setLayout(self.LayoutGeneral)

        self.display = QLineEdit()
        self.display.setFixedHeight(35)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.LayoutGeneral.addWidget(self.display)

        self.almacen = ""
        self.comprobador_parentesis = True

        buttonsLayout = QGridLayout()
        buttons = {
            'AC': (0, 0),
            '()': (0, 1),
            '%': (0, 2),
            '/': (0, 3),
            '7': (1, 0),
            '8': (1, 1),
            '9': (1, 2),
            '*': (1, 3),
            '4': (2, 0),
            '5': (2, 1),
            '6': (2, 2),
            '+': (2, 3),
            '1': (3, 0),
            '2': (3, 1),
            '3': (3, 2),
            '-': (3, 3),
            '0': (4, 0),
            '.': (4, 1),
            '<-': (4, 2),
            '=': (4, 3),
                    }
        for btn_text in buttons.keys():
            button = QPushButton(btn_text)
            button.setFixedSize(40, 40)
            buttonsLayout.addWidget(
                button, 
                buttons[btn_text][0],
                buttons[btn_text][1]
            )
            button.clicked.connect(self.operacion)

        self.LayoutGeneral.addLayout(buttonsLayout)

    def operacion(self):
        if (self.sender().text() == "="):
            self.setDisplayText(str(eval(self.almacen)))
        elif (self.sender().text() == "<-"):
            self.setDisplayText(self.almacen[:-1])
            self.almacen = self.almacen[:-1]
        elif (self.sender().text() == "AC"):
            self.clearDisplay()
        elif (self.sender().text() == "()"):
            if (self.comprobador_parentesis):
                self.almacen += "("
                self.comprobador_parentesis = False
            elif (not self.comprobador_parentesis):
                self.almacen += ")"
                self.comprobador_parentesis = True
        else:
            self.almacen += self.sender().text()
        self.setDisplayText(self.almacen)

    def setDisplayText(self, text):
        self.display.setText(text)
        self.display.setFocus()

    def displayText(self):
        return self.display.text()

    def clearDisplay(self):
        self.setDisplayText("")
        self.almacen = ""


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
