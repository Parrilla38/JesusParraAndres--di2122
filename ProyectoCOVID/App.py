from cProfile import label
from trace import Trace
from PySide6.QtCore import QPointF
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QLineEdit, QHBoxLayout
from PySide6.QtWidgets import QWidget, QPushButton, QComboBox, QVBoxLayout, QToolBar
from PySide6.QtGui import Qt, QAction, QPainter, QPen
from PySide6.QtCharts import (QAreaSeries, QBarSet, QChart, QChartView,
                              QLineSeries, QPieSeries, QScatterSeries,
                              QSplineSeries, QStackedBarSeries, QBarCategoryAxis)
import sys
import os
import sqlite3 
from sqlite3 import Error
import csv

carpeta = os.path.dirname(__file__)

try:
    sqliteConnection = sqlite3.connect(carpeta + '/db')
    cursor = sqliteConnection.cursor()
    print("Conectado a la base de datos")
except Error as error:
    print("Error al conectar con la base de datos", error)
    
    
class VentanaERROR(QMainWindow):
    
    def __init__(self):
        super(VentanaERROR, self).__init__()

        self.setWindowTitle("ERROR")

        self.widget = QWidget()

        self.layoutHorizontal = QHBoxLayout()
        self.layoutVertical = QVBoxLayout()
        self.setLayout(self.layoutVertical)
        self.label = QLabel("El usuario o la contraseña introducidos no son correctos")
        self.layoutVertical.addWidget(self.label)
        

        self.buttonConnect = QPushButton("Aceptar")
        self.buttonConnect.setStatusTip("Aceptar")
        self.buttonConnect.clicked.connect(self.cerrarApp)
        self.layoutHorizontal.addWidget(self.buttonConnect)
        
        self.layoutVertical.addLayout(self.layoutHorizontal)
        self.widget.setLayout(self.layoutVertical)

        self.setStatusTip("Usuario Default")
        self.setCentralWidget(self.widget)

    def cerrarApp(self):
        self.close()
        log.show()
    
class LoginWindow(QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()

        self.setWindowTitle("Login Window")
        self.widget = QWidget()
        self.layout = QVBoxLayout()
        self.layoutHorizontal = QHBoxLayout()

        self.usuario = QLineEdit()
        self.usuario.setPlaceholderText("Usuario")
        self.usuariol = QLabel("Usuario")
        self.layout.addWidget(self.usuariol)
        self.layout.addWidget(self.usuario)
        
        self.contraseña = QLineEdit()
        self.contraseña.setPlaceholderText("Contraseña")
        self.contraseñal = QLabel("Password")
        self.contraseña.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.contraseñal)
        self.layout.addWidget(self.contraseña)

        self.conectar = QPushButton("Conectar")
        self.conectar.setStatusTip("Conectar")
        self.conectar.clicked.connect(self.conectarapp)
        self.layoutHorizontal.addWidget(self.conectar)

        self.cancelar = QPushButton("Cancelar")
        self.cancelar.setStatusTip("Cancelar")
        self.cancelar.clicked.connect(self.cerrarapp)
        self.layoutHorizontal.addWidget(self.cancelar)
        
        self.layout.addLayout(self.layoutHorizontal)
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        self.error_w = VentanaERROR()
        
    def conectarapp(self):
        self.close()

        cursor.execute("""SELECT user,pass FROM datos WHERE user=? AND pass=?""",
                        (self.usuario.text(), self.contraseña.text()))

        result = cursor.fetchone()
        if result:
            window.show()
        else:
            print("El usuario o la contraseña introducidos son incorrectos")
            self.error_w.show()

    def cerrarapp(self):
        self.close()



class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('APP COVID COMUNIDAD VALENCIANA')
        
        self.widget = QWidget()
        self.LayoutHorizontal = QHBoxLayout()
        self.layoutHorizontal2 = QHBoxLayout()
        self.LayoutVertical = QVBoxLayout()
        self.LayoutVertical.addLayout(self.LayoutHorizontal)
        self.LayoutVertical.addLayout(self.layoutHorizontal2)

        
        
        ''' MENÚ COVID'''
        self.toolbar = QToolBar("Menu")
        self.addToolBar(self.toolbar)


        self.Total = QAction("Total", self)
        self.Total.setStatusTip("Total Covid")
        self.Total.triggered.connect(self.totalcovid)

        self.Casos = QAction("PCR+", self)
        self.Casos.setStatusTip("PCR COVID")
        self.Casos.triggered.connect(self.pcrcovid)
        
        self.Incidencias = QAction("Incidencias", self)
        self.Incidencias.setStatusTip("Incidencias COVID")
        self.Incidencias.triggered.connect(self.incidenciascovid)
        
        self.Fallecidos = QAction("Fallecidos", self)
        self.Fallecidos.setStatusTip("Fallecidos COVID")
        self.Fallecidos.triggered.connect(self.fallecidoscovid)
        
        self.tasafallecidos = QAction("Tasa Fallecidos", self)
        self.tasafallecidos.setStatusTip("Tasa Fallecidos COVID")
        self.tasafallecidos.triggered.connect(self.tasacovid)
        
        self.toolbar.addAction(self.Total)
        self.toolbar.addAction(self.Casos)
        self.toolbar.addAction(self.Incidencias)
        self.toolbar.addAction(self.Fallecidos)
        self.toolbar.addAction(self.tasafallecidos)

        ''' MENÚ DE SELECCIÓN'''
        self.spais = QLabel("Seleccionar País")
        self.spais.setAlignment(Qt.AlignCenter)
        self.LayoutHorizontal.addWidget(self.spais)
        
        self.pais = QComboBox()
        self.pais.setFixedWidth(200)
        self.pais.addItem('España')
        self.pais.setEnabled(False)
        self.pais.setCurrentText("España")
        self.LayoutHorizontal.addWidget(self.pais)   
        
        self.sprovincia = QLabel("Seleccionar Provincia")
        self.sprovincia.setAlignment(Qt.AlignCenter)
        self.LayoutHorizontal.addWidget(self.sprovincia)
        
        self.provincia = QComboBox()
        self.provincia.setFixedWidth(200)
        self.provincia.addItem("Comunidad Valenciana")
        self.provincia.setEnabled(False)
        self.provincia.setCurrentText("Comunidad Valenciana")
        self.LayoutHorizontal.addWidget(self.provincia)
        
        self.smunicipio = QLabel("Seleccionar Municipio")
        self.smunicipio.setAlignment(Qt.AlignCenter)
        self.LayoutHorizontal.addWidget(self.smunicipio)
        
        self.municipio = QComboBox()
        self.municipio.setFixedWidth(200)
        self.municipio.setEditable(True)
        self.municipio.setEnabled(False)
        self.LayoutHorizontal.addWidget(self.municipio)
        
        ''' BUSQUEDA POR TIEMPO
        
       
        self.tiempo = QComboBox()
        self.tiempo.setFixedWidth(100)
        self.tiempo.addItem('1 Semana')
        self.tiempo.addItem('1 Mes')
        self.LayoutHorizontal.addWidget(self.tiempo) '''
        
        
        ''' BOTON CAMBIO GRAFICO TOTAL '''
        
        ''' BOTON TOTAL PCR 1'''
        self.ctotal = QPushButton("Cambiar a Gráfico Redondo")

        self.ctotal.setFixedWidth(400)
        self.ctotal.setFixedHeight(25)
        self.ctotal.setVisible(False)
        self.ctotal.setEnabled(False)
        self.ctotal.clicked.connect(self.totalcovid)
        
        self.LayoutVertical.addWidget(self.ctotal)
        
        ''' BOTON TOTAL PCR 2'''
        self.ctotal2 = QPushButton("Cambiar a Gráfico Largo")

        self.ctotal2.setFixedWidth(400)
        self.ctotal2.setFixedHeight(25)
        self.ctotal2.setVisible(False)
        self.ctotal2.setEnabled(False)
        self.ctotal2.clicked.connect(self.totalcovid2)

        self.LayoutVertical.addWidget(self.ctotal2)
        
        ''' BOTONES DE BÚSQUEDA'''
        
        ''' BOTON TOTAL PCR '''
        self.busqueda1 = QPushButton("Buscar")

        self.busqueda1.setFixedWidth(100)
        self.busqueda1.setFixedHeight(25)
        self.busqueda1.setVisible(True)
        self.busqueda1.setEnabled(False)
        self.busqueda1.clicked.connect(self.mostrarpcr)

        self.LayoutHorizontal.addWidget(self.busqueda1)
        
        
        ''' BOTON INCIDENCIAS'''
        self.busqueda2 = QPushButton("Buscar")

        self.busqueda2.setFixedWidth(100)
        self.busqueda2.setFixedHeight(25)
        self.busqueda2.setVisible(False)
        self.busqueda2.clicked.connect(self.mostrarincidencia)

        self.LayoutHorizontal.addWidget(self.busqueda2)
        
        
        ''' BOTON FALLECIDOS'''
        self.busqueda3 = QPushButton("Buscar")

        self.busqueda3.setFixedWidth(100)
        self.busqueda3.setFixedHeight(25)
        self.busqueda3.setVisible(False)
        self.busqueda3.clicked.connect(self.mostrarfallecidos)

        self.LayoutHorizontal.addWidget(self.busqueda3)
        
        
        ''' BOTON TASA FALLEICOD'''
        self.busqueda4 = QPushButton("Buscar")

        self.busqueda4.setFixedWidth(100)
        self.busqueda4.setFixedHeight(25)
        self.busqueda4.setVisible(False)
        self.busqueda4.clicked.connect(self.mostrartasa)

        self.LayoutHorizontal.addWidget(self.busqueda4)
        
        ''' LABEL TEXTO DATOS '''
        
        self.informacion = QLabel()

        self.informacion.setFixedHeight(130)
        self.informacion.setFixedWidth(1000)
        self.informacion.setText('PANTALLA DE DATOS SOBRE EL COVID' + '\n' +
                                 'Seleccione arriba a la izquierda el apartado que desea ' + '\n' +
                                 'para continuar')

        self.font = self.informacion.font()
        self.font.setPointSize(15)
        self.font.setBold(True)
        self.informacion.setFont(self.font)
        
        
        ''' RELLENAR COMBOBOX MUNICIPIOS'''
        with open(
            carpeta + '/extras/covid/30d/03.csv', mode = 'r', encoding ='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file,  delimiter=";")
            contador = 0
            for line in csv_reader:
                if (contador == 0):
                    contador += 1
                else:
                    self.municipio.addItem(line[1])
                    
                    
        self.label2 = QLabel()
        self.font.setPointSize(14)
        self.label2.setFont(self.font)
        self.label2.setText("APP COVID DE LA COMUNIDAD VALENCIANA")

        self.label2.setFixedHeight(500)
        self.label2.setFixedWidth(500)
        self.label2.setAlignment(Qt.AlignCenter)
        self.layoutHorizontal2.addWidget(self.label2)   

        self.graphWidget = QChartView()
        self.graphWidget.setFixedHeight(300)
        self.graphWidget.setFixedWidth(900)

        self.LayoutVertical.addWidget(self.informacion)

        self.widget.setLayout(self.LayoutVertical)
        self.setCentralWidget(self.widget)
        
    def totalcovid(self):
        
        self.municipio.setEnabled(False)
        self.busqueda1.setEnabled(False)
        self.busqueda2.setEnabled(False)
        self.busqueda3.setEnabled(False)
        self.busqueda4.setEnabled(False)
        self.ctotal.setVisible(False)
        self.ctotal2.setVisible(True)
        self.ctotal.setEnabled(False)
        self.ctotal2.setEnabled(True)

        with open(
            
            carpeta + '/extras/covid/total_gva_covid19.csv', mode = 'r', encoding ='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file)
            contador = 0

            for line in csv_reader:
                if contador == 0:
                    pcr = line[0]
                elif contador == 2:
                    hospitalizados = line[0]
                elif contador == 4:
                    altas = line[0]
                elif contador == 5:
                    fallecidos = line[0]
                contador += 1

            self.informacion.setText(
                'INFORMACIÓN TOTAL SOBRE EL COVID EN LA COMUNIDAD VALENCIANA:' + '\n' +
                "PCR+: " + pcr + "\n"
                + "Incidencias: " + altas + "\n"
                + "Fallecidos: " + fallecidos + "\n"
                + "Hospitalizados: " + hospitalizados + "\n"
            )
            
        self.layoutHorizontal2.removeWidget(self.label2)
        self.layoutHorizontal2.removeWidget(self.graphWidget)
        self.graphWidget.close()

        self.graphWidget = QChartView(self.graficoredondo_total())
        self.graphWidget.setRenderHint(QPainter.Antialiasing)
        self.layoutHorizontal2.addWidget(self.graphWidget)

    def totalcovid2(self):
        
        self.municipio.setEnabled(False)
        self.busqueda1.setEnabled(False)
        self.busqueda2.setEnabled(False)
        self.busqueda3.setEnabled(False)
        self.busqueda4.setEnabled(False)
        self.ctotal.setVisible(True)
        self.ctotal2.setVisible(False)
        self.ctotal.setEnabled(True)
        self.ctotal2.setEnabled(False)
        
        self.layoutHorizontal2.removeWidget(self.label2)
        self.layoutHorizontal2.removeWidget(self.graphWidget)
        self.graphWidget.close()

        self.graphWidget = QChartView(self.grafico_total())
        self.graphWidget.setRenderHint(QPainter.Antialiasing)
        self.layoutHorizontal2.addWidget(self.graphWidget)
        
        
        
    def pcrcovid(self):
    
        self.municipio.setEnabled(True)
        
        self.busqueda1.setEnabled(True)
        self.busqueda1.setVisible(True)
        
        self.busqueda2.setEnabled(False)
        self.busqueda2.setVisible(False)
        
        self.busqueda3.setEnabled(False)
        self.busqueda3.setVisible(False)
        
        self.busqueda4.setEnabled(False)
        self.busqueda4.setVisible(False)
        
        self.ctotal.setVisible(False)
        self.ctotal2.setVisible(False)
        self.ctotal.setEnabled(False)
        self.ctotal2.setEnabled(False)
        
        self.informacion.setText(
                'INTRODUZCA EL MUNICIPIO PARA SABER LAS PCR+:' + '\n' +
                "PCR+: " + ' ' + "\n"
            )
        
        self.graphWidget.close()
        self.layoutHorizontal2.addWidget(self.label2)
        
        
        
            
    def mostrarpcr(self):
        
        with open(
            
            carpeta + '/extras/covid/30d/31.csv' , mode = 'r', encoding ='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                if line[1] == self.municipio.currentText():
                    pcr = line[2]

            self.informacion.setText(
                'INFORMACIÓN PCR+ COVID EN ' + self.municipio.currentText() + '\n' +
                "ÚLTIMAS PCR+: " + pcr 
            )
            
        
        self.layoutHorizontal2.removeWidget(self.label2)
        self.layoutHorizontal2.removeWidget(self.graphWidget)
        self.graphWidget.close()

        self.graphWidget = QChartView(self.grafico_pcr())
        self.graphWidget.setRenderHint(QPainter.Antialiasing)
        self.layoutHorizontal2.addWidget(self.graphWidget)
            
    def incidenciascovid(self):
        
        self.municipio.setEnabled(True)
        
        self.busqueda1.setEnabled(False)
        self.busqueda1.setVisible(False)
        
        self.busqueda2.setEnabled(True)
        self.busqueda2.setVisible(True)
        
        self.busqueda3.setEnabled(False)
        self.busqueda3.setVisible(False)
        
        self.busqueda4.setEnabled(False)
        self.busqueda4.setVisible(False)
        
        self.ctotal.setVisible(False)
        self.ctotal2.setVisible(False)
        self.ctotal.setEnabled(False)
        self.ctotal2.setEnabled(False)
        
        self.informacion.setText(
                'INTRODUZCA EL MUNICIPIO PARA SABER LAS INCIDENCIAS POR COVID:' + '\n' +
                "INCIDENCIAS: " + ' ' + "\n"
            )
        
        self.graphWidget.close()
        self.layoutHorizontal2.addWidget(self.label2)

        
            
    def mostrarincidencia(self):
        
        with open(
            
            carpeta + '/extras/covid/30d/31.csv' , mode = 'r', encoding ='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                if line[1] == self.municipio.currentText():
                    incidencia = line[5]

            self.informacion.setText(
                'INFORMACIÓN INCIDENCIAS COVID EN ' + self.municipio.currentText() + '\n' +
                "ÚLTIMAS INCIDENCIAS: " + incidencia 
            )
            
        self.layoutHorizontal2.removeWidget(self.label2)
        self.layoutHorizontal2.removeWidget(self.graphWidget)
        self.graphWidget.close()

        self.graphWidget = QChartView(self.grafico_incidencias())
        self.graphWidget.setRenderHint(QPainter.Antialiasing)
        self.layoutHorizontal2.addWidget(self.graphWidget)
            
    def fallecidoscovid(self):
        
        self.municipio.setEnabled(True)
        
        self.busqueda1.setEnabled(False)
        self.busqueda1.setVisible(False)
        
        self.busqueda2.setEnabled(False)
        self.busqueda2.setVisible(False)
        
        self.busqueda3.setEnabled(True)
        self.busqueda3.setVisible(True)
        
        self.busqueda4.setEnabled(False)
        self.busqueda4.setVisible(False)
        
        self.ctotal.setVisible(False)
        self.ctotal2.setVisible(False)
        self.ctotal.setEnabled(False)
        self.ctotal2.setEnabled(False)
        
        self.informacion.setText(
                'INTRODUZCA EL MUNICIPIO PARA SABER LOS FALLECIDOS POR COVID:' + '\n' +
                "FALLECIDOS: " + ' ' + "\n"
            )

        self.graphWidget.close()
        self.layoutHorizontal2.addWidget(self.label2)
            
    def mostrarfallecidos(self):
        
        with open(
            
            carpeta + '/extras/covid/30d/31.csv' , mode = 'r', encoding ='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                if line[1] == self.municipio.currentText():
                    fallecidos = line[6]

            self.informacion.setText(
                'INFORMACIÓN FALLECIDOS POR COVID EN ' + self.municipio.currentText() + '\n' +
                "ÚLTIMOS FALLECIDOS: " + fallecidos 
            )
            
        self.layoutHorizontal2.removeWidget(self.label2)
        self.layoutHorizontal2.removeWidget(self.graphWidget)
        self.graphWidget.close()

        self.graphWidget = QChartView(self.grafico_fallecidos())
        self.graphWidget.setRenderHint(QPainter.Antialiasing)
        self.layoutHorizontal2.addWidget(self.graphWidget)
            
    def tasacovid(self):
        
        self.municipio.setEnabled(True)
        
        self.busqueda1.setEnabled(False)
        self.busqueda1.setVisible(False)
        
        self.busqueda2.setEnabled(False)
        self.busqueda2.setVisible(False)
        
        self.busqueda3.setEnabled(False)
        self.busqueda3.setVisible(False)
        
        self.busqueda4.setEnabled(True)
        self.busqueda4.setVisible(True)
        
        self.ctotal.setVisible(False)
        self.ctotal2.setVisible(False)
        self.ctotal.setEnabled(False)
        self.ctotal2.setEnabled(False)
        
        self.informacion.setText(
                'INTRODUZCA EL MUNICIPIO PARA SABER LA TASA DE DEFUNCION DE COVID:' + '\n' +
                "TASA DE DEFUNCIÓN: " + ' ' + '%' + "\n"
            )

        self.graphWidget.close()
        self.layoutHorizontal2.addWidget(self.label2)
            
    def mostrartasa(self):
        
        with open(
            
            carpeta + '/extras/covid/30d/31.csv' , mode = 'r', encoding ='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                if line[1] == self.municipio.currentText():
                    tasa = line[7]

            self.informacion.setText(
                'INFORMACIÓN TASA DE DEFUNCIÓN COVID EN ' + self.municipio.currentText() + '\n' +
                "ÚLTIMA TASA DE DEFUNCIÓN: " + tasa + '%'
            )
            
        self.layoutHorizontal2.removeWidget(self.label2)
        self.layoutHorizontal2.removeWidget(self.graphWidget)
        self.graphWidget.close()

        self.graphWidget = QChartView(self.grafico_tasa())
        self.graphWidget.setRenderHint(QPainter.Antialiasing)
        self.layoutHorizontal2.addWidget(self.graphWidget)
            
    ''' GRÁFICO TOTAL COVID '''
    
    def grafico_total(self):
    
        self.bar1 = QBarSet("PCR+")
        self.bar2 = QBarSet("Incidencias")
        self.bar3 = QBarSet("Fallecidos")
        self.bar4 = QBarSet("Hospitalizados")

        self.categorias = ["PCR+", "Incidencias",
                           "Fallecidos", "Hospitalizados"]

        with open(
            carpeta + '/extras/covid/total_gva_covid19.csv' , mode = 'r', encoding ='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file)

            for i, data in enumerate(csv_reader):
                if (i == 0):
                    self.bar1.append([int(data[0]), 0, 0, 0])
                if (i == 4):
                    self.bar2.append([0, int(data[0]), 0, 0])
                if (i == 5):
                    self.bar3.append([0, 0, int(data[0]), 0])
                if (i == 2):
                    self.bar4.append([0, 0, 0, int(data[0])])

        self.barras_grafico = QStackedBarSeries()
        self.barras_grafico.append(self.bar1)
        self.barras_grafico.append(self.bar2)
        self.barras_grafico.append(self.bar3)
        self.barras_grafico.append(self.bar4)
        
        self.chart = QChart()
        self.chart.addSeries(self.barras_grafico)
        self.chart.setTitle("Gráfico TOTAL COVID")

        self.chart.createDefaultAxes()
        self.chart.removeAxis(self.chart.axisX())

        categorias_axis = QBarCategoryAxis()
        categorias_axis.append(self.categorias)
        self.chart.setAnimationOptions(QChart.AllAnimations)

        return self.chart
    
    ''' GRÁFICO TASA DEFUNCIÓN '''
    
    def grafico_tasa(self):
        
        self.bar1 = QBarSet("0 - 3")
        self.bar2 = QBarSet("3 - 5")
        self.bar3 = QBarSet("5 - 10")
        self.bar4 = QBarSet("10 - 13")
        self.bar5 = QBarSet("13 - 17")
        self.bar6 = QBarSet("17 - 20")
        self.bar7 = QBarSet("20 - 24")
        self.bar8 = QBarSet("24 - 27")
        self.bar9 = QBarSet("27 - 31")

        self.categorias = ["Tasa de Defunción por Días"]

        with open(
            carpeta + '/extras/covid/30dgrafico/03.csv' , mode = 'r', encoding ='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                municipio = self.municipio.currentText().replace(' ','')
                if line[1] == municipio:
                    i = line[7]
                    self.bar1.append([float(i), 0, 0, 0, 0, 0, 0, 0, 0])
                    
                    
        with open(
            carpeta + '/extras/covid/30dgrafico/05.csv' , mode = 'r', encoding ='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                municipio = self.municipio.currentText().replace(' ','')
                if line[1] == municipio:
                    i = line[7]
                    self.bar2.append([0, float(i), 0, 0, 0, 0, 0, 0, 0])
                    
        with open(
            carpeta + '/extras/covid/30dgrafico/10.csv' , mode = 'r', encoding ='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                municipio = self.municipio.currentText().replace(' ','')
                if line[1] == municipio:
                    i = line[7]
                    self.bar3.append([0, 0, float(i), 0, 0, 0, 0, 0, 0])

        with open(
            carpeta + '/extras/covid/30dgrafico/13.csv' , mode = 'r', encoding ='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                municipio = self.municipio.currentText().replace(' ','')
                if line[1] == municipio:
                    i = line[7]
                    self.bar4.append([0, 0, 0, float(i), 0, 0, 0, 0, 0])
        

        with open(
            carpeta + '/extras/covid/30dgrafico/17.csv' , mode = 'r', encoding ='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                municipio = self.municipio.currentText().replace(' ','')
                if line[1] == municipio:
                    i = line[7]
                    self.bar5.append([0, 0, 0, 0, float(i), 0, 0, 0, 0])


        with open(
            carpeta + '/extras/covid/30dgrafico/20.csv' , mode = 'r', encoding ='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                municipio = self.municipio.currentText().replace(' ','')
                if line[1] == municipio:
                    i = line[7]
                    self.bar6.append([0, 0, 0, 0, 0, float(i), 0, 0, 0])


        with open(
            carpeta + '/extras/covid/30dgrafico/24.csv' , mode = 'r', encoding ='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                municipio = self.municipio.currentText().replace(' ','')
                if line[1] == municipio:
                    i = line[7]
                    self.bar7.append([0, 0, 0, 0, 0, 0, float(i), 0, 0])


        with open(
            carpeta + '/extras/covid/30dgrafico/27.csv' , mode = 'r', encoding ='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                municipio = self.municipio.currentText().replace(' ','')
                if line[1] == municipio:
                    i = line[7]
                    self.bar8.append([0, 0, 0, 0, 0, 0, 0, float(i), 0])


        with open(
            carpeta + '/extras/covid/30dgrafico/31.csv' , mode = 'r', encoding ='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                municipio = self.municipio.currentText().replace(' ','')
                if line[1] == municipio:
                    i = line[7]
                    self.bar9.append([0, 0, 0, 0, 0, 0, 0, 0, float(i)])


        self.barras_grafico = QStackedBarSeries()
        self.barras_grafico.append(self.bar1)
        self.barras_grafico.append(self.bar2)
        self.barras_grafico.append(self.bar3)
        self.barras_grafico.append(self.bar4)
        self.barras_grafico.append(self.bar5)
        self.barras_grafico.append(self.bar6)
        self.barras_grafico.append(self.bar7)
        self.barras_grafico.append(self.bar8)
        self.barras_grafico.append(self.bar9)
        
        self.chart = QChart()
        self.chart.addSeries(self.barras_grafico)
        self.chart.setTitle("Gráfico TASA DEFUNCIÓN COVID por Días")

        self.chart.createDefaultAxes()
        self.chart.removeAxis(self.chart.axisX())

        categorias_axis = QBarCategoryAxis()
        categorias_axis.append(self.categorias)
        self.chart.setAnimationOptions(QChart.AllAnimations)

        return self.chart
            
            
    ''' GRÁFICO PCR COVID '''
    
    def grafico_pcr(self):
    
        self.series = QSplineSeries()
        self.chart = QChart()

        with open(
            carpeta + '/extras/covid/30dgrafico/03.csv' , mode = 'r', encoding ='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                municipio = self.municipio.currentText().replace(' ','')
                if line[1] == municipio:
                    pcr = line[2]

            self.series.append(QPointF(0.0, float(pcr)))
            self.series.append(QPointF(3.0, float(pcr)))

        with open(
            carpeta + '/extras/covid/30dgrafico/05.csv' , mode = 'r', encoding ='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                municipio = self.municipio.currentText().replace(' ','')
                if line[1] == municipio:
                    pcr = line[2]

            self.series.append(QPointF(5.0, float(pcr)))

        with open(
            carpeta + '/extras/covid/30dgrafico/10.csv' , mode = 'r', encoding ='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                municipio = self.municipio.currentText().replace(' ','')
                if line[1] == municipio:
                    pcr = line[2]

            self.series.append(QPointF(10.0, float(pcr)))

        with open(
            carpeta + '/extras/covid/30dgrafico/13.csv' , mode = 'r', encoding ='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                municipio = self.municipio.currentText().replace(' ','')
                if line[1] == municipio:
                    pcr = line[2]

            self.series.append(QPointF(13.0, float(pcr)))

        with open(
            carpeta + '/extras/covid/30dgrafico/17.csv' , mode = 'r', encoding ='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                municipio = self.municipio.currentText().replace(' ','')
                if line[1] == municipio:
                    pcr = line[2]

            self.series.append(QPointF(17.0, float(pcr)))

        with open(
            carpeta + '/extras/covid/30dgrafico/20.csv' , mode = 'r', encoding ='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                municipio = self.municipio.currentText().replace(' ','')
                if line[1] == municipio:
                    pcr = line[2]

            self.series.append(QPointF(20.0, float(pcr)))

        with open(
            carpeta + '/extras/covid/30dgrafico/24.csv' , mode = 'r', encoding ='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                municipio = self.municipio.currentText().replace(' ','')
                if line[1] == municipio:
                    pcr = line[2]

            self.series.append(QPointF(24.0, float(pcr)))

        with open(
            carpeta + '/extras/covid/30dgrafico/27.csv' , mode = 'r', encoding ='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                municipio = self.municipio.currentText().replace(' ','')
                if line[1] == municipio:
                    pcr = line[2]

            self.series.append(QPointF(27.0, float(pcr)))

        with open(
            carpeta + '/extras/covid/30dgrafico/31.csv' , mode = 'r', encoding ='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                municipio = self.municipio.currentText().strip()
                if line[1] == municipio:
                    pcr = line[2]

            self.series.append(QPointF(31.0, float(pcr)))

        
        self.chart.legend().hide()
        self.chart.addSeries(self.series)
        self.chart.createDefaultAxes()
        self.chart.setTitle("PCR+")
        self.chart.setAnimationOptions(QChart.AllAnimations)

        return self.chart
    
    ''' GRAFICO INCIDENCIAS COVID '''
    
    def grafico_incidencias(self):
        
        self.series = QScatterSeries()
        self.chart = QChart()

        with open(
            carpeta + '/extras/covid/30dgrafico/03.csv' , mode = 'r', encoding ='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                municipio = self.municipio.currentText().replace(' ','')
                if line[1] == municipio:
                    incidencias = line[5]

            self.series.append(QPointF(0.0, float(incidencias)))
            self.series.append(QPointF(3.0, float(incidencias)))

        with open(
            carpeta + '/extras/covid/30dgrafico/05.csv' , mode = 'r', encoding ='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                municipio = self.municipio.currentText().replace(' ','')
                if line[1] == municipio:
                    incidencias = line[5]

            self.series.append(QPointF(5.0, float(incidencias)))

        with open(
            carpeta + '/extras/covid/30dgrafico/10.csv' , mode = 'r', encoding ='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                municipio = self.municipio.currentText().replace(' ','')
                if line[1] == municipio:
                    incidencias = line[5]

            self.series.append(QPointF(10.0, float(incidencias)))

        with open(
            carpeta + '/extras/covid/30dgrafico/13.csv' , mode = 'r', encoding ='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                municipio = self.municipio.currentText().replace(' ','')
                if line[1] == municipio:
                    incidencias = line[5]

            self.series.append(QPointF(13.0, float(incidencias)))

        with open(
            carpeta + '/extras/covid/30dgrafico/17.csv' , mode = 'r', encoding ='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                municipio = self.municipio.currentText().replace(' ','')
                if line[1] == municipio:
                    incidencias = line[5]

            self.series.append(QPointF(17.0, float(incidencias)))

        with open(
            carpeta + '/extras/covid/30dgrafico/20.csv' , mode = 'r', encoding ='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                municipio = self.municipio.currentText().replace(' ','')
                if line[1] == municipio:
                    incidencias = line[5]

            self.series.append(QPointF(20.0, float(incidencias)))

        with open(
            carpeta + '/extras/covid/30dgrafico/24.csv' , mode = 'r', encoding ='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                municipio = self.municipio.currentText().replace(' ','')
                if line[1] == municipio:
                    incidencias = line[5]

            self.series.append(QPointF(24.0, float(incidencias)))

        with open(
            carpeta + '/extras/covid/30dgrafico/27.csv' , mode = 'r', encoding ='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                municipio = self.municipio.currentText().replace(' ','')
                if line[1] == municipio:
                    incidencias = line[5]

            self.series.append(QPointF(27.0, float(incidencias)))

        with open(
            carpeta + '/extras/covid/30dgrafico/31.csv' , mode = 'r', encoding ='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                municipio = self.municipio.currentText().replace(' ','')
                if line[1] == municipio:
                    incidencias = line[5]

            self.series.append(QPointF(31.0, float(incidencias)))

        
        self.chart.legend().hide()
        self.chart.addSeries(self.series)
        self.chart.createDefaultAxes()
        self.chart.setTitle("Incidencias")
        self.chart.setAnimationOptions(QChart.AllAnimations)

        return self.chart
    
    def grafico_fallecidos(self):
        
        self.series = QLineSeries()
        self.chart = QChart()

        with open(
            carpeta + '/extras/covid/30dgrafico/03.csv' , mode = 'r', encoding ='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                municipio = self.municipio.currentText().replace(' ','')
                if line[1] == municipio:
                    fallecidos = line[6]

            self.series.append(QPointF(0.0, float(fallecidos)))
            self.series.append(QPointF(3.0, float(fallecidos)))

        with open(
            carpeta + '/extras/covid/30dgrafico/05.csv' , mode = 'r', encoding ='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                municipio = self.municipio.currentText().replace(' ','')
                if line[1] == municipio:
                    fallecidos = line[6]

            self.series.append(QPointF(5.0, float(fallecidos)))

        with open(
            carpeta + '/extras/covid/30dgrafico/10.csv' , mode = 'r', encoding ='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                municipio = self.municipio.currentText().replace(' ','')
                if line[1] == municipio:
                    fallecidos = line[6]

            self.series.append(QPointF(10.0, float(fallecidos)))

        with open(
            carpeta + '/extras/covid/30dgrafico/13.csv' , mode = 'r', encoding ='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                municipio = self.municipio.currentText().replace(' ','')
                if line[1] == municipio:
                    fallecidos = line[6]

            self.series.append(QPointF(13.0, float(fallecidos)))

        with open(
            carpeta + '/extras/covid/30dgrafico/17.csv' , mode = 'r', encoding ='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                municipio = self.municipio.currentText().replace(' ','')
                if line[1] == municipio:
                    fallecidos = line[6]

            self.series.append(QPointF(17.0, float(fallecidos)))

        with open(
            carpeta + '/extras/covid/30dgrafico/20.csv' , mode = 'r', encoding ='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                municipio = self.municipio.currentText().replace(' ','')
                if line[1] == municipio:
                    fallecidos = line[6]

            self.series.append(QPointF(20.0, float(fallecidos)))

        with open(
            carpeta + '/extras/covid/30dgrafico/24.csv' , mode = 'r', encoding ='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                municipio = self.municipio.currentText().replace(' ','')
                if line[1] == municipio:
                    fallecidos = line[6]

            self.series.append(QPointF(24.0, float(fallecidos)))

        with open(
            carpeta + '/extras/covid/30dgrafico/27.csv' , mode = 'r', encoding ='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                municipio = self.municipio.currentText().replace(' ','')
                if line[1] == municipio:
                    fallecidos = line[6]

            self.series.append(QPointF(27.0, float(fallecidos)))

        with open(
            carpeta + '/extras/covid/30dgrafico/31.csv' , mode = 'r', encoding ='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            for line in csv_reader:
                municipio = self.municipio.currentText().replace(' ','')
                if line[1] == municipio:
                    fallecidos = line[6]

            self.series.append(QPointF(31.0, float(fallecidos)))

        
        self.chart.legend().hide()
        self.chart.addSeries(self.series)
        self.chart.createDefaultAxes()
        self.chart.setTitle("Fallecidos")
        self.chart.setAnimationOptions(QChart.AllAnimations)

        return self.chart
    
    
    def graficoredondo_total(self):
        self.series = QPieSeries()

        with open(
            carpeta + '/extras/covid/total_covid.csv' , mode = 'r', encoding ='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")
            
            for line in csv_reader:
                pcr = line[0]
                incidencias = line[1]
                fallecidos = line[2]
                hospitalizados = line[4]
           
           
            self.series.append('PCR+: ' + pcr, 4)
            self.series.append('Incidencias: ' + incidencias, 3)
            self.series.append('Fallecidos: ' + fallecidos, 1)
            self.series.append('Hospitalizados: ' + hospitalizados, 2)

        self.slice = self.series.slices()[0]
        self.slice.setExploded()
        self.slice.setLabelVisible()
        self.slice.setPen(QPen(Qt.black, 2))
        self.slice.setBrush(Qt.green)
        
        
        self.slice = self.series.slices()[1]
        self.slice.setExploded()
        self.slice.setLabelVisible()
        self.slice.setPen(QPen(Qt.black, 2))
        self.slice.setBrush(Qt.red)
        
        self.slice = self.series.slices()[2]
        self.slice.setExploded()
        self.slice.setLabelVisible()
        self.slice.setPen(QPen(Qt.black, 2))
        self.slice.setBrush(Qt.yellow)
        
        self.slice = self.series.slices()[3]
        self.slice.setExploded()
        self.slice.setLabelVisible()
        self.slice.setPen(QPen(Qt.black, 2))
        self.slice.setBrush(Qt.blue)

        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.setTitle('Gráfico TOTAL COVID')
        self.chart.legend().hide()

        self._chart_view = QChartView(self.chart)
        self._chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart.setAnimationOptions(QChart.AllAnimations)

        return self.chart
    
app = QApplication(sys.argv)
window = MainWindow()
log = LoginWindow()
log.show()
app.exec()