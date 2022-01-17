from datetime import datetime
from datetime import timedelta
from trenes2 import *
from parametros import *
from operator import attrgetter

'''
    Hump Yard simulation

    20-11-2018
    @author: zupeuc
'''

def leer_inbound():

    trenes = []
    c = 0
    with open("input2dias.csv", "r") as file:
        for line in file:
            if c == 0:
                pass
            else:
                linea = line.strip().split(';')

                # Nos saltamos esta linea que es el header del excel
                if linea[0] == 'Total general' or linea[0] == '':
                    continue

                # Tren(id, cantidad de vagones, horario de llegada, dia)
                tren = Tren(linea[0], linea[14], linea[15], linea[16])

                # Agrego carepalo cada vagon segun su identidad
                for i in range(int(linea[1])):
                    tren.vagones.append(Vagon(datetime.strptime(linea[15], "%H:%M"), 'AD'))
                for i in range(int(linea[2])):
                    tren.vagones.append(Vagon(datetime.strptime(linea[15], "%H:%M"), 'AF'))
                for i in range(int(linea[3])):
                    tren.vagones.append(Vagon(datetime.strptime(linea[15], "%H:%M"), 'AH'))
                for i in range(int(linea[4])):
                    tren.vagones.append(Vagon(datetime.strptime(linea[15], "%H:%M"), 'AJ'))
                for i in range(int(linea[5])):
                    tren.vagones.append(Vagon(datetime.strptime(linea[15], "%H:%M"), 'AK'))
                for i in range(int(linea[6])):
                    tren.vagones.append(Vagon(datetime.strptime(linea[15], "%H:%M"), 'AN'))
                for i in range(int(linea[7])):
                    tren.vagones.append(Vagon(datetime.strptime(linea[15], "%H:%M"), 'AP'))
                for i in range(int(linea[8])):
                    tren.vagones.append(Vagon(datetime.strptime(linea[15], "%H:%M"), 'AR'))
                for i in range(int(linea[9])):
                    tren.vagones.append(Vagon(datetime.strptime(linea[15], "%H:%M"), 'AV'))
                for i in range(int(linea[10])):
                    tren.vagones.append(Vagon(datetime.strptime(linea[15], "%H:%M"), 'AW'))
                for i in range(int(linea[11])):
                    tren.vagones.append(Vagon(datetime.strptime(linea[15], "%H:%M"), 'AX'))
                for i in range(int(linea[12])):
                    tren.vagones.append(Vagon(datetime.strptime(linea[15], "%H:%M"), 'AY'))
                for i in range(int(linea[13])):
                    tren.vagones.append(Vagon(datetime.strptime(linea[15], "%H:%M"), 'BG'))

                trenes.append(tren)
            c += 1
    return trenes


def ordenar_trenes(trenes):
    for i in trenes:
        i.llegada = datetime.strptime(i.llegada, "%H:%M")
    trenes.sort(key=lambda r: r.llegada)
    return trenes


def filtrar_trenes(dia, trenes):
    final = []
    for i in trenes:
        if i.dia == dia:
            final.append(i)
    return final


def siguiente_tren(trenes):
    if trenes == []:
        return False
    return trenes[0].llegada


#trenes = leer_inbound()
#print(trenes[7].vagones)

class Variable:

    def __init__(self, track1, track2):

        self.track1 = track1
        self.track2 = track2

        if not track2:
            self.valor = track1.valor
            self.largo = 1
        else:
            self.valor = track1.valor + track2.valor
            self.largo = 2

