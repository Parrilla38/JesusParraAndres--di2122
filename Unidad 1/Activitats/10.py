## Definix una llista i utilitzant filter, que la separe en dues llistes, una amb els elements parells i l’altra
## amb els senars.


lista_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def numero_par(numero):
    if numero % 2 == 0:
        return True
    

def numero_impar(numero):
    if numero % 2 != 0:
        return True


comprabador_pares = filter(numero_par, lista_nums)
comprabador_impares = filter(numero_impar, lista_nums)

lista_pares = list(comprabador_pares)
lista_impares = list(comprabador_impares)

print(f"Lista impares:  {lista_impares}")
print(f"Lista pares:  {lista_pares}")
