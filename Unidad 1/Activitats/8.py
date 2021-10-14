## Fes una aplicació que imprimisca els primers 100 números imparells.
contador = 0

while contador < 101:
    contador += 1
    if contador % 2 != 0:
        print(contador)