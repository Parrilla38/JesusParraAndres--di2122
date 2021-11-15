from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from PySide6.QtGui import QScreen
from PySide6.QtCore import QSize

from config import t_max, t_min, t_norm, b_x, b_y

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)


        # Tamaño de la pantalla
        self.my_screen = QScreen.availableGeometry(QApplication.primaryScreen())

        self.setMaximumSize(t_max)
        self.setMinimumSize(t_min)
        
        self.setWindowTitle("Exemple signals-slots 1")
        
        self.pybutton = QPushButton('Maximizar', self)
        self.pybutton2 = QPushButton('Normalitza', self)
        self.pybutton3 = QPushButton('Minimizar', self)
        
        #Connectem la senyal clicked a la ranura button_pressed
        self.pybutton.clicked.connect(self.button_pressedmax)     
        self.pybutton2.clicked.connect(self.button_pressednormal)
        self.pybutton3.clicked.connect(self.button_pressedmin)
        
        self.pybutton.resize(b_x, b_y)
        self.pybutton2.resize(b_x, b_y)
        self.pybutton3.resize(b_x, b_y)
           
           
        self.cambia_tam(t_norm)
        self.setFixedSize(t_norm)

        
        

    def cambia_tam(self, tam):
        
        self.move((self.my_screen.width() - tam.width()) / 2, (self.my_screen.height() - tam.height()) / 2)
        self.pybutton.move((tam.width() / 5) - (b_x / 2), (tam.height() / 2) - (b_y / 2))
        self.pybutton2.move((tam.width() / 2) - (b_x / 2), (tam.height() / 2) - (b_y / 2))
        self.pybutton3.move((tam.width() / 1.25) - (b_x / 2), (tam.height() / 2) - (b_y / 2))


    def button_pressedmax(self):

        self.setWindowTitle("Maximizado")
        self.setFixedSize(t_max)
        self.cambia_tam(t_max)
        
        self.pybutton.setEnabled(False)
        self.pybutton2.setEnabled(True)
        self.pybutton3.setEnabled(True)
        
            
    def button_pressednormal(self):

        self.setWindowTitle("Normal")
        self.setFixedSize(t_norm)
        self.cambia_tam(t_norm)
        
        self.pybutton.setEnabled(True)
        self.pybutton2.setEnabled(False) 
        self.pybutton3.setEnabled(True)

        
    def button_pressedmin(self):

        self.setWindowTitle("Minimizado")
        self.setFixedSize(t_min)
        self.cambia_tam(t_min)
        
        self.pybutton.setEnabled(True)
        self.pybutton2.setEnabled(True)
        self.pybutton3.setEnabled(False)

    

if __name__ == "__main__":
    app = QApplication([])
    mainWin = MainWindow()
    mainWin.show()
    app.exec()