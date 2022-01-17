from datetime import datetime
from datetime import timedelta
from trenes import *


# Funcion que lee el inbound.csv y lo transforma en un diccionario
def leer_inbound():

    trenes = {}
    c = 0
    with open("inbound.csv", "r") as file:
        for line in file:
            if c == 0:
                pass
            else:
                linea = line.strip().split(';')
                linea = linea[0: 5]
                linea[4] = int(linea[4])
                # print(linea)
                if linea[1] not in trenes.keys():
                    trenes[linea[1]] = [linea[0], linea[2], [linea[3]], [linea[4]]]
                else:
                    if linea[3] in trenes[linea[1]][2]:
                        trenes[linea[1]][3][-1] = linea[4] - (sum(trenes[linea[1]][3][:-1]))
                    elif linea[3] not in trenes[linea[1]][2]:
                        trenes[linea[1]][2].append(linea[3])
                        trenes[linea[1]][3].append(linea[4])
            c += 1
    return trenes   # Retorna diccionario con el formato:
                    # ID: [dia, hora, lista de tipos de vagon, lista de cantidades de vagones]


# Prints de prueba

"""
trenes = leer_inbound()
print(trenes)

# Imprime todos los trenes guardados en la lista inbound
"""

""""
for i in estacion.rec_tracks:
    print(i)
for i in estacion.cla_tracks:
    print(i)
for i in estacion.dep_tracks:
    print(i)
"""