class Simulacion:

    def __init__(self, dia, estacion, inbound, t_inicial, horizonte):

        self.estacion = estacion
        self.tiempo_simulacion = datetime.strptime(t_inicial, "%H:%M")
        self.horizonte = datetime.strptime(horizonte, "%H:%M")
        self.dia = dia
        self.inbound = inbound

        self.n_trenes = len(self.inbound)
        self.proximo = datetime.strptime(t_inicial, "%H:%M")

        #ending
        self.ending = []

        #hump
        self.humping = False
        self.next_hump = datetime.strptime(t_inicial, "%H:%M")
        self.n_descansos = 0

        #pull
        self.pulling = False
        self.next_pull = datetime.strptime(t_inicial, "%H:%M")

    # Mochila
    '''
    Inspirado en:

    Knapsack Problem implementation

    Created on Dec 6, 2010
    @author: rohanbk
    '''
    def knapsack(self, ingresar_tiempo):
        tiempo_actual = ingresar_tiempo
        combinaciones = []

        # Aqui le asigno un valor a cada track y lo guardo en track.valor
        for track in self.estacion.cla_tracks:
            suma = 0
            largo = len(track.vagones)
            for vagon in track.vagones:
                tiempo = vagon.llegada - tiempo_actual

                tiempo_final = int(tiempo.total_seconds() / 60)

                suma += tiempo_final
            tiempo_final = suma

            ########################################################################################
            ########################################################################################
            ########################################################################################

            # Condiciones de los ponderadores
            if 0.25 > self.estacion.ocupado / self.estacion.capacidad_cla:
                track.valor = largo * 90* parametros["plargo1"] + tiempo_final * parametros["ptiempo1"]
            elif 0.50 > self.estacion.ocupado/self.estacion.capacidad_cla > 0.25:
                track.valor = largo* 90 * parametros["plargo2"] + tiempo_final * parametros["ptiempo2"]
            elif 0.75 > self.estacion.ocupado/self.estacion.capacidad_cla > 0.50:
                track.valor = largo* 90 * parametros["plargo3"] + tiempo_final * parametros["ptiempo3"]
            elif 1 > self.estacion.ocupado/self.estacion.capacidad_cla > 0.75:
                track.valor = largo* 90 * parametros["plargo4"] + tiempo_final * parametros["ptiempo4"]

            ########################################################################################
            ########################################################################################
            ########################################################################################


            if len(track.vagones) > self.estacion.min_outbound:
                var = Variable(track, None)
                combinaciones.append(var)

        # Ahora armo las mochilas con todas las combinaciones de tracks posibles para un multipull

        for track1 in self.estacion.cla_tracks:
            for track2 in self.estacion.cla_tracks:
                if track1.combination == track2.combination and track1 != track2:
                    if len(track1.vagones) + len(track2.vagones) > self.estacion.min_outbound:
                        var = Variable(track1, track2)
                        combinaciones.append(var)

        # Ahora buscamos el máximo entre todas las mochilas
        if len(combinaciones) >0:
            obj = max(combinaciones, key=attrgetter('valor'))
            return obj
        return False

    def llegada_tren(self):
        tren = self.inbound.pop(0)
        contador = 0
        for via in self.estacion.rec_tracks:
            if (via.ocupado == 0):
                for vagon in tren.vagones:
                    via.vagones.append(vagon)
                break
            else:
                contador += 1
        if contador == len(self.estacion.rec_tracks):
            self.estacion.sobra.append(tren)

    def llegada_espera(self):
        tren = self.estacion.sobra.pop(0)
        contador = 0
        for via in self.estacion.rec_tracks:
            if (via.ocupado == 0):
                for vagon in tren.vagones:
                    via.vagones.append(vagon)
                break
            else:
                contador += 1
        if contador == len(self.estacion.rec_tracks):
            self.estacion.sobra.append(tren)

    # Hump para tracks con un tipo
    def humpearle_tipovagon(self):
        if not self.humping:  # Si no esta humpeando
            current = Track('numero', 'tipo', 999)  # Creo un tren que no existe con 0 vagones para comparar
            for track in self.estacion.rec_tracks:
                if track.ocupado > current.ocupado:
                    current = track

            if current.ocupado == 0:  # No hay trenes a humpear
                self.next_hump = self.tiempo_simulacion + timedelta(minutes=1)

            elif current.ocupado > 0:  # Si hay trenes a humpear, preparamos el humpeo 1313
                current.estado = True
                self.humping = True
                self.next_hump = self.tiempo_simulacion + timedelta(minutes=1)

        elif self.humping:
            for track in self.estacion.rec_tracks:  # for para seleccionar el track que estamos humpeando actual
                if track.estado:
                    if track.ocupado == 0:
                        track.estado = False  # Dejamos de humpear esta track :D
                        self.humping = False
                        self.n_descansos += 1
                        self.next_hump = self.tiempo_simulacion + timedelta(
                            minutes=self.estacion.hump_interval)  # ponemos a descansar al hump
                        break
                    else:
                        vagon1 = track.vagones.pop()
                        vagon2 = track.vagones.pop()
                        contador1 = 0
                        contador2 = 0
                        for track in self.estacion.cla_tracks:
                            if vagon1.tipo in track.combination and track.disponibilidad(1):
                                track.vagones.append(vagon1)
                                contador1 = 1
                                break

                        if contador1 == 0:
                            for track in self.estacion.cla_tracks:
                                if track.ocupado == 0:
                                    track.combination.append(vagon1.tipo)
                                    track.vagones.append(vagon1)
                                    break
                        for track in self.estacion.cla_tracks:
                            if vagon2.tipo in track.combination and track.disponibilidad(1):
                                track.vagones.append(vagon2)
                                contador2 = 1
                                break
                        if contador2 == 0:
                            for track in self.estacion.cla_tracks:
                                if track.ocupado == 0:
                                    track.combination.append(vagon2.tipo)
                                    track.vagones.append(vagon2)
                                    break
                        self.next_hump = self.tiempo_simulacion + timedelta(minutes=1)
                        break

    # Hump para tracks con coutbound combination
    def humpearle_outbound_combination(self, bool):

        outbound = [["AD", "AF"],["AF", "AW", "AY"],["AH", "AK"],["AN", "AP", "AJ", "BG"],["AR", "AW", "AY"]]

        if not self.humping:  # Si no esta humpeando
            current = Track('numero', 'tipo', 999)  # Creo un tren que no existe con 0 vagones para comparar
            contador = 0
            for track in self.estacion.rec_tracks:
                if bool:
                    if track.ocupado > current.ocupado:
                        current = track
                if not bool:
                    if contador == 0:
                        if track.ocupado > 0:
                            current = track
                            contador += 1
                    elif track.ocupado <= current.ocupado and track.ocupado > 0:
                        current = track


            if current.ocupado == 0:  # No hay trenes a humpear
                self.next_hump = self.tiempo_simulacion + timedelta(minutes=1)

            elif current.ocupado > 0:  # Si hay trenes a humpear, preparamos el humpeo 1313
                current.estado = True
                self.humping = True
                self.next_hump = self.tiempo_simulacion + timedelta(minutes=1)

        elif self.humping:
            for track in self.estacion.rec_tracks:  # for para seleccionar el track que estamos humpeando actual
                if track.estado:
                    if track.ocupado == 0:
                        track.estado = False  # Dejamos de humpear esta track :D
                        self.humping = False
                        self.n_descansos += 1
                        self.next_hump = self.tiempo_simulacion + timedelta(
                            minutes=self.estacion.hump_interval)  # ponemos a descansar al hump
                        break
                    else:
                        vagon1 = track.vagones.pop()
                        vagon2 = track.vagones.pop()
                        contador1 = 0
                        contador2 = 0
                        for track in self.estacion.cla_tracks:
                            if vagon1.tipo in track.combination and track.disponibilidad(1):
                                track.vagones.append(vagon1)
                                contador1 = 1
                                break

