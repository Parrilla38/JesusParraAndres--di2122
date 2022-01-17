from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QLineEdit, QHBoxLayout
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QStatusBar, QStackedLayout
from PySide6.QtGui import QAction
import sys


class Login(QWidget):
    """
    Login class
    """
    def __init__(self, user):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Conectado como usuario " + user)
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.btn = QPushButton("Logout")
        self.btn.setEnabled(True)
        layout.addWidget(self.btn)
        self.btn.clicked.connect(self.logout)

        self.btn2 = QPushButton("Salir")
        self.btn2.setEnabled(True)
        layout.addWidget(self.btn2)
        self.btn2.clicked.connect(self.salir)

    def logout(self):
        self.hide()
        self.w = MainWindow()
        self.w.show()

    def salir(self):
        app.closeAllWindows()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('App Login')

        self.widget = QWidget()
        self.LayoutHorizontal = QHBoxLayout()
        self.LayoutVertical = QVBoxLayout()
        self.LayoutVertical.addLayout(self.LayoutHorizontal)

        # APARTADO DEL USUARIO
        self.usertext = QLabel("Usuario")
        self.LayoutVertical.addWidget(self.usertext)
        self.user = QLineEdit(self.widget)
        self.user.setMaxLength(15)
        self.user.setPlaceholderText("Introduce el usuario:")
        self.user.setText("")
        self.LayoutVertical.addWidget(self.user)

        self.userpass = QLabel("Contraseña")
        self.LayoutVertical.addWidget(self.userpass)
        self.passw = QLineEdit(self.widget)
        self.passw.setEchoMode(QLineEdit.Password)
        self.passw.setMaxLength(15)
        self.passw.setPlaceholderText("Introduce la contraseña:")
        self.passw.setText("")
        self.LayoutVertical.addWidget(self.passw)

        # Boton para hacer login
        self.btn = QPushButton("Login")
        self.btn.setEnabled(True)
        self.LayoutVertical.addWidget(self.btn)
        self.btn.clicked.connect(
            lambda x: self.comprobar_user(self.user.text(),
                                          self.passw.text()))

        # Barra del Menu
        menu = self.menuBar()
        file_menu = menu.addMenu("&Menú")

        # Opcion para cerrar la Aplicación
        button_action2 = QAction("Salir", self)
        button_action2.setStatusTip("Salir de la aplicación")
        button_action2.triggered.connect(self.cerrarApp)

        self.setStatusBar(QStatusBar(self))
        file_menu.addAction(button_action2)

        # Stacked Layout para almacenar el login y las interfaces de los usuarios

        self.widget.setLayout(self.LayoutVertical)
        self.setCentralWidget(self.widget)

    def comprobar_user(self, user, password):
        if (user == "admin" or user == "user" and password == "1234"):
            self.show_new_window(user)
            self.hide()

    def cerrarApp(self):
        app.closeAllWindows()

    def show_new_window(self, user):
        self.w = Login(user)
        self.w.show()


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()