class Simulacion:

    def __init__(self, estacion, inbound, t_inicial, horizonte):

        self.estacion = estacion
        self.t_inicial = t_inicial
        self.horizonte = horizonte
        self.tiempo_simulacion = t_inicial
        self.hump = Hump(self.estacion.hump_rate, self.estacion.hump_interval)
        self.pullback = Pullback(self.estacion.pull_time, self.estacion.multi_pull, self.horizonte)
        self.espera = []        # Trenes en espera para entrar al sistema
        self.track_humpeada = None
        self.track_pulleada = None
        self.lista_salida = []
        self.vagones_sacados = 0


        # un for a self.trenes_llegada[i][1] entrega el hroario de dicho tren

        self.inbound = []       # Listado con todos los trenes de llegada
        for i in inbound:
            tren = Tren(i, trenes[i][2], trenes[i][3], trenes[i][1], trenes[i][0])
            self.inbound.append(tren)

        self.tiempos_in = []
        for i in self.inbound:
            self.tiempos_in.append(i.llegada)

        #self.tiempos_hump = []

        print(self.inbound)
        """
        for i in self.inbound:
            print(i)
            print(i.largo())
        """

    def proximo_tren(self): # Como los trenes ya vienen ordenados por tiempo, es cosa de hacer popleft nomas :)
        if not self.inbound:
            tiempo = self.horizonte     # Casi límite con lita vacía
        else:
            tiempo = self.inbound[0].llegada
            #tren = self.inbound.pop(0)
        return tiempo


    def run(self):

        while datetime.strptime(self.tiempo_simulacion, '%H:%M').time() < datetime.strptime(self.horizonte, '%H:%M').time():

            #   Aqui comparamos todos los eventos y tomamos el mas temprano.
            #   Luego actualizamos el tiempo actual al mismo tiempo que el evento mas temprano.

            print(self.tiempo_simulacion)

            # Aca deberiamos elegir el minimo entre todos los eventos
            if self.hump.waiting and self.hump.humping_ready:
                print('Consideramos todos')
                self.tiempo_simulacion = \
                    min(
                    datetime.strptime(self.proximo_tren(), '%H:%M').time(),
                    datetime.strptime(self.hump.waiting, '%H:%M').time(),
                    datetime.strptime(self.hump.humping_ready, '%H:%M').time(),
                    datetime.strptime(self.pullback.pulling, '%H:%M').time(),
                    datetime.strptime(self.pullback.descanso, '%H:%M').time()
                    ).strftime('%H:%M')


            # Estos elif estan por que no definí muy bien los estados del hump, pretendo sacarlos mas adelante

            elif self.hump.waiting and not self.hump.humping_ready:
                print('Consideramos hump_waiting')
                self.tiempo_simulacion = \
                    min(
                        datetime.strptime(self.proximo_tren(), '%H:%M').time(),
                        datetime.strptime(self.hump.waiting, '%H:%M').time(),
                        datetime.strptime(self.pullback.pulling, '%H:%M').time(),
                        datetime.strptime(self.pullback.descanso, '%H:%M').time()
                    ).strftime('%H:%M')

            elif self.hump.humping_ready and not self.hump.waiting:
                print('calculamos el tiempo considerando hump_ready')
                self.tiempo_simulacion = \
                    min(
                        datetime.strptime(self.proximo_tren(), '%H:%M').time(),
                        datetime.strptime(self.hump.humping_ready, '%H:%M').time(),
                        datetime.strptime(self.pullback.pulling, '%H:%M').time(),
                        datetime.strptime(self.pullback.descanso, '%H:%M').time()
                    ).strftime('%H:%M')

            else:
                print('calculamos solo proximo tren')
                self.tiempo_simulacion = self.proximo_tren()

            # 1) Este if maneja lo que tenga que ver con los inbound trains!

            if self.tiempo_simulacion == self.proximo_tren() and self.inbound and self.tiempo_simulacion in self.tiempos_in:
                tren = self.inbound.pop(0)  #    Acá tomo el tren que llegó y lo elimino de la lista de inbound
                if self.tiempo_simulacion in self.tiempos_in:
                    self.tiempos_in.remove(self.tiempo_simulacion)
                asignado = False

                # Aca asignamos el tren a un track que no tenga vagones.

                for i in self.estacion.rec_tracks:
                    if i.ocupado == 0 and not asignado:
                        #ponemos el tren ahí agergando los vagones individualmente
                        for j in tren.vagones:
                            i.vagones.append(j)
                        print("[{}]El tren {} entra a {}".format(self.tiempo_simulacion, tren, i))
                        asignado = True

                # Acá asignamos el tren a un track que ya tiene vagones, pero tiene espacio para recibir al tren.

                if not asignado:
                    for i in self.estacion.rec_tracks:
                        if i.disponibilidad(tren.largo()) and not asignado:
                            #ponemos el tren ahí agregando los vagones individualmente
                            for j in tren.vagones:
                                i.vagones.append(j)
                            print("[{}]El tren {} entra a {}".format(self.tiempo_simulacion, tren, i))
                            asignado = True

                if not asignado:    # Para efectos de construcción, esto luego se borrará
                    self.espera.append(tren)
                    print('[{}]El tren {}, entra a la sala de espera.'.format(self.tiempo_simulacion, tren))

            # 2) Estos if manejam el estados del hump engine

            if not self.hump.disponible and not self.hump.humping and self.tiempo_simulacion == self.hump.waiting:
                print("Se termina el tiempo de espera del hump")
                self.hump.disponible = True
                self.hump.waiting = False

            if self.hump.disponible:
                print('[{}]hump disponible'.format(self.tiempo_simulacion))
                numero = 0
                for i in self.estacion.rec_tracks:  # Busca la track con mayor cantidad de vagones para ser humpeada
                    if i.ocupado > numero:
                        self.track_humpeada = i
                        numero = i.ocupado
                if not self.track_humpeada.vagones:   # Condicion que existe si no hay vagones en ninguna receiving track
                    print("entramos aca?")
                    #self.hump.waiting = False
                    pass
                else:
                    print('nos ponemos a humpear')
                    self.hump.waiting = False
                    self.hump.humping = True
                    self.hump.disponible = False
                    self.hump.humping_ready = self.hump.humpeo(self.track_humpeada.ocupado, self.tiempo_simulacion)
                    print("El tiempo para que este listo el humpeo es: "+str(self.hump.humping_ready))

            # 3) Esta if hace el humpeo a cada track.

            if not self.hump.disponible and self.hump.humping and self.tiempo_simulacion == self.hump.humping_ready:
                self.hump.humping_ready = False
                print("[{}]El hump termino de humpear".format(self.tiempo_simulacion))
                print(self.track_humpeada.vagones)
                for j in self.track_humpeada.vagones:
                    if j[0] == 'B1':
                        self.estacion.cla_tracks[0].vagones.append(j)
                    if j[0] == 'B2':
                        self.estacion.cla_tracks[1].vagones.append(j)
                    if j[0] == 'B3':
                        self.estacion.cla_tracks[2].vagones.append(j)
                    if j[0] == 'B4':
                        self.estacion.cla_tracks[3].vagones.append(j)
                    if j[0] == 'B5':
                        self.estacion.cla_tracks[4].vagones.append(j)
                    if j[0] == 'B6':
                        self.estacion.cla_tracks[5].vagones.append(j)
                self.track_humpeada.vagones = []

                print(self.track_humpeada)

                self.hump.disponible = False
                self.hump.humping = False
                self.hump.waiting = self.hump.descanso(self.estacion.hump_interval, self.tiempo_simulacion)
                print("El hump estará disponible nuevamente a las "+str(self.hump.waiting))
                for i in self.estacion.cla_tracks:

                    print('[{}] "Classification Track Nr° {}: Tiene {} / {} vagones" luego del humping.'
                          .format(self.tiempo_simulacion, i.numero, i.ocupado, i.capacidad))

            # 4) Este if maneja el pullback

            if self.pullback.disponible:
                numero = 0
                for i in self.estacion.cla_tracks:
                    if i.ocupado > numero:
                        self.track_pulleada = i
                        numero = i.ocupado
                if numero >= 30:
                    # Hacemos pull
                    self.pullback.pulling = self.pullback.pull(self.tiempo_simulacion)
                    self.pullback.disponible = False
                else:
                    pass

            if not self.pullback.disponible and self.pullback.pulling == self.tiempo_simulacion:
                print('Se hizo un pull :)')
                # Movemos los carros
                if self.track_pulleada.ocupado < 40:
                    vagones = self.track_pulleada.vagones
                    for i in vagones:
                        self.vagones_sacados += i[1]
                    self.track_pulleada.vagones = []
                    print("Sale el outbound train: {}".format(vagones))
                    self.lista_salida.append((vagones, self.tiempo_simulacion))

                else:
                    numero = 40
                    outbound_train = []
                    for i in self.track_pulleada.vagones:
                        if i[1] != 0:
                            if i[1] > 40 and numero == 40:
                                outbound_train.append((i[0], 40))
                                i[1] -= 40
                                self.vagones_sacados += 40
                                break
                            elif i[1] < 40 and numero == 40:
                                numero -= i[1]
                                self.vagones_sacados += i[1]
                                outbound_train.append(i)
                                i[1] = 0
                            elif i[1] < numero:
                                self.vagones_sacados += i[1]
                                numero -= i[1]
                                outbound_train.append(i)
                                i[1] = 0
                            elif i[1] > numero:
                                self.vagones_sacados += numero
                                outbound_train.append((i[0], numero))
                                i[1] -= numero
                                numero = 0
                    print("Sale el outbound train: {}".format(outbound_train))

                vagones_nuevos = []
                for j in self.track_pulleada.vagones:
                    if j[1] == 0:
                        pass
                    else:
                        vagones_nuevos.append(j)
                self.track_pulleada.vagones = vagones_nuevos


                self.pullback.pulling = self.horizonte
                self.pullback.descanso = self.pullback.descansar(self.tiempo_simulacion)

            if not self.pullback.disponible and self.pullback.descanso == self.tiempo_simulacion:
                # El pullback termina de descansar!

                self.pullback.disponible = True
                self.pullback.descanso = self.horizonte

        # Print de estadísticas finales

        for i in self.estacion.cla_tracks:
            print(i)
        print("Sacamos en total: {} vagones".format(self.vagones_sacados))
        for i in self.lista_salida:
            print("El tren {} salió a las [{}]".format(i[0], i[1]))

            # vagones = self.estacion.min_outbound    # Definimos el mínimo de vagones requerido para hacer un pull


# Aqui hacemos correr la simulacion

# (rec_number, rec_cap, cla_number, cla_cap, dep_number, dep_cap, hump_rate,
# hump_interval, pull_time, multi_pull, max_outbound, min_outbound)
estacion = Estacion(4, 40, 6, 50, 4, 40, 2.5, 8, 5, 5, 40, 30)
trenes = leer_inbound()

sim = Simulacion(estacion, trenes, "9:00", "12:00")

print("\nSIMULACION\n")
sim.run()