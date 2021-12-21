from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow, QLineEdit, QVBoxLayout
from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QStatusBar, QDialogButtonBox, QLabel, QDialog
from PySide6.QtGui import Qt, QAction
import sys
import os

directorio = os.path.dirname(__file__)

# Clase QDialog para mostrar la ventana de confirmar cierre


class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("ALERTA!")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("Estás seguro de que quieres cerrar la aplicación?")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calculadora')

        # Widget y Layout de uso General
        self.widgetCentral = QWidget(self)
        self.LayoutGeneral = QVBoxLayout(self.widgetCentral)
        self.setCentralWidget(self.widgetCentral)
        self.widgetCentral.setLayout(self.LayoutGeneral)

        # Barra de operaciones de la Calculadora
        self.display = QLineEdit()
        self.display.setFixedHeight(35)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.LayoutGeneral.addWidget(self.display)

        # Variable para guardar las operaciones
        self.almacen = ""
        # Variable para guardar las operaciones más la solucion
        self.almacen_solucion = ""
        # Variable para guardar la carpeta de las operaciones
        self.carpeta = ""
        # Variable para comprobar si se cierra o se abre el parentesis
        self.comprobador_parentesis = True

        # Creacion de botones de la calculadora (Normal)
        self.buttons = {}
        self.buttonsLayout = QGridLayout()
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
        for btn_text, pos in buttons.items():
            self.buttons[btn_text] = QPushButton(btn_text)
            self.buttons[btn_text].setFixedSize(40, 40)
            self.buttons[btn_text].setShortcut(btn_text)
            self.buttonsLayout.addWidget(self.buttons[btn_text],
                                         pos[0], pos[1])
            self.buttons[btn_text].clicked.connect(self.operacion)

        self.LayoutGeneral.addLayout(self.buttonsLayout)
        self.buttons['='].clicked.connect(self.result)
        self.buttons['='].clicked.connect(self.guardarSalida)

        # Creacion de botones de la calculadora (Cientifica)
        self.buttons2 = {}
        self.buttonsLayout_cientifica = QGridLayout()
        buttons2 = {
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
            'log': (5, 0),
            'exp': (5, 1),
            'mod': (5, 2),
            'ln': (5, 3),
                    }
        for btn_text2, pos2 in buttons2.items():
            self.buttons2[btn_text2] = QPushButton(btn_text2)
            self.buttons2[btn_text2].setFixedSize(40, 40)
            self.buttons2[btn_text2].setShortcut(btn_text2)
            self.buttonsLayout_cientifica.addWidget(self.buttons2[btn_text2],
                                                    pos2[0], pos2[1])
            self.buttons2[btn_text2].clicked.connect(self.operacion)

        self.buttons2['='].clicked.connect(self.result)
        self.buttons2['='].clicked.connect(self.guardarSalida)
        self.calculadora_cientifica = False

        # Creacion de menu de opciones
        menu = self.menuBar()
        # Opcion para la calculadora cientifica
        self.button_action = QAction("&Cientifica", self)
        self.button_action.setStatusTip("Calculadora Cientifica")
        self.button_action.triggered.connect(self.comprobadorCalculadora)

        # Opcion para cerrar la calculadora
        button_action2 = QAction("Cerrar", self)
        button_action2.setStatusTip("Cerrar calculadora")
        button_action2.triggered.connect(self.cerrarCalculadora)

        # Opcion para guardar datos
        self.button_checkbox = QAction("&Guardar datos", self)
        self.button_checkbox.setCheckable(True)
        self.button_checkbox.triggered.connect(self.seleccionar_ruta)
        self.button_checkbox.triggered.connect(self.guardarSalida)

        self.setStatusBar(QStatusBar(self))

        # Añadiendo todos los QAction al menú
        file_menu = menu.addMenu("&Menú")
        file_menu.addAction(self.button_action)
        file_menu.addSeparator()
        file_menu.addAction(button_action2)
        file_menu.addSeparator()
        file_menu.addAction(self.button_checkbox)

    # Funcion para comprobar todas las operaciones de la calculadora
    def operacion(self):
        if (self.sender().text() == "="):
            self.almacen_solucion = self.almacen + " = " + str((eval(self.almacen)))
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

    # Funcion para devolver el resultado de la operacion
    def result(self):
        self.setDisplayText(str(eval(self.almacen)))

    # Funcion para mostrar por pantalla el resultado
    def setDisplayText(self, text):
        self.display.setText(text)
        self.display.setFocus()

    # Funcion para devolver el resultado que hay mostrado por pantalla
    def displayText(self):
        return self.display.text()

    # Funcion para borrar la pantalla
    def clearDisplay(self):
        self.setDisplayText("")
        self.almacen = ""
        self.almacen_solucion = ""

    # Funcion para crear la Calculadora Cientifica
    def cientifica(self):
        self.setWindowTitle('Calculadora Cientifica')
        self.buttons2 = {}
        self.buttonsLayout_cientifica = QGridLayout()
        buttons2 = {
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
            'log': (5, 0),
            'exp': (5, 1),
            'mod': (5, 2),
            'ln': (5, 3),
                    }
        for btn_text2, pos2 in buttons2.items():
            self.buttons2[btn_text2] = QPushButton(btn_text2)
            self.buttons2[btn_text2].setFixedSize(40, 40)
            self.buttons2[btn_text2].setShortcut(btn_text2)
            self.buttonsLayout_cientifica.addWidget(self.buttons2[btn_text2],
                                                    pos2[0], pos2[1])
            self.buttons2[btn_text2].clicked.connect(self.operacion)

        self.buttons2['='].clicked.connect(self.result)
        self.buttons2['='].clicked.connect(self.guardarSalida)
        self.LayoutGeneral.addLayout(self.buttonsLayout_cientifica)

    # Funcion para crear la Calculadora Normal
    def normal(self):
        self.setWindowTitle('Calculadora')
        self.buttons = {}
        self.buttonsLayout = QGridLayout()
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
        for btn_text, pos in buttons.items():
            self.buttons[btn_text] = QPushButton(btn_text)
            self.buttons[btn_text].setFixedSize(40, 40)
            self.buttons2[btn_text].setShortcut(btn_text)
            self.buttonsLayout.addWidget(self.buttons[btn_text],
                                         pos[0], pos[1])
            self.buttons[btn_text].clicked.connect(self.operacion)

        self.buttons['='].clicked.connect(self.result)
        self.buttons['='].clicked.connect(self.guardarSalida)
        self.LayoutGeneral.addLayout(self.buttonsLayout)

    # Funcion para cerrar la calculadora
    def cerrarCalculadora(self):
        dlg = CustomDialog(self)
        if dlg.exec():
            app.closeAllWindows()
        else:
            pass

    # Funcion para comprobar que calculadora ha solicitado el usuario
    def comprobadorCalculadora(self):
        if not(self.calculadora_cientifica):
            self.calculadora_cientifica = True
            self.button_action.setText("Normal")
            for i in reversed(range(self.buttonsLayout.count())):
                self.buttonsLayout.itemAt(i).widget().setParent(None)
            self.cientifica()

        elif(self.calculadora_cientifica):
            self.calculadora_cientifica = False
            self.button_action.setText("Cientifica")

            for i in reversed(range(self.buttonsLayout_cientifica.count())):
                self.buttonsLayout_cientifica.itemAt(i).widget().setParent(None)
            self.normal()

    # Funcion para guardar las operaciones en un fichero externo
    def guardarSalida(self):
        if (self.button_checkbox.isChecked()):
            try:
                # He intentado hacer el os path pero no me funciona
                # with open(os.path.join(directorio("filePath.txt", 'a+'))) as f:
                with open(self.carpeta, 'a+') as f:
                    f.write(self.almacen_solucion)
                    f.write("\n")
                    f.close()
            except FileNotFoundError as e:
                return e
            except IOError as e:
                return e
        else:
            pass

    # Funcion para seleccionar el fichero donde guardar la informacion
    def seleccionar_ruta(self):
        ruta_archivo = QFileDialog.getOpenFileName(self, "Abrir Archivo", "", "Text Files (*.txt)")
        if ruta_archivo:
            self.carpeta = ruta_archivo[0]


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
