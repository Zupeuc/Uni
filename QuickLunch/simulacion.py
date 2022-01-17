# Autor: Daniel Zupeuc

from readfiles import *
from quickdevil import *
from variables import *
import numpy as np
import datetime
import random


class Semestre():
    """Esta clase modela el transcurso de todo el semestre"""

    def __init__(self, vendedores, alumnos, funcionarios, Booleano):    # Hay que ingresar un boolano True o False
                                                                        # para ver los prints diarios o no
        self.dias_habiles = DIAS_HABILES
        self.dia_actual = 1
        self.mes_final = MESES
        self.mes_actual = 1
        self.s = Simulacion(vendedores, alumnos, funcionarios)

        """Importante para no printear nada en los escenarios! True, printea, False no"""
        self.s.notestadistica = Booleano
        self.parametros = leer_parametros()
        self.concha = 0
        self.contador_concha = 0

        self.dias_totales = 0
        self.ultima_concha = 0

        self.temperaturas_extremas = 0
        self.ultima_extrema = 0
        self.frio = False
        self.caluroso = False
        self.llamados_carabineros = 0

        self.contador_hamburguesas = 0
        self.lluvia_burgas = False

    def concha_acustica(self):
        """Funcion arma la concha acusta y ajusta valores"""
        print('Se realiza una CONCHA ESTEREO!')
        self.contador_concha += 1
        self.ultima_concha = self.dia_actual
        self.concha = 1
        for vendedor in self.s._dict_vendedores:
            for producto in self.s._dict_vendedores[vendedor].lista_productos:
                producto.precio = producto.precio * (1.25)

    def desarmar_concha(self):
        """Funciona ajusta precios post concha y los vuelve a la normalidad"""
        self.concha = 0
        for vendedor in self.s._dict_vendedores:
            for producto in self.s._dict_vendedores[vendedor].lista_productos:
                producto.precio = producto.precio / (1.25)

    def reset_llegadas(self):
        """Resetea los tiempos de llegada de funcionarios, vendedores y alumnos"""
        for vendedor in self.s._dict_vendedores:
            self.s._dict_vendedores[vendedor].tiempo_llegada = LLEGADA_VENDEDORES()
        for funcionario in self.s.funcionarios:
            self.s.funcionarios[funcionario].tiempo_llegada = ALUMNOS_LLEGADA()
            self.s.funcionarios[funcionario].modificar_horario()
        for alumno in self.s._dict_alumnos:
            self.s._dict_alumnos[alumno].tiempo_llegada = ALUMNOS_LLEGADA()
            self.s._dict_alumnos[alumno].modificar_horario()

    def estadisticas(self):
        print('')
        print('                                     """ESTADISTICAS"""                              ')
        print('')
        print('1. Cantidad promedio de dinero confiscado a los vendedores debido a llegada de carabineros:')
        print('2. Cantidad minima, maxima y promedio por productos vendidos durante un dia:')
        print('3. Cantidad de confiscaciones que realizaron los Hyde: {} y los Keckyl: {}'
              .format(self.s.confiscaciones_hyde, self.s.confiscaciones_jeckyl))
        print('4. EL número de llamadas que realizó Quick Devil a los Carabineros fue: {}'.
              format(self.llamados_carabineros))
        print('5. Número de veces que se realizó la Concha Estereo: {}'.format(self.contador_concha))
        print('6. Número de veces donde hubo Temperaturas extremas: {}'.format(self.temperaturas_extremas))
        print('7. Número de veces donde hubo una Lluvia de hamburguesas: {}'.format(self.contador_hamburguesas))
        print('8.1. Cantidad promedio de personas que almorzó entre las 12:00-12:59: {}'.format(
            str(int(self.s.almuerzo12/self.dias_totales))))
        print('8.2. Cantidad promedio de personas que almorzó entre las 13:00-13:59: {}'.format(
            str(int(self.s.almuerzo13 / self.dias_totales))))
        print('8.3. Cantidad promedio de personas que almorzó entre las 14:00-15:00: {}'.format(
            str(int(self.s.almuerzo14 / self.dias_totales))))
        print('9. Cantidad de alumnos que no almorzaron por mes fue: {}'.format(self.s.alumnos_hambrientos))
        print('10. Calidad promedio de productos de todos los vendedores por escenario fue: {}'
              .format(self.s.stock_totales))
        print('11. La cantidad promedio MiembrosUC que se intoxicaron por vendedor fue: {}'
              .format(self.s.numero_enfermos / 30))
        print('12. Cantidad de Productos que se descompone fue: {}'.format(self.s.numero_enfermos))
        print('13. Cantidad promedio de miembros de la PUC que abandonaron una cola de espera por día fue: {}'
              .format(self.s.cambio_colas / self.dias_totales))
        print('14. Cantidad promedio de vendedores por día que se quedaron sin stock fue: {}'
              .format(str((int(self.s.vendedores_nostock)) / int(self.dias_totales))))
        print('15. Cantidad de veces que se engaño a los carabineros de personalidad Dr. Jekyll: {} y Mr. Hyde: {}'
              .format(self.s.engano_jeckyl, self.s.engano_hide))


    def run(self):

        while self.mes_actual <= self.mes_final:
            if self.s.notestadistica:
                print('########### MES {} ####################'.format(self.mes_actual))

            """Cambio la mesada al principio del mes"""
            for alumno in self.s._dict_alumnos:
                self.s._dict_alumnos[alumno].dinero = MESADA_DIA()


            while self.dia_actual <= self.dias_habiles:

                a = """

                                ############################   DIA HABIL N° {} MES N° {} ############################


                                                    """.format(self.dia_actual, self.mes_actual)
                if self.s.notestadistica:
                    print(a)

                """Cambio la paciencia de los alumnos al principio del dia"""
                for alumno in self.s._dict_alumnos:
                    self.s._dict_alumnos[alumno].paciencia = PACIENCIA()

                """Cambio el stock de los vendedores a principio de cada día"""
                for vendedor in self.s._dict_vendedores:
                    self.s._dict_vendedores[vendedor].stock = STOCK_VENDEDORES()
                    self.s.stock_totales += self.s._dict_vendedores[vendedor].stock

                """Temperaturas Extremas"""
                if PROB_EXTREMOS():
                    if self.s.notestadistica:
                        print('El día presenta temperaturas EXTREMAS!')
                    self.ultima_extrema = self.dias_totales
                    self.temperaturas_extremas += 1
                    valor = random.randint(1, 2)
                    if valor == 1:  # CALUROSO
                        self.caluroso = True
                        for vendedor in self.s._dict_vendedores:
                            for producto in self.s._dict_vendedores[vendedor].lista_productos:
                                producto.tasita = 2
                    elif valor == 2:  # FRIO
                        self.frio = True
                        for vendedor in self.s._dict_vendedores:
                            for producto in self.s._dict_vendedores[vendedor].lista_productos:
                                producto.tasa_calidad = 0.5

                """Lluvia de hamburguesas!"""
                if not self.caluroso and not self.frio:
                    if self.dias_totales - self.ultima_extrema > prob_hamburguesas(
                                    self.dias_totales - self.ultima_extrema) and \
                            self.temperaturas_extremas > 3*self.contador_hamburguesas:
                        if self.s.notestadistica:
                            print('¡¡¡¡LLUVIA DE HAMBURGUESAS!!!!')
                        self.contador_hamburguesas += 1
                        self.lluvia_burgas = True

                if not self.lluvia_burgas:
                    """Concha Estereo"""
                    if int(self.dia_actual) % 5 == 0:   # Estos son los viernes :D
                        if self.dias_totales - self.ultima_concha > DIAS_SIN_CONCHA + 20:   # 4 semanas
                            self.concha_acustica()  # Esta funcion arma la concha acustica XD
                        elif random.randint(1, 100) < P_CONCHA():
                            self.concha_acustica()
                        else:
                            pass

                    """LLamada policias"""
                    if PROBABILIDAD_PACOS():
                        self.s.pacos = 1
                        self.llamados_carabineros += 1

                    retorno = self.s.run()

                    """Revierto la putrefaccion luego de que haya pasado el dia siguiente"""
                    if self.s.burgas_putrefactas:
                        self.s.burgas_putrefactas = False

                    self.s._dict_vendedores = retorno[0].copy()
                    self.s.alumnos = retorno[1].copy()
                    self.s.funcionarios = retorno[2].copy()
                    self.s.tiempo_simulacion = TIEMPO_SIMULACION

                    self.dia_actual += 1
                    self.dias_totales += 1

                    """Concha Estereo RESET"""
                    if self.concha == 1:
                        self.desarmar_concha()  # Esta funcion desarma la concha acustica

                    """Dia extremo RESET"""
                    if self.caluroso:
                        self.caluroso = False
                        for vendedor in self.s._dict_vendedores:
                            for producto in self.s._dict_vendedores[vendedor].lista_productos:
                                producto.tasita = 1
                    if self.frio:
                        self.frio = False
                        for vendedor in self.s._dict_vendedores:
                            for producto in self.s._dict_vendedores[vendedor].lista_productos:
                                producto.tasa_calidad = 1

                elif self.lluvia_burgas:
                    if self.s.notestadistica:
                        print('Las burgas se pudren para el dia siguiente')
                    self.lluvia_burgas = False
                    self.s.burgas_putrefactas = True
                    self.dia_actual += 1
                    self.dias_totales += 1

                """Cambio el tiempo de llegada de las personas"""
                self.reset_llegadas()

            """Cambio de precio para proximo mes"""
            for vendedor in self.s._dict_vendedores:
                for producto in self.s._dict_vendedores[vendedor].lista_productos:
                    producto.precio += self.s._dict_vendedores[vendedor].nostock/100 * producto.precio

            self.mes_actual += 1
            self.dia_actual = 1

        if self.s.notestadistica:
            self.estadisticas()

        """Estadísticas para hacer los escenarios"""

        dict0 = {'concha': self.contador_concha,
                 'carabineros': self.llamados_carabineros,
                 'textremas': self.temperaturas_extremas,
                 'hamburguesas': self.contador_hamburguesas,
                 'promedio12': int(self.s.almuerzo12 / self.dias_totales),
                 'promedio13': int(self.s.almuerzo13 / self.dias_totales),
                 'promedio14': int(self.s.almuerzo14 / self.dias_totales),
                 'no_almuerzo': self.s.alumnos_hambrientos,
                 'stock_total': self.s.stock_totales,
                 'intoxicados': self.s.numero_enfermos / 30,
                 'podridos': self.s.numero_enfermos,
                 'vendedores_sinstock': (int(self.s.vendedores_nostock)) / int(self.dias_totales),
                 'cambio_cola': self.s.cambio_colas / self.dias_totales}

        return dict0