# outbound = [["AD", "AF"],["AF", "AW", "AY"],["AH", "AK"],["AN", "AP", "AJ", "BG"],["AR", "AW", "AY"]]

                        if contador1 == 0:
                            for track in self.estacion.cla_tracks:
                                if track.ocupado == 0:
                                    if vagon1.tipo == "AD":
                                        track.combination  = ["AD", "AF"]
                                    if vagon1.tipo == "AF":
                                        track.combination = ["AF", "AW", "AY"]
                                    if vagon1.tipo == "AW":
                                        track.combination  = ["AF", "AW", "AY"]
                                    if vagon1.tipo == "AY":
                                        track.combination = ["AF", "AW", "AY"]
                                    if vagon1.tipo == "AH":
                                        track.combination = ["AH", "AK"]
                                    if vagon1.tipo == "AK":
                                        track.combination = ["AH", "AK"]
                                    if vagon1.tipo == "AN":
                                        track.combination = ["AN", "AP", "AJ", "BG"]
                                    if vagon1.tipo == "AP":
                                        track.combination = ["AN", "AP", "AJ", "BG"]
                                    if vagon1.tipo == "AJ":
                                        track.combination = ["AN", "AP", "AJ", "BG"]
                                    if vagon1.tipo == "BG":
                                        track.combination = ["AN", "AP", "AJ", "BG"]
                                    if vagon1.tipo == "AR":
                                        track.combination = ["AR", "AW", "AY"]
                                    if vagon1.tipo == "AV":
                                        track.combination = ["AV", "AX"]
                                    if vagon1.tipo == "AX":
                                        track.combination = ["AV", "AX"]

                                    track.vagones.append(vagon1)
                                    break
                        for track in self.estacion.cla_tracks:
                            if vagon2.tipo in track.combination and track.disponibilidad(1):
                                track.vagones.append(vagon2)
                                contador2 = 1
                                break
                        if contador2 == 0:
                            for track in self.estacion.cla_tracks:
                                if track.ocupado == 0:
                                    if vagon2.tipo == "AD":
                                        track.combination  = ["AD", "AF"]
                                    if vagon2.tipo == "AF":
                                        track.combination = ["AF", "AW", "AY"]
                                    if vagon2.tipo == "AW":
                                        track.combination  = ["AF", "AW", "AY"]
                                    if vagon2.tipo == "AY":
                                        track.combination = ["AF", "AW", "AY"]
                                    if vagon2.tipo == "AH":
                                        track.combination = ["AH", "AK"]
                                    if vagon2.tipo == "AK":
                                        track.combination = ["AH", "AK"]
                                    if vagon2.tipo == "AN":
                                        track.combination = ["AN", "AP", "AJ", "BG"]
                                    if vagon2.tipo == "AP":
                                        track.combination = ["AN", "AP", "AJ", "BG"]
                                    if vagon2.tipo == "AJ":
                                        track.combination = ["AN", "AP", "AJ", "BG"]
                                    if vagon2.tipo == "BG":
                                        track.combination = ["AN", "AP", "AJ", "BG"]
                                    if vagon2.tipo == "AR":
                                        track.combination = ["AR", "AW", "AY"]
                                    if vagon2.tipo == "AV":
                                        track.combination = ["AV", "AX"]
                                    if vagon2.tipo == "AX":
                                        track.combination = ["AV", "AX"]
                                    track.vagones.append(vagon2)
                                    break
                        self.next_hump = self.tiempo_simulacion + timedelta(minutes=1)
                        break

    # pull tren mas largo
    def pullearle(self):
        current = Track('numero', 'tipo', 999)
        for track in self.estacion.cla_tracks:
            if len(track.vagones) > len(current.vagones):
                current = track
        condicion = 0
        if len(current.vagones) > 0:
            if len(current.vagones) >= self.estacion.min_outbound:
                vagones = []
                for vagon in current.vagones:
                    vagon.salida = self.tiempo_simulacion + timedelta(minutes=self.estacion.pull_time)
                vagones = current.vagones
                current.vagones = []
                for i in vagones:
                    self.ending.append(i)
                self.next_pull = self.tiempo_simulacion + timedelta(minutes=self.estacion.pull_time)
                condicion = 1
            if condicion == 0:
                self.next_pull = self.tiempo_simulacion + timedelta(minutes=1)
        else:
            self.next_pull = self.tiempo_simulacion + timedelta(minutes=1)

    def multipull(self):

        # Obtenemos la track a pulear con el knapsack
        tracks = self.knapsack(self.tiempo_simulacion)

        if not tracks:
            self.next_pull = self.tiempo_simulacion + timedelta(minutes=1)

        else:
            # Multipull
            if tracks.largo == 2:
                for track in self.estacion.cla_tracks:
                    if track == tracks.track1 or track == tracks.track2:
                        vagones = []
                        for vagon in track.vagones:
                            vagon.salida = self.tiempo_simulacion + timedelta(minutes=self.estacion.multi_time)
                        vagones = track.vagones
                        track.vagones = []
                        track.combination = []
                        for i in vagones:
                            self.ending.append(i)
                        self.next_pull = self.tiempo_simulacion + timedelta(minutes=self.estacion.multi_pull)


            # Pull normal
            elif tracks.largo == 1:
                for track in self.estacion.cla_tracks:
                    if track == tracks.track1:
                        vagones = []
                        for vagon in track.vagones:
                            vagon.salida = self.tiempo_simulacion + timedelta(minutes=self.estacion.pull_time)
                        vagones = track.vagones
                        track.vagones = []
                        track.combination = []
                        for i in vagones:
                            self.ending.append(i)
                        self.next_pull = self.tiempo_simulacion + timedelta(minutes=self.estacion.pull_time)

    # pull por fecha
    def pullearle_fecha(self):
        current = Track('numero', 'tipo', 999)
        vagon = Vagon(self.horizonte, '?')
        current.vagones.append(vagon)
        for track in self.estacion.cla_tracks:
            if len(track.vagones) > 0:
                if track.vagones[0].llegada < current.vagones[0].llegada and len(track.vagones) >= self.estacion.min_outbound:
                    current = track
        condicion = 0
        if len(current.vagones) > 1:
            if len(current.vagones) >= self.estacion.min_outbound:
                vagones = []
                for vagon in current.vagones:
                    vagon.salida = self.tiempo_simulacion + timedelta(minutes=self.estacion.pull_time)
                vagones = current.vagones
                current.vagones = []
                for i in vagones:
                    self.ending.append(i)
                self.next_pull = self.tiempo_simulacion + timedelta(minutes=self.estacion.pull_time)
                condicion = 1
            if condicion == 0:
                self.next_pull = self.tiempo_simulacion + timedelta(minutes=1)
        else:
            self.next_pull = self.tiempo_simulacion + timedelta(minutes=1)

    # pull tren mas corto
    def pullearle_corto(self):
        pass

    def cada_hora(self, tiempo):
        proximo = tiempo + timedelta(minutes=60)
        return proximo

    def run(self):

            while self.tiempo_simulacion < self.horizonte:

                #Para ver si colapsa el área de clasificación
                #if self.estacion.clasi_llena():
                    #print('LLENOOOOOO')

                if not siguiente_tren(self.inbound):
                    self.tiempo_simulacion = min(self.next_hump,
                                                 self.next_pull,
                                                 self.proximo)     #Arreglar esto es para que corra por mientras nomas

                else:
                    self.tiempo_simulacion = min(siguiente_tren(self.inbound),
                                                 self.next_hump,
                                                 self.next_pull,
                                                 self.proximo)

                # 0) Toma los trenes en espera y los ingresa si hay espacio

                # Estadísticas de cada hora
                if self.tiempo_simulacion == self.proximo:
                    # print("[{}] {}%".format(self.tiempo_simulacion, int((self.estacion.ocupado / self.estacion.capacidad_cla)*100)))
                    self.proximo = self.cada_hora(self.tiempo_simulacion)

                if len(self.estacion.sobra) > 0:
                    print(self.estacion.sobra)
                    self.llegada_espera()

                # 1) Toma los inbound trains
                if siguiente_tren(self.inbound) == self.tiempo_simulacion:
                    self.llegada_tren()

                # 2) Hace el humpeo
                if self.next_hump == self.tiempo_simulacion:    # Si es tiempo del proximo hump

                    ##############################################################################
                    ##############################################################################
                    ##############################################################################

                    # True humpea el mas largo, False humpea el mas corto
                    self.humpearle_outbound_combination(False)

                    ##############################################################################
                    ##############################################################################
                    ##############################################################################

                # 3) Hace el pulling
                if self.next_pull == self.tiempo_simulacion:
                   self.multipull()

            #### ESTADISTICAS ####

            #for i in self.estacion.rec_tracks:
                #print(i)

            suma2 = 0
            for j in self.estacion.rec_tracks:
                suma2+=len(j.vagones)

            suma = 0
            for j in self.estacion.cla_tracks:
                suma+=len(j.vagones)
            print("DIA {}\n".format(self.dia))

            print("Vagones en recepcion: {}".format(suma2))
            print("Vagones en clasificacion: {}".format(suma))

            # Reset de los tiempos en clasi y en rec para efectos del día siguiente.
            for track in self.estacion.rec_tracks:
                for vagon in track.vagones:
                    vagon.llegada = datetime.strptime("00:00", "%H:%M")

            for track in self.estacion.cla_tracks:
                for vagon in track.vagones:
                    vagon.llegada = datetime.strptime("00:00", "%H:%M")

            datetimes = []
            largo = len(self.ending)
            for i in self.ending:
                datetimes.append(i.salida - i.llegada)
            average_timedelta = sum(datetimes, timedelta()) / len(datetimes)
            print("Vagones Enviados: {}".format(len(self.ending)))
            print("Tiempo promedio de un carro: {}\n".format(average_timedelta))
            print("N Vagones en la estacion: {}\n".format(self.estacion.ocupado))
            print("Clasificacion ocupados: {} / Clasificacion capacidad: {}\n".format(self.estacion.ocupado_cla, self.estacion.capacidad_cla))


#trenes = ordenar_trenes(filtrar_trenes("1", leer_inbound()))
# rec_number, rec_cap, cla_number, cla_cap, dep_number, dep_cap,
# hump_rate, hump_interval,
# pull_time, multi_pull, max_outbound, min_outbound


estacion = Estacion(10, 185, 42, 60, 7, 207, 2, 10, 10, 15, 150, 25)

for i in range(18):
    i+=1
    trenes = ordenar_trenes(filtrar_trenes(str(i), leer_inbound()))
    sim = Simulacion(i, estacion, trenes, "00:00", "23:59")
    sim.run()
    estacion = sim.estacion

