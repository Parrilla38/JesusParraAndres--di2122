# Anem a implementar un xicotet joc per consola. El programa generarà un número
# aleatori entre 0 i 100 (utilitzeu randint() del mòdul random) i demanarà a l’usuari que introduïsca un
# número.
# Mentre el número siga massa menut, llançarà una excepció ErrorEnterMassaMenut indicant-li-ho. Si
# per contra és massa gran llançarà ErrorEnterMassaGran.
# El joc acabarà quan s’introduïsca un valor no numèric o quan s’introduïsca l’enter buscat, en este cas
# felicitarà a l’usuari. 


import random

class ErrorEnterMassaMenut(Exception):
    "Lanzada cuando el numero es más pequeño que el solicitado"
    pass

class ErrorEnterMassaGran(Exception):
    "Lanzada cuando el numero es más grande que el solicitado"
    pass

numero_random = random.randint(0, 100)

while True:
    try:
        numero_usuario = input("Dona'm un número: ")

        if numero_usuario.isdigit():

            numero_usuario = int(numero_usuario)
            if numero_usuario == numero_random:
                print("Enhorabuena, has ganado el juego, el número escrito coincide con el buscado!!")
                break

            if numero_usuario == 999: ### Funcion de administrador para saber el número
                print(numero_random)
                
            if numero_usuario < numero_random:
                raise ErrorEnterMassaMenut
            
            if numero_usuario > numero_random:
                raise ErrorEnterMassaGran

            
        
        else:
            print("El número introducido debe de ser un número!!")
            break
            
    except ErrorEnterMassaMenut:
        print("El numero es más pequeño que el solicitado!")
        print()

    except ErrorEnterMassaGran:
        print("El numero es más grande que el solicitado!")
        print()

print("Fi del programa")


    