class Simulacion:

    def __init__(self, vendedores, alumnos, funcionarios):
        self.notestadistica = True

        self.devil = QuickDevil()
        self._tiempo_simulacion = TIEMPO_SIMULACION
        self.tiempo_max = TIEMPO_MAX
        self._cola_eventos = []
        self.pacos = 0
        self.confiscaciones_jeckyl = 0
        self.confiscaciones_hyde = 0

        self.hyde = guardar_hyde()
        self.jeckyl = guardar_jeckyl()
        self.carabinero = None
        self.confiscado = 0
        self.engano_hide = 0
        self.engano_jeckyl = 0

        self._dict_vendedores = vendedores
        self._guardar_vendedores = vendedores.copy()
        self.puestos = {}

        self._dict_alumnos = alumnos
        self.guardamos_alumnos = {}
        self.asistencia = {}
        self.trasladando = {}
        self.dict_mercado = {}

        self.funcionarios = funcionarios
        self.guardamos_funcionarios = {}
        self.asistencia_funcionarios = {}
        self.trasladando_funcionarios = {}

        self.parametros = leer_parametros()

        self.burgas_putrefactas = False
        self.numero_enfermos = 0
        self.cambio_colas = 0
        self.vendedores_nostock = 0
        self.stock_totales = 0
        self.alumnos_hambrientos = 0

        self.almuerzo12 = 0
        self.almuerzo13 = 0
        self.almuerzo14 = 0

    @property
    def cantidad_vendedores(self):
        return len(self.puestos)

    @property
    def cola_eventos(self):
        return self._cola_eventos

    @cola_eventos.setter
    def cola_eventos(self, elemento):
        self._cola_eventos.append(elemento)

    @property
    def alumnos(self):
        return self._dict_alumnos

    @alumnos.setter
    def alumnos(self, value):
        self._dict_alumnos = value

    def eliminar(self, key):
        self._dict_alumnos.pop(key)

    @property
    def tiempo_simulacion(self):
        return self._tiempo_simulacion

    @tiempo_simulacion.setter
    def tiempo_simulacion(self, valor):
        self._tiempo_simulacion = valor

    def alumno_decide(self):
        """Funciona modela a los alumnos que deciden ir a almorzar en cierto horario definido en el mismo alumno"""
        try:
            min(map(lambda y: self.asistencia[y].horario, self.asistencia.keys()))
            if self.tiempo_simulacion == min(map(lambda y: self.asistencia[y].horario, self.asistencia.keys())):
                alumno = list(filter(lambda x: self.asistencia[x].horario == min(map(
                    lambda y: self.asistencia[y].horario, self.asistencia.keys())),
                                     self.asistencia.keys()))[0]
                if self.notestadistica:
                    print('El alumno {} decide ir a almorzar a las {} horas'.format(alumno, self.tiempo_simulacion))
                self.trasladando[alumno] = self.asistencia[alumno]
                """Agrego el tiempo que se demora en trasladarse el loco"""
                self._cola_eventos.append(self.trasladando[alumno].traslado)
                self.asistencia.pop(alumno)

        except ValueError as err:
            pass

    def alumno_cola(self, alumno):
        """Alumnos en el mercado son puestos en la cola de algun vendedor"""
        if len(self.dict_mercado[alumno].vendedores) == 0:
            if self.notestadistica:
                print('Alumno se va al quickdevil')
            self.almuerzo_horarios()
            if self.devil.minimo_comida() > self.dict_mercado[alumno].dinero:
                self.alumnos_hambrientos += 1
        else:
            ocupado = 0
            for k in self.dict_mercado[alumno].vendedores:
                if k in self.puestos.keys():
                    if self.puestos[k].puedo_comprar(self.dict_mercado[alumno].dinero) \
                                                                    and self.puestos[k].disponibilidad_stock():
                        if self.puestos[k].cola_alumnos + self.puestos[k].cola_funcionarios == []:
                            """Agrego el tiempo de la proxima atencion a la cola de eventos"""
                            self._cola_eventos.append(self.tiempo_simulacion + self.puestos[k].atencion)
                            self.puestos[k].proxima_atencion = self.tiempo_simulacion + self.puestos[k].atencion
                        self.puestos[k].cola_alumnos.append(alumno)
                        self.dict_mercado[alumno].paciencia_cola = self.tiempo_simulacion + \
                                                                   self.dict_mercado[alumno].paciencia
                        if self.notestadistica:
                            print('[COLA] El alumno {} se pone a la cola del vendedor {} a las {} horas'
                              .format(alumno, self.puestos[k], self.tiempo_simulacion))
                        ocupado = 1
                        break
                    else:
                        continue
                else:
                    continue
            if ocupado == 0:
                if self.notestadistica:
                    print('alumno se va al quickdevil')
                self.almuerzo_horarios()
                if self.devil.minimo_comida() > self.dict_mercado[alumno].dinero:
                    self.alumnos_hambrientos += 1
                    if self.notestadistica:
                        print('No le alcanzan las monedas y se muere de hambrea :(')
                pass

    def llega_paco(self):
        """Llega un policia si es llamado por el quickdevil"""
        if self.pacos == 1:
            if random.randint(1, 2) == 1:
                self.carabinero = random.choice(self.hyde)
            else:
                self.carabinero = random.choice(self.jeckyl)
            self.carabinero.siguiente_revision = self.carabinero.tiempo_fisco
            self._cola_eventos.append(self.carabinero.tiempo_fisco)

    def fiscaliza_paco(self):
        """Policia revisa a algun vendedor y es engañado, confisca o hecha segun dependa"""
        if self.carabinero != None and self.pacos == 1:
            if self.carabinero.siguiente_revision == self.tiempo_simulacion:
                vendedor = random.choice(list(self.puestos.keys()))
                if self.puestos[vendedor].permiso*10 > random.randint(1, 10):
                    producto = random.choice(self.puestos[vendedor].lista_productos)
                    producto.tiempo = self.tiempo_simulacion
                    if producto.calidad < 0.2:
                        self.confiscado += self.puestos[vendedor].stock
                        self.vendedores_nostock += 1
                        if self.notestadistica:
                            print('El puesto del vendedor {} ha sido confiscado'.format(vendedor))
                        self.puestos[vendedor].sin_stock += 1
                        for alumno in self.puestos[vendedor].cola_alumnos:
                            self.puestos[vendedor].cola_alumnos.remove(alumno)
                            self.alumno_cola(alumno)
                        self.puestos[vendedor].cola_alumnos = []
                        for funcionario in self.puestos[vendedor].cola_funcionarios:
                            self.puestos[vendedor].cola_funcionarios.remove(funcionario)
                            self.funcionario_cola(funcionario)
                        self.puestos[vendedor].cola_funcionarios = []
                        self.puestos.pop(vendedor)
                else:   #Aqui engaña al paco
                    if int(self.carabinero.engano)*10 > random.randint(1, 10):
                        if self.carabinero.personalidad == 'Dr. Jekyll ':
                            self.engano_jeckyl += 1
                        else:
                            self.engano_hide += 1
                        producto = random.choice(self.puestos[vendedor].lista_productos)
                        producto.tiempo = self.tiempo_simulacion
                        if producto.calidad < 0.2:
                            self.confiscado += self.puestos[vendedor].stock
                            self.vendedores_nostock += 1
                            if self.notestadistica:
                                print('El puesto del vendedor {} ha sido confiscado'.format(vendedor))
                            self.puestos[vendedor].sin_stock += 1
                            for alumno in self.puestos[vendedor].cola_alumnos:
                                self.alumno_cola(alumno)
                            self.puestos[vendedor].cola_alumnos = []
                            for funcionario in self.puestos[vendedor].cola_funcionarios:
                                self.funcionario_cola(funcionario)
                            self.puestos[vendedor].cola_funcionarios = []
                            self.puestos.pop(vendedor)
                    else:
                        self.confiscado += self.puestos[vendedor].stock
                        self.vendedores_nostock += 1
                        if self.notestadistica:
                            print('El vendedor {} escapa!'.format(vendedor))
                        self.puestos[vendedor].sin_stock += 1
                        for alumno in self.puestos[vendedor].cola_alumnos:
                            self.alumno_cola(alumno)
                        self.puestos[vendedor].cola_alumnos = []
                        for funcionario in self.puestos[vendedor].cola_funcionarios:
                            self.funcionario_cola(funcionario)
                        self.puestos[vendedor].cola_funcionarios = []
                        self.puestos.pop(vendedor)
                        self._guardar_vendedores.susto = SUSTO
                if self.tiempo_simulacion < self.carabinero.tiempo_final:
                    self.carabinero.siguiente_revision = self.tiempo_simulacion \
                                                     + self.carabinero.tiempo_fiscalizar(self.cantidad_vendedores)
                    self.cola_eventos.append(self.carabinero.siguiente_revision)
                else:
                    self.pacos = 0
                    if self.notestadistica:
                        print('Se termina la ronda de fiscalizacion del agente {}'.format(self.carabinero.nombre))

    def alumnos_trasladan(self):
        """Manejo a los trasladados y calculo cuando llegan, luego inicio las colas"""
        try:
            min(map(lambda y: self.trasladando[y].traslado, self.trasladando.keys()))
            if self.tiempo_simulacion == min(map(lambda y: self.trasladando[y].traslado, self.trasladando.keys())):
                alumno = list(filter(lambda x: self.trasladando[x].traslado == min(map(
                    lambda y: self.trasladando[y].traslado, self.trasladando.keys())),
                                     self.trasladando.keys()))[0]
                if self.notestadistica:
                    print('{} llego a comprar al mercado a las {} horas'.format(alumno, self.tiempo_simulacion))
                self.dict_mercado[alumno] = self.trasladando[alumno]
                self.guardamos_alumnos[alumno] = self.trasladando[alumno]
                self.trasladando.pop(alumno)

                """Meto al alumno en alguna cola"""

                self.alumno_cola(alumno)

        except ValueError as err:
            pass

    def pierde_paciencia(self, vendedori):
        """Modela el cambio de cola cuando un alumno pierde la paciencia,
        recibe como parametro el nombre del vendedor"""
        for alumno in self.puestos[vendedori].cola_alumnos:

            if self.dict_mercado[alumno].paciencia_cola < self.tiempo_simulacion:
                self.dict_mercado[alumno].vendedores.remove(vendedori)  # Quito al vendedor de sus opciones
                if self.dict_mercado[alumno].paciencia <= datetime.timedelta(0, 0, 0, 0, 5, 0):
                    self.puestos[vendedori].cola_alumnos.remove(alumno)
                    self.dict_mercado.pop(alumno)  # Lo quito del mercado
                    if self.notestadistica:
                        print('El alumno decide irse del mercado sin consumir ahi, '
                          'pierde la paciencia completamente')
                    pass
                else:
                    self.dict_mercado[alumno].paciencia = self.dict_mercado[alumno].paciencia - \
                                                          datetime.timedelta(0, 0, 0, 0, 5, 0)
                    self.puestos[vendedori].cola_alumnos.remove(alumno)
                    """"""
                    if len(self.dict_mercado[alumno].vendedores) > 0:
                        ocupado = 0
                        for k in self.dict_mercado[alumno].vendedores:
                            if k in self.puestos.keys():
                                if self.puestos[k].puedo_comprar(self.dict_mercado[alumno].dinero):
                                    if self.puestos[k].cola_alumnos + self.puestos[k].cola_funcionarios == []:
                                        self.puestos[k].cola_alumnos.append(alumno)
                                        self.dict_mercado[alumno].paciencia_cola = self.tiempo_simulacion + \
                                                                                   self.dict_mercado[
                                                                                       alumno].paciencia
                                        """Agrego el tiempo de la proxima atencion a la cola de eventos"""
                                        self._cola_eventos.append(self.tiempo_simulacion
                                                                  + self.puestos[k].atencion)
                                        self.puestos[k].proxima_atencion = self.tiempo_simulacion \
                                                                           + self.puestos[k].atencion
                                    else:
                                        self.puestos[k].cola_alumnos.append(alumno)
                                        self.dict_mercado[alumno].paciencia_cola = self.tiempo_simulacion + \
                                                                                   self.dict_mercado[
                                                                                       alumno].paciencia
                                    if self.notestadistica:
                                        print('[PACIENCIA] El alumno {}'
                                          ' se cambia a la cola del vendedor {} a las {} horas'
                                          .format(alumno, self.puestos[k], self.tiempo_simulacion))
                                    self.cambio_colas += 1
                                    ocupado = 1
                                    break
                                else:
                                    continue
                            else:
                                continue
                        if ocupado == 0:
                            if self.notestadistica:
                                print('alumno se va al quickdevil')
                            if self.devil.minimo_comida() > self.dict_mercado[alumno].dinero:
                                self.alumnos_hambrientos += 1
                                if self.notestadistica:
                                    print('No le alcanzan las monedas y se muere de hambrea :(')
                            else:
                                self.almuerzo_horarios()
                    else:
                        self.dict_mercado.pop(alumno)
                        if self.notestadistica:
                            print('El alumno decide irse del mercado sin consumir ahi, '
                              'pierde la paciencia completamente e intenta ir al QuickDevil')
                        if self.devil.minimo_comida() > self.dict_mercado[alumno].dinero:
                            self.alumnos_hambrientos += 1
                            if self.notestadistica:
                                print('No le alcanzan las monedas y se muere de hambre :(')
                        else:
                            self.almuerzo_horarios()
                    """"""

    def almuerzo_horarios(self):
        """Suma todas las personas que almuerzan a estos horarios"""
        if (self.tiempo_simulacion >= datetime.timedelta(0, 0, 0, 0, 0, 12)
                and (self.tiempo_simulacion < datetime.timedelta(0, 0, 0, 0, 0, 13))):
            self.almuerzo12 += 1
        if self.tiempo_simulacion >= datetime.timedelta(0, 0, 0, 0, 0, 13) \
                and (self.tiempo_simulacion < datetime.timedelta(0, 0, 0, 0, 0, 14)):
            self.almuerzo13 += 1
        if self.tiempo_simulacion >= datetime.timedelta(0, 0, 0, 0, 0, 14) \
                and (self.tiempo_simulacion < datetime.timedelta(0, 0, 0, 0, 0, 15)):
            self.almuerzo14 += 1

    def atencion_cliente(self):

        """"Manejo la atencion del proximo cliente de las colas del vendedor con orden de preferencia"""
        try:
            min(map(lambda vendedors: self.puestos[vendedors].proxima_atencion, self.puestos.keys()))
            if self.tiempo_simulacion == min(map(lambda vendedors:
                                self.puestos[vendedors].proxima_atencion, self.puestos.keys())):
                vendedori = list(filter(lambda x: self.puestos[x].proxima_atencion == min(map(
                    lambda y: self.puestos[y].proxima_atencion, self.puestos.keys())), self.puestos.keys()))[0]
                if self.notestadistica:
                    print('!!!: '+vendedori)

                """Si algun alumno pierde la paciencia, se sale de cola y elige una nueva"""
                self.pierde_paciencia(vendedori)

                if self.puestos[vendedori].cola_funcionarios == [] and len(self.puestos[vendedori].cola_alumnos) > 0:
                    alumno = self.puestos[vendedori].cola_alumnos.pop(0)
                    objeto_alumno = self.dict_mercado[alumno]
                    objeto_vendedor = self.puestos[vendedori]
                    producto = objeto_vendedor.producto_azar(objeto_alumno.dinero)
                    producto.tiempo = self.tiempo_simulacion    #Seteo el tiempo del producto
                    if self.notestadistica:
                        print('[COMPRA] El alumno {} compra exitosamente al vendedor {} el producto {} en el tiempo {}'.
                          format(alumno, vendedori, producto, self.tiempo_simulacion))
                    self.almuerzo_horarios()
                    self.puestos[vendedori].stock -= 1

                    """Veo si el producto le cae mal o no al alumno"""
                    if self.burgas_putrefactas:
                        producto.tiempo = self.tiempo_simulacion
                        if producto.calidad <= PUTREFACION_MIN and PROBABILIDAD_PUTREFACCION2():
                            if self.notestadistica:
                                print('[ENFERMO] El alumno {}, se enfermó comiendo el producto {} del vendedor {}'.
                                  format(alumno, producto, vendedori))
                            self.numero_enfermos += 1
                            self.guardamos_alumnos[alumno].vendedores.remove(vendedori)
                            if self.notestadistica:
                                print('[ENFERMO] El alumno {} borra al vendedor {} de sus preferencias'.format(alumno,
                                                                                                            vendedori))
                    else:
                        producto.tiempo = self.tiempo_simulacion
                        if producto.calidad <= PUTREFACION_MIN and PROBABILDIAD_PUTREFACCION():
                            if self.notestadistica:
                                print('[ENFERMO] El alumno {}, se enfermó comiendo el producto {} del vendedor {}'.
                                  format(alumno, producto, vendedori))
                            self.numero_enfermos += 1
                            self.guardamos_alumnos[alumno].vendedores.remove(vendedori)
                            if self.notestadistica:
                                print('[ENFERMO] El alumno {} borra al vendedor {} de sus preferencias'.format(alumno,
                                                                                                             vendedori))


                    self.dict_mercado.pop(alumno)
                    """Agrego el tiempo de la proxima atencion a la cola de eventos"""
                    self._cola_eventos.append(self.tiempo_simulacion
                                              + self.puestos[vendedori].atencion)
                    if self.notestadistica:
                        print('Proxima atencion a las  {} horas'.format(self.tiempo_simulacion
                                              + self.puestos[vendedori].atencion))
                    self.puestos[vendedori].proxima_atencion = self.tiempo_simulacion \
                                                       + self.puestos[vendedori].atencion

                    """Vendedor se queda sin stock, limpio las colas y las reasigno"""
                    if self.puestos[vendedori].stock == 0:
                        self.puestos[vendedori].nostock += 1
                        self.vendedores_nostock += 1
                        if self.notestadistica:
                            print('Vendedor {} se ha quedado sin stock'.format(vendedori))
                        self.puestos[vendedori].sin_stock += 1
                        for alumno in self.puestos[vendedori].cola_alumnos:
                            self.puestos[vendedori].cola_alumnos.remove(alumno)
                            self.alumno_cola(alumno)
                        self.puestos[vendedori].cola_alumnos = []
                        for funcionario in self.puestos[vendedori].cola_funcionarios:
                            self.puestos[vendedori].cola_funcionarios.remove(funcionario)
                            self.funcionario_cola(funcionario)
                        self.puestos[vendedori].cola_funcionarios = []
                        self.puestos.pop(vendedori)

                elif self.puestos[vendedori].cola_funcionarios != []:
                    funcionario = self.puestos[vendedori].cola_funcionarios.pop(0)
                    objeto_funcionario = self.dict_mercado[funcionario]
                    objeto_vendedor = self.puestos[vendedori]
                    producto = objeto_vendedor.producto_calidoso(objeto_funcionario.dinero)
                    producto.tiempo = self.tiempo_simulacion  # Seteo el tiempo del producto
                    if self.notestadistica:
                        print('[COMPRA] El funcionario {} '
                              'compra exitosamente al vendedor {} el producto {} en el tiempo {}'.
                            format(funcionario, vendedori, producto, self.tiempo_simulacion))
                    self.almuerzo_horarios()
                    self.puestos[vendedori].stock -= 1

                    """Veo si el producto le cae mal o no al funcionario"""
                    if self.burgas_putrefactas:
                        producto.tiempo = self.tiempo_simulacion
                        if producto.calidad <= PUTREFACION_MIN and PROBABILIDAD_PUTREFACCION2():
                            if self.notestadistica:
                                print('[ENFERMO] El funcionario {}, se enfermó comiendo el producto {} del vendedor {}'.
                                  format(funcionario, producto, vendedori))
                            self.numero_enfermos += 1
                            self.guardamos_funcionarios[funcionario].vendedores.remove(vendedori)
                            if self.notestadistica:
                                print('[ENFERMO] El funcionario {} borra al vendedor {} de sus preferencias'.format(
                                funcionario, vendedori))
                    else:
                        producto.tiempo = self.tiempo_simulacion
                        if producto.calidad <= PUTREFACION_MIN and PROBABILDIAD_PUTREFACCION():
                            if self.notestadistica:
                                print('[ENFERMO] El funcionario {}, se enfermó comiendo el producto {} del vendedor {}'.
                                  format(funcionario, producto, vendedori))
                            self.numero_enfermos += 1
                            self.guardamos_funcionarios[funcionario].vendedores.remove(vendedori)
                            if self.notestadistica:
                                print('[ENFERMO] El funcionario {} borra al vendedor {} de sus preferencias'.format(
                                    funcionario, vendedori))

                    """Cambiamos el orden de prioridades del funcionario"""
                    self.dict_mercado.pop(funcionario)  # Funcionario se vira
                    """Agrego el tiempo de la proxima atencion a la cola de eventos"""
                    self._cola_eventos.append(self.tiempo_simulacion
                                              + self.puestos[vendedori].atencion)
                    if self.notestadistica:
                        print('Proxima atencion a las  {} horas'.format(self.tiempo_simulacion
                                                                    + self.puestos[vendedori].atencion))
                    self.puestos[vendedori].proxima_atencion = self.tiempo_simulacion \
                                                               + self.puestos[vendedori].atencion

                    """Vendedor se queda sin stock, limpio las colas y las reasigno"""
                    if self.puestos[vendedori].stock == 0:
                        self.puestos[vendedori].nostock +=1
                        self.vendedores_nostock += 1
                        if self.notestadistica:
                            print('Vendedor {} se ha quedado sin stock'.format(vendedori))
                        self.puestos[vendedori].sin_stock += 1
                        for alumno in self.puestos[vendedori].cola_alumnos:
                            self.puestos[vendedori].cola_alumnos.remove(alumno)
                            self.alumno_cola(alumno)
                        self.puestos[vendedori].cola_alumnos = []
                        for funcionario in self.puestos[vendedori].cola_funcionarios:
                            self.puestos[vendedori].cola_funcionarios.remove(funcionario)
                            self.funcionario_cola(funcionario)
                        self.puestos[vendedori].cola_funcionarios = []
                        self.puestos.pop(vendedori)

                else:
                    if self.notestadistica:
                        print('No pasa naipe')
                    self.puestos[vendedori].proxima_atencion = datetime.timedelta(0, 0, 0, 0, 0, 20)      # Muito TEMPO
                    pass

        except ValueError as err:
            pass

    def llegan_vendedores(self):
        """Agrego a un vendedor"""
        try:
            min(map(lambda y: self._dict_vendedores[y].tiempo_llegada, self._dict_vendedores.keys()))
            if self.tiempo_simulacion == min(map(lambda y: self._dict_vendedores[y].tiempo_llegada,
                                                 self._dict_vendedores.keys())):
                vendedor = list(filter(lambda x: self._dict_vendedores[x].tiempo_llegada == min(map(
                    lambda y: self._dict_vendedores[y].tiempo_llegada, self._dict_vendedores.keys())),
                                       self._dict_vendedores.keys()))[0]
                if self.notestadistica:
                    print('El vendedor {} ha instalado su puesto a las {} horas'.format(vendedor,
                                                                                        self.tiempo_simulacion))
                    """Elimino al vendedor correspondiente y lo agrego a los puestos disponibles,
                    el vendedor sera un puesto"""

                #self._dict_vendedores[vendedor].tiempo_llegada = LLEGADA_VENDEDORES
                self._guardar_vendedores[vendedor] = self._dict_vendedores[vendedor]
                self.puestos[vendedor] = self._dict_vendedores[vendedor]
                self._dict_vendedores.pop(vendedor)

        except ValueError as err:
            pass

    def llegan_funcionarios(self):
        """Agrego a un funcionario"""
        try:
            min(map(lambda y: self.funcionarios[y].tiempo_llegada, self.funcionarios.keys()))
            if self.tiempo_simulacion == min(map(lambda y: self.funcionarios[y].tiempo_llegada,
                                                 self.funcionarios.keys())):
                funcionario = list(filter(lambda x: self.funcionarios[x].tiempo_llegada == min(map(
                    lambda y: self.funcionarios[y].tiempo_llegada, self.funcionarios.keys())),
                                     self.funcionarios.keys()))[0]
                if self.notestadistica:
                    print('Ha llegado el funcionario {} a las {} horas'.format(funcionario, self.tiempo_simulacion))

                    """Aca elimino al funcionario del diccionario anterior y
                    lo agrego al diccionario siguiente reseteando su tiempo de llegada a la u,
                    para que al dia siguiente llegue en otro tiempo :)"""


                self.asistencia_funcionarios[funcionario] = self.funcionarios[funcionario]
                self._cola_eventos.append(self.asistencia_funcionarios[funcionario].horario)
                self.funcionarios.pop(funcionario)

        except ValueError as err:
            pass

    def funcionario_decide(self):
        """Funcionario decide ir a almorzar"""
        try:
            min(map(lambda y: self.asistencia_funcionarios[y].horario, self.asistencia_funcionarios.keys()))
            if self.tiempo_simulacion == min(map(lambda y: self.asistencia_funcionarios[y].horario,
                                                 self.asistencia_funcionarios.keys())):
                funcionario = list(filter(lambda x: self.asistencia_funcionarios[x].horario == min(map(
                    lambda y: self.asistencia_funcionarios[y].horario, self.asistencia_funcionarios.keys())),
                                     self.asistencia_funcionarios.keys()))[0]
                if self.notestadistica:
                    print('El funcionario {} decide ir a almorzar a las {} horas'.format(funcionario, self.tiempo_simulacion))
                self.trasladando_funcionarios[funcionario] = self.asistencia_funcionarios[funcionario]
                """Agrego el tiempo que se demora en trasladarse el loco"""
                self._cola_eventos.append(self.trasladando_funcionarios[funcionario].traslado)
                self.asistencia_funcionarios.pop(funcionario)

        except ValueError as err:
            pass

    def funcionario_cola(self, funcionario):
        """Pongo al funcionario en alguna cola de vendedor"""
        if len(self.dict_mercado[funcionario].vendedores) == 0:
            if self.notestadistica:
                print('Funcionario se va al quickdevil')
            self.almuerzo_horarios()
        else:
            ocupado = 0
            for k in self.dict_mercado[funcionario].vendedores:
                if k in self.puestos.keys():
                    if self.puestos[k].puedo_comprar(self.dict_mercado[funcionario].dinero) \
                                                                        and self.puestos[k].disponibilidad_stock():

                        if self.puestos[k].cola_alumnos + self.puestos[k].cola_funcionarios == []:
                            """Agrego el tiempo de la proxima atencion a la cola de eventos"""
                            self._cola_eventos.append(self.tiempo_simulacion + self.puestos[k].atencion)
                            self.puestos[k].proxima_atencion = self.tiempo_simulacion + self.puestos[k].atencion
                        self.puestos[k].cola_funcionarios.append(funcionario)
                        if self.notestadistica:
                            print('[COLA] El funcionario {} se pone a la cola del vendedor {} a las {} horas'
                              .format(funcionario, self.puestos[k], self.tiempo_simulacion))
                        ocupado = 1
                        break
                    else:
                        continue
                else:
                    continue
            if ocupado == 0:
                if self.notestadistica:
                    print('funcionario se va al quickdevil')
                self.almuerzo_horarios()
                # Ir al QuickDevil o morirse de hambre :(
                pass

    def funcionarios_trasladan(self):
        """Manejo a los trasladados y calculo cuando llegan, luego inicio las colas"""
        try:
            min(map(lambda y: self.trasladando_funcionarios[y].traslado, self.trasladando_funcionarios.keys()))
            if self.tiempo_simulacion == min(map(lambda y: self.trasladando_funcionarios[y].traslado,
                                                                    self.trasladando_funcionarios.keys())):

                funcionario = list(filter(lambda x: self.trasladando_funcionarios[x].traslado == min(map(
                    lambda y: self.trasladando_funcionarios[y].traslado, self.trasladando_funcionarios.keys())),
                                     self.trasladando_funcionarios.keys()))[0]
                if self.notestadistica:
                    print('{} llego a comprar al mercado a las {} horas'.format(funcionario, self.tiempo_simulacion))
                self.dict_mercado[funcionario] = self.trasladando_funcionarios[funcionario]
                self.guardamos_funcionarios[funcionario] = self.trasladando_funcionarios[funcionario]
                self.trasladando_funcionarios.pop(funcionario)

                """Meto al funcionario en alguna cola"""
                self.funcionario_cola(funcionario)

        except ValueError as err:
            pass

    def llegan_alumnos(self):
        """Agrego a un alumno"""
        try:
            min(map(lambda y: self.alumnos[y].tiempo_llegada, self.alumnos.keys()))
            if self.tiempo_simulacion == min(map(lambda y: self.alumnos[y].tiempo_llegada, self.alumnos.keys())):
                alumno = list(filter(lambda x: self.alumnos[x].tiempo_llegada == min(map(
                    lambda y: self.alumnos[y].tiempo_llegada, self.alumnos.keys())),
                                     self.alumnos.keys()))[0]
                if self.notestadistica:
                    print('Ha llegado el alumno {} a las {} horas'.format(alumno, self.tiempo_simulacion))

                """Aca elimino al alumno del diccionario anterior y lo agrego al diccionario siguiente reseteando
                su tiempo de llegada a la u, para que al dia siguiente llegue en otro tiempo :)"""

                self.asistencia[alumno] = self._dict_alumnos[alumno]
                self._cola_eventos.append(self.asistencia[alumno].horario)
                self.eliminar(alumno)

        except ValueError as err:
            pass

    def run(self):

        self._cola_eventos += list(map(lambda y: self.funcionarios[y].tiempo_llegada, self.funcionarios.keys()))
        self._cola_eventos += list(map(lambda y: self.alumnos[y].tiempo_llegada, self.alumnos.keys()))
        self._cola_eventos += list(map(lambda y: self._dict_vendedores[y].tiempo_llegada, self._dict_vendedores.keys()))

        # Aca entrego todas las variables que se restean dia a día, por ejemplo el stock de los cabros.
        while self.tiempo_simulacion < self.tiempo_max:
            try:
                self.tiempo_simulacion = min(self.cola_eventos)
                self._cola_eventos.remove(min(self.cola_eventos))

                self.alumno_decide()
                self.alumnos_trasladan()
                self.llegan_vendedores()
                self.llegan_alumnos()
                self.atencion_cliente()

                self.llegan_funcionarios()
                self.funcionario_decide()
                self.funcionarios_trasladan()

                #self.llega_paco()
                #self.fiscaliza_paco()

            except ValueError as err:
                print('Se acabo el dia laboral, todos se van a la casita :)')
                self._tiempo_simulacion = self.tiempo_max
        return self._guardar_vendedores, self.guardamos_alumnos, self.guardamos_funcionarios


if __name__ == '__main__':

    vendedores = {i.nombre + ' ' + i.apellido: i for i in guardar_vendedores()}
    alumnos = {i.nombre + ' ' + i.apellido: i for i in guardar_alumnos()}
    funcionarios = {i.nombre + ' ' + i.apellido: i for i in guardar_funcionarios()}
    m = Semestre(vendedores, alumnos, funcionarios, True)
    m.run()

