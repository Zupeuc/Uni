import csv
import random
import datetime
import numpy as np


def leer_parametros():

    read = open('parametros_iniciales.csv', 'r', encoding='utf-8')
    reader = csv.reader((line.replace(' ', '') for line in read), delimiter=',')
    firstline = next(reader)
    secondline = next(reader)
    return {firstline[i]: secondline[i] for i in range(len(firstline))}


def leer_escenarios(n):         # No funciona
    read = open('escenarios.csv', 'r', encoding='utf-8')
    reader = csv.reader((line.replace(' ', '') for line in read), delimiter=',')
    for line in reader:
        if line == 0:
            firstline = line
        if line == n:
            secondline = line
    return {firstline[i]: secondline[i] for i in range(len(firstline))}


"""Cambiar el leer parametros cambiaria todas los parametros de la simulaicon, por lo que cambiando
esto podriamos hacer escenarios distintos, sin embargo no se me ocurrio como hacerlo ya que revise muy tarde
la parte de escenarios en el PDF. De alguna forma habría que cambiar el dict_parametros desde la simulacion misma"""
dict_parametros = leer_parametros()


"""SIMULACION"""
TIEMPO_SIMULACION = datetime.timedelta(0, 0, 0, 0, 0, 8)
TIEMPO_MAX = datetime.timedelta(0, 0, 0, 0, 0, 17)
DIAS_HABILES = 22
MESES = 4


"""PRODUCTOS"""
PUTREFACION_MIN = 0.2

"""Por favor ruego disculpar pep8 por estas funciones ne mayuscula, pero las habia hecho parametros y necesitaba que
variaran y no me dio para cmabiar todo a minuscula"""
def PROBABILDIAD_PUTREFACCION():
    return random.randint(0, 100) < 35

def PROBABILIDAD_PUTREFACCION2():
    return random.randint(0, 100) < 70

"""ALUMNOS"""
MODA_LLEGADA = int(dict_parametros['moda_llegada_campus'])
def ALUMNOS_LLEGADA():
    return datetime.timedelta(0, 0, 0, 0, int(np.random.triangular(0, MODA_LLEGADA, 240)), 11)
TRASLADO_CAMPUS = float(dict_parametros['traslado_campus'])
TRASLADO_ALUMNOS = datetime.timedelta(0, 0, 0, 0, int(abs(random.expovariate(TRASLADO_CAMPUS))), 0)

BASE_MESADA = int(dict_parametros['base_mesada'])
def MESADA():
    return int(BASE_MESADA * (1 + (random.random()**random.random())) * 20)
def MESADA_DIA():
    return int(MESADA() / 20)

LIMITE_PACIENCIA = dict_parametros['limite_paciencia'].split(';')
def PACIENCIA():
    return datetime.timedelta(0, 0, 0, 0, random.randint(int(LIMITE_PACIENCIA[0]), int(LIMITE_PACIENCIA[1])), 0)
INIT_PACIENCIA = datetime.timedelta(12, 0, 0, 0, 0, 0)
INIT_HAMBRE = 0

"""FUNCIONARIOS"""
DINERO_FUNCIONARIOS = int(dict_parametros['dinero_funcionarios'])
DISTRIBUCION_X = int((dict_parametros['distribución_almuerzo']).split(';')[0])
DISTRIBUCION_Y = int((dict_parametros['distribución_almuerzo']).split(';')[1])

"""VENDEDORES"""
def LLEGADA_VENDEDORES():
    return datetime.timedelta(0, 0, 0, 0, int(np.random.normal(0, 30)), 11)

SUSTO = int(dict_parametros['días_susto'])
RAPIDEZ_VENDEDORES = dict_parametros['rapidez_vendedores'].split(';')
PROB_PERMISO = float(dict_parametros['probabilidad_permiso'])

def ATENCION_VENDEDORES():
    return datetime.timedelta(0, 0, 0, 0, random.randint(int(RAPIDEZ_VENDEDORES[0]), int(RAPIDEZ_VENDEDORES[1])), 0)

PROXIMA_ATENCION = datetime.timedelta(0, 0, 0, 0, 0, 20)

OBTENER_STOCK = dict_parametros['stock_vendedores'].split(';')

def STOCK_VENDEDORES():
    return random.randint(int(OBTENER_STOCK[0]), int(OBTENER_STOCK[1]))

"""EVENTOS NO PROGRAMADOS"""

def P_CONCHA():
    return int(100*float(dict_parametros['concha_estéreo']))
DIAS_SIN_CONCHA = 20

def DIAS_EXTREMOS():
    return random.randint(2, 20)

def PROB_EXTREMOS():
    return (DIAS_EXTREMOS() / 30)*100 >= random.randint(0, 100)

def LLAMADA_PACOS():
    return (random.expovariate(float(dict_parametros['llamado_policial'])))

def PROBABILIDAD_PACOS():
    return LLAMADA_PACOS() >= random.randint(1, 50)

def prob_hamburguesas(n):
    return -int(random.expovariate(1/(1 / 21 - n)))

"""CARABINEROS"""

JECKYL = dict_parametros['personalidad_jekyll'].split(';')
TASA_JECKYL = JECKYL[0]
PROB_JECKYL = JECKYL[1]
HYDE = dict_parametros['personalidad_hide'].split(';')
TASA_HYDE = HYDE[0]
PROB_HYDE = HYDE[1]



