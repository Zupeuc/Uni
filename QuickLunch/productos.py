import csv
import math
import datetime



class Producto:

    def __init__(self, nombre, tipo, precio, calorias, putrefaccion):
        self.nombre = nombre
        self.tipo = tipo
        self.precio = int(precio)
        self.calorias = int(calorias)
        self.tasa_putrefaccion = int(putrefaccion)
        self._tiempo = datetime.timedelta(0, 0, 0, 0, 0, 0)
        self.calidad_neta = self.calorias / self.precio**(4/5)
        self.tasita = 1
        self.tasa_calidad = 1
        #self._calidad = 0

    def __repr__(self):
        return self.nombre

    def __str__(self):
        return self.nombre

    @property
    def tiempo(self):
        return self._tiempo

    @tiempo.setter
    def tiempo(self, valor):
        self._tiempo = valor

    @property
    def calidad(self):
        putrefaccion = 1 - math.exp(-(int((self.tiempo.seconds - int(datetime.timedelta(0, 0, 0, 0, 0, 8).seconds))/60)/self.tasa_putrefaccion))
        #self._calidad = ((self.calorias*(1 - putrefaccion))**4)/self.precio**(4/5)
        return self.tasa_calidad*(self.calorias*(1 - (putrefaccion*self.tasita))**4)/self.precio**(4/5)


def leer_productos():

    read = open('productos.csv', 'r', encoding='utf-8')
    reader = csv.reader((line.replace('; ', ';') for line in read), delimiter=';')
    gen = filter(lambda x: x[0] != 'Producto', reader)
    return gen


def productos_mexicanos():
    filtro = filter(lambda x: x[5] == 'Puesto de comida mexicana', leer_productos())
    return [Producto(i[0], i[1], i[2], i[3], i[4]) for i in filtro]

def productos_chinos():
    filtro = filter(lambda x: x[5] == 'Puesto de comida china', leer_productos())
    return [Producto(i[0], i[1], i[2], i[3], i[4]) for i in filtro]

def productos_snacks():
    filtro = filter(lambda x: x[5] == 'Puesto de snacks', leer_productos())
    return [Producto(i[0], i[1], i[2], i[3], i[4]) for i in filtro]
