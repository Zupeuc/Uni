import random
import numpy as np


def aparicion_enemigos(valor):
    if valor == 1:
        lambdax = 1/10
    elif valor == 2:
        lambdax = 1/8
    elif valor == 3:
        lambdax = 1/6
    elif valor == 4:
        lambdax = 1/4
    elif valor == 5:
        lambdax = 1/2
    return random.expovariate(lambdax)


def tamano_enemigos(valor):
    if valor == 1:
        a = 1
        b = 5
        c = 1
    elif valor == 2:
        a = 1
        b = 6
        c = 3
    elif valor == 3:
        a = 3
        b = 7
        c = 5
    elif valor == 4:
        a = 5
        b = 9
        c = 7
    elif valor == 5:
        a = 7
        b = 10
        c = 9
    return int(np.random.triangular(a, c, b))


def leer_historial():
    read = open('highscores.txt', 'r')
    diccionario = {}
    for line in read:
        line = line.strip('\n')
        lista = line.split(';')
        diccionario[lista[0]] = int(lista[1])
    return diccionario


def entregar_top(diccionario):
    lista = []
    lista2 = []
    dicto = {}
    for key in diccionario.keys():
        lista.append(diccionario[key])
    if len(lista) < 10:
        largo = len(lista)
    else:
        largo = 10
    for i in range(largo):
        lista2.append(max(lista))
        lista.remove(max(lista))
    filtro = filter(lambda x: diccionario[x] in lista2, diccionario.keys())
    for valor in filtro:
        dicto[valor] = diccionario[valor]
    return dicto


def escribir_puntaje(nombre, puntaje):
    file = open('highscores.txt', 'a')
    file.write(str(nombre)+';'+str(puntaje)+"\n")

