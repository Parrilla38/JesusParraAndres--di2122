# Modifica el codi de l’activitat 11 per a que no es produïsquen errors en l’execució, ja siga
# per introdïur valor no definits per a lesfuncions, valors que no són numèrics o operacions desconegudes.
# Controla també que no es produïsquen errors en la lectura/escriptura dels arxius.
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

            try:
                suma = int(nuevalinea[0]) + int(nuevalinea[2])
            except ValueError:
                print("El valor debe de ser numerico")
            lineanueva = nuevalinea[0] + " + " + nuevalinea[2] + " = " + str(suma)
            archivo2.write(lineanueva)
            linea = archivo.readline()
        
        if (nuevalinea[1] == "-"):

            try:
                resta = int(nuevalinea[0]) - int(nuevalinea[2])
            except ValueError:
                print("El valor debe de ser numerico")
            lineanueva = nuevalinea[0] + " - " + nuevalinea[2] + " = " + str(resta)
            archivo2.write(lineanueva)
            linea = archivo.readline()

        if (nuevalinea[1] == "*"):

            try:
                mult = int(nuevalinea[0]) * int(nuevalinea[2])
            except ValueError:
                print("El valor debe de ser numerico")
            
            lineanueva = nuevalinea[0] + " * " + nuevalinea[2] + " = " + str(mult)
            archivo2.write(lineanueva)
            linea = archivo.readline()

        if (nuevalinea[1] == "/"):

            try:
                div = int(nuevalinea[0]) / int(nuevalinea[2])
            except ZeroDivisionError:
                print("No se puede dividir entre cero")
            lineanueva = nuevalinea[0] + " / " + nuevalinea[2] + " = " + str(div)
            archivo2.write(lineanueva)
            linea = archivo.readline()

        
        archivo2.write("\n")
    

# inicia bucle infinito para leer línea a línea
try:
    archivo = open(os.path.join(base_url, "f.txt"), "r")
    archivo2 = open(os.path.join(base_url, "f2.txt"), "w")
except FileNotFoundError:
    print("No se puede encontrar el archivo")

leerNumeros(archivo, archivo2)

