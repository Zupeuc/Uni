import numpy as np
import datetime
import random
from productos import *
from variables import *


class Persona:

    def __init__(self, nombre, apellido, edad):
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad

    def __str__(self):
        return self.nombre+' '+self.apellido

    def __repr__(self):
        return self.nombre + ' ' + self.apellido

class MiembroUc(Persona):

    def __init__(self, nombre, apellido, edad, vendedores):
        Persona.__init__(self, nombre, apellido, edad)
        self.vendedores = vendedores.split(' - ')
        self._tiempo_llegada = datetime.timedelta(0, 0, 0, 0, 0, 11) + \
                               datetime.timedelta(0, 0, 0, 0, int(np.random.triangular(0, 30, 240)), 0)
        self.a = random.randint(0, 100)

        """El siguiente codigo separa los horarios en los cuales almuerza cada persona :)"""
        if self.a < DISTRIBUCION_Y:  # Reemplazar luego por variable culiá
            hora = min(max(datetime.timedelta(0, 0, 0, 0, 10 + int(np.random.normal(0, 10)), 12),
                           datetime.timedelta(0, 0, 0, 0, 0, 12)), datetime.timedelta(0, 0, 0, 0, 0, 14))
            if hora <= self._tiempo_llegada:
                self.horario = self.tiempo_llegada + datetime.timedelta(0, 0, 0, 0, 10, 0)
            else:
                self.horario = hora
        elif self.a < DISTRIBUCION_X:
            hora = min(max(datetime.timedelta(0, 0, 0, 0, 10 + int(np.random.normal(0, 10)), 13),
                           datetime.timedelta(0, 0, 0, 0, 0, 13)), datetime.timedelta(0, 0, 0, 0, 0, 15))
            if hora <= self._tiempo_llegada:
                self.horario = self._tiempo_llegada + datetime.timedelta(0, 0, 0, 0, 10, 0)
            else:
                self.horario = hora
        else:
            hora = min(max(datetime.timedelta(0, 0, 0, 0, 10 + int(np.random.normal(0, 10)), 14),
                           datetime.timedelta(0, 0, 0, 0, 0, 14)), datetime.timedelta(0, 0, 0, 0, 0, 16))
            if hora <= self._tiempo_llegada:
                self.horario = self._tiempo_llegada + datetime.timedelta(0, 0, 0, 0, 10, 0)
            else:
                self.horario = hora
        self._traslado = self.horario + TRASLADO_ALUMNOS


    def modificar_horario(self):
        """Tuve que crear esta funcion para modificar los horarios de llegada y que
        no se solapen los tiempos, me demoré mucho en darme cuenta de esto, casi me vuelvo loco jaja"""
        if self.a < DISTRIBUCION_Y:  # Reemplazar luego por variable culiá
            hora = min(max(datetime.timedelta(0, 0, 0, 0, 10 + int(np.random.normal(0, 10)), 12),
                           datetime.timedelta(0, 0, 0, 0, 0, 12)), datetime.timedelta(0, 0, 0, 0, 0, 14))
            if hora <= self._tiempo_llegada:
                self.horario = self.tiempo_llegada + datetime.timedelta(0, 0, 0, 0, 10, 0)
            else:
                self.horario = hora
        elif self.a < DISTRIBUCION_X:
            hora = min(max(datetime.timedelta(0, 0, 0, 0, 10 + int(np.random.normal(0, 10)), 13),
                           datetime.timedelta(0, 0, 0, 0, 0, 13)), datetime.timedelta(0, 0, 0, 0, 0, 15))
            if hora <= self._tiempo_llegada:
                self.horario = self._tiempo_llegada + datetime.timedelta(0, 0, 0, 0, 10, 0)
            else:
                self.horario = hora
        else:
            hora = min(max(datetime.timedelta(0, 0, 0, 0, 10 + int(np.random.normal(0, 10)), 14),
                           datetime.timedelta(0, 0, 0, 0, 0, 14)), datetime.timedelta(0, 0, 0, 0, 0, 16))
            if hora <= self._tiempo_llegada:
                self.horario = self._tiempo_llegada + datetime.timedelta(0, 0, 0, 0, 10, 0)
            else:
                self.horario = hora
        self._traslado = self.horario + datetime.timedelta(0, 0, 0, 0, int(abs(random.expovariate(0.33))), 0)

    @property
    def traslado(self):
        # self._traslado = self.horario + datetime.timedelta(0, 0, 0, 0, min(random.expovariate(0.33), 3*(0.33)), 0)
        return self._traslado

    @property
    def tiempo_llegada(self):
        return self._tiempo_llegada

    @tiempo_llegada.setter
    def tiempo_llegada(self, valor):
        self._tiempo_llegada = valor


