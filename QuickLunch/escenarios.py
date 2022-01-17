from simulacion import *


"""Falta implementar el cambio de los parametros de los escenarios, peor ya había programado todo y no se me
ocurrio como hacerlo al final"""


def replicas_escenario(n):
    """Hace n replicas del escneario y guarda todas las estadisticas de cada replica en una lista de replicas"""

    inicio = 0
    lista_replicas = []
    while inicio <= n:

        vendedores = {i.nombre + ' ' + i.apellido: i for i in guardar_vendedores()}
        alumnos = {i.nombre + ' ' + i.apellido: i for i in guardar_alumnos()}
        funcionarios = {i.nombre + ' ' + i.apellido: i for i in guardar_funcionarios()}
        m = Semestre(vendedores, alumnos, funcionarios, False)      #Para que no printee en consola
        lista_replicas.append(m.run())

        inicio += 1

    return lista_replicas


def medida_desempeno(replicas_escenario, medida_desempeno = str):
    """Obitene la sumatoria de la medida de desempeño"""

    sumatoria = 0
    for i in replicas_escenario:
        sumatoria += i[medida_desempeno]
    return sumatoria


def mejor_medida(a, b):
    """Compara cual sumatoria es mayor y tiene mejor desempeño"""

    if a > b:
        return a
    else:
        return b