## Crea una aplicació que vaja llegint operacions d’un fitxer (una operació per línia) i
## afegisca els resultats. Per exemple, si llig: 4 + 4
## Haurà de generar: 4 + 4 = 8
import os
from posixpath import dirname
base_url = os.path.dirname(__file__)


def leer_archivo(archivo):
    contenido = archivo.read()
    return contenido

def escribir_archivo(archivo, texto):
    archivo.write(texto)

def leerNumeros(archivo, archivo2):
    suma = 0
    linea = archivo.readline()
    lineanueva = ""


    while(linea):
        nuevalinea = linea.split()

        if (nuevalinea[1] == "+"):
            suma = int(nuevalinea[0]) + int(nuevalinea[2])
            lineanueva = nuevalinea[0] + " + " + nuevalinea[2] + " = " + str(suma)
            archivo2.write(lineanueva)
            linea = archivo.readline()
        
        if (nuevalinea[1] == "-"):
            resta = int(nuevalinea[0]) - int(nuevalinea[2])
            lineanueva = nuevalinea[0] + " - " + nuevalinea[2] + " = " + str(resta)
            archivo2.write(lineanueva)
            linea = archivo.readline()

        if (nuevalinea[1] == "*"):
            mult = int(nuevalinea[0]) * int(nuevalinea[2])
            lineanueva = nuevalinea[0] + " * " + nuevalinea[2] + " = " + str(mult)
            archivo2.write(lineanueva)
            linea = archivo.readline()

        if (nuevalinea[1] == "/"):
            div = int(nuevalinea[0]) / int(nuevalinea[2])
            lineanueva = nuevalinea[0] + " / " + nuevalinea[2] + " = " + str(div)
            archivo2.write(lineanueva)
            linea = archivo.readline()

        
        archivo2.write("\n")
    

# inicia bucle infinito para leer línea a línea
archivo = open(os.path.join(base_url, "f.txt"), "r")
archivo2 = open(os.path.join(base_url, "f2.txt"), "w")
leerNumeros(archivo, archivo2)