class Alumno(MiembroUc):

    def __init__(self, nombre, apellido, edad, vendedores):
        MiembroUc.__init__(self, nombre, apellido, edad, vendedores)
        self.dinero = MESADA_DIA()
        self.paciencia = PACIENCIA()
        self.paciencia_cola = INIT_PACIENCIA     # SOLO PARA EFECTOS DE INIT
        self.hambre = INIT_HAMBRE    # SOLO PARA EFECTOS DE INIT


class Funcionario(MiembroUc):

    def __init__(self, nombre, apellido, edad, vendedores):
        MiembroUc.__init__(self, nombre, apellido, edad, vendedores)
        self.dinero = DINERO_FUNCIONARIOS


class Externo(Persona):
    pass


class Vendedor(Externo):

    def __init__(self, nombre, apellido, edad, comidas):
        Persona.__init__(self, nombre, apellido, edad)
        self.comidas = comidas
        self._tiempo_llegada = LLEGADA_VENDEDORES()
        self.atencion = ATENCION_VENDEDORES()
        self.proxima_atencion = PROXIMA_ATENCION
        self.cola_alumnos = []
        self.cola_funcionarios = []
        self.permiso = PROB_PERMISO
        self.stock = STOCK_VENDEDORES()
        if self.comidas == 'China ':
            self.lista_productos = productos_chinos()
        elif self.comidas == 'Snack ':
            self.lista_productos = productos_snacks()
        elif self.comidas == 'Mexicana ':
            self.lista_productos = productos_mexicanos()
        self.nostock = 0
        self.susto = 0


    def disponibilidad_stock(self):
        if self.stock > len(self.cola_alumnos) + len(self.cola_funcionarios):
            return True
        else:
            return False

    @property
    def tiempo_llegada(self):
        return self._tiempo_llegada

    @tiempo_llegada.setter
    def tiempo_llegada(self, valor):
        self._tiempo_llegada = valor

    def puedo_comprar(self, dinero):
        """Retorna True si el consumidor target tiene dinero suficiente para comprarle al vendedor"""
        a = list(filter(lambda x: x.precio <= dinero, self.lista_productos))
        if len(a) > 0:
            return True
        else:
            return False

    def producto_azar(self, dinero):
        """"Obtiene un producto al azar de la lista de productos que puede vender al alumno"""
        lista = list(filter(lambda x: x.precio <= dinero, self.lista_productos))
        return(random.choice(lista))


    def producto_calidoso(self, dinero):
        """Obtiene el producto de mejor caldiad para venderslo al funcionario"""
        lista = list(filter(lambda x: x.precio <= dinero, self.lista_productos))
        maxi = max([i.calidad_neta for i in lista])
        return list(filter(lambda x: x.calidad_neta == maxi, self.lista_productos))[0]

    def sin_stock(self):
        pass

    def __str__(self):
        return self.nombre + ' ' + self.apellido

    def __repr__(self):
        return self.nombre + ' ' + self.apellido


class Carabinero(Externo):

    def __init__(self, nombre, apellido, edad, personalidad):
        Persona.__init__(self, nombre, apellido, edad)
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.personalidad = personalidad
        self.tiempo_fisco = datetime.timedelta(0, 0, 0, 0, 0, 13)
        self.tiempo_final = datetime.timedelta(0, 0, 0, 0, 40, 13)
        self.siguiente_revision = datetime.timedelta(0, 0, 0, 0, 0, 13)
        if self.personalidad == 'Dr. Jekyll ':
            self.tasa_productos = TASA_JECKYL
            self.engano = PROB_JECKYL
        elif self.personalidad == 'Mr. Hyde ':
            self.tasa_productos = TASA_HYDE
            self.engano = PROB_JECKYL

    def tiempo_fiscalizar(self, n):     # A este le entregamos la property cantidad_vendedores
        return datetime.timedelta(0, 0, 0, 0, int(40/n), 0)

