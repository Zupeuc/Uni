import csv
from personas import Funcionario, Alumno, Carabinero, Vendedor


def leer_personas():

    read = open('personas.csv', 'r', encoding='utf-8')
    reader = csv.reader((line.replace('; ', ';') for line in read), delimiter=';')
    gen = filter(lambda x: x[0] != 'Nombre', reader)
    return gen


def leer_parametros():

    read = open('parametros_iniciales.csv', 'r', encoding='utf-8')
    reader = csv.reader((line.replace(' ', '') for line in read), delimiter=',')
    firstline = next(reader)
    secondline = next(reader)
    return {firstline[i]: secondline[i] for i in range(len(firstline))}


def filtrar_personas(tipo):
    return filter(lambda x: x[4] == tipo, leer_personas())


def guardar_alumnos():
    return [Alumno(i[0], i[1], i[2], i[3]) for i in filtrar_personas('Alumno')]


def guardar_funcionarios():
    return [Funcionario(i[0], i[1], i[2], i[3]) for i in filtrar_personas('Funcionario')]


def guardar_carabineros():
    return [Carabinero(i[0], i[1], i[2], i[6]) for i in filtrar_personas('Carabinero')]


def guardar_vendedores():
    return [Vendedor(i[0], i[1], i[2], i[5]) for i in filtrar_personas('Vendedor')]


def guardar_jeckyl():
    return list(filter(lambda x: x.personalidad == 'Dr. Jekyll ', guardar_carabineros()))


def guardar_hyde():
    return list(filter(lambda x: x.personalidad == 'Mr. Hyde ', guardar_carabineros()))

#for i in leer_personas():
#    print(i)