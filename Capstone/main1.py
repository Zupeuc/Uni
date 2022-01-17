from datetime import datetime
from datetime import timedelta
from trenes2 import *


def leer_inbound():

    trenes = []
    c = 0
    with open("input1dias.csv", "r") as file:
        for line in file:
            if c == 0:
                pass
            else:
                linea = line.strip().split(';')

                # Nos saltamos esta linea que es el header del excel
                if linea[0] == 'Total general' or linea[0] == '':
                    continue

                # Tren(id, cantidad de vagones, horario de llegada, dia)
                tren = Tren(linea[0], linea[7], linea[8][:-3], linea[9])

                # Agrego carepalo cada vagon segun su identidad
                for i in range(int(linea[1])):
                    tren.vagones.append(Vagon(datetime.strptime(linea[8][:-3], "%H:%M"), 'B1'))
                for i in range(int(linea[2])):
                    tren.vagones.append(Vagon(datetime.strptime(linea[8][:-3], "%H:%M"), 'B2'))
                for i in range(int(linea[3])):
                    tren.vagones.append(Vagon(datetime.strptime(linea[8][:-3], "%H:%M"), 'B3'))
                for i in range(int(linea[4])):
                    tren.vagones.append(Vagon(datetime.strptime(linea[8][:-3], "%H:%M"), 'B4'))
                for i in range(int(linea[5])):
                    tren.vagones.append(Vagon(datetime.strptime(linea[8][:-3], "%H:%M"), 'B5'))
                for i in range(int(linea[6])):
                    tren.vagones.append(Vagon(datetime.strptime(linea[8][:-3], "%H:%M"), 'B6'))

                trenes.append(tren)
            c += 1
    return trenes

trenes = leer_inbound()
for i in trenes:
    print(i)


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


class Simulacion:

    def __init__(self, dia, estacion, inbound, t_inicial, horizonte):

        self.estacion = estacion
        self.tiempo_simulacion = datetime.strptime(t_inicial, "%H:%M")
        self.horizonte = datetime.strptime(horizonte, "%H:%M")
        self.dia = dia
        self.inbound = inbound

        self.n_trenes = len(self.inbound)

        #ending
        self.ending = []

        #hump
        self.humping = False
        self.next_hump = datetime.strptime(t_inicial, "%H:%M")
        self.n_descansos = 0

        #pull
        self.pulling = False
        self.next_pull = datetime.strptime(t_inicial, "%H:%M")


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

    def humpearle_outbound_combination(self):

        outbound = [["AD", "AF"],["AF", "AW", "AY"],["AH", "AK"],["AN", "AP", "AJ", "BG"],["AR", "AW", "AY"]]

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
                        try:
                            vagon2 = track.vagones.pop()
                        except:
                            pass
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
                                    if vagon1.tipo == "B1":
                                        track.combination = ["B1", "B2"]
                                    if vagon1.tipo == "B2":
                                        track.combination = ["B1", "B2"]
                                    if vagon1.tipo == "B3":
                                        track.combination = ["B3", "B4"]
                                    if vagon1.tipo == "B4":
                                        track.combination = ["B3", "B4"]
                                    if vagon1.tipo == "B5":
                                        track.combination = ["B5", "B6"]
                                    if vagon1.tipo == "B6":
                                        track.combination = ["B5", "B6"]

                                    track.vagones.append(vagon1)
                                    break
                        for track in self.estacion.cla_tracks:
                            try:
                                if vagon2.tipo in track.combination and track.disponibilidad(1):
                                    track.vagones.append(vagon2)
                                    contador2 = 1
                                    break
                            except:
                                pass

                        if contador2 == 0:
                            for track in self.estacion.cla_tracks:
                                if track.ocupado == 0:
                                    try:
                                        if vagon2.tipo == "B1":
                                            track.combination = ["B1", "B2"]
                                        if vagon2.tipo == "B2":
                                            track.combination = ["B1", "B2"]
                                        if vagon2.tipo == "B3":
                                            track.combination = ["B3", "B4"]
                                        if vagon2.tipo == "B4":
                                            track.combination = ["B3", "B4"]
                                        if vagon2.tipo == "B5":
                                            track.combination = ["B5", "B6"]
                                        if vagon2.tipo == "B6":
                                            track.combination = ["B5", "B6"]

                                        track.vagones.append(vagon2)
                                        break
                                    except:
                                        pass

                        self.next_hump = self.tiempo_simulacion + timedelta(minutes=1)
                        break

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

    def pullearle_corto(self):
        pass

    def run(self):

            while self.tiempo_simulacion < self.horizonte:

                if not siguiente_tren(self.inbound):
                    self.tiempo_simulacion = min(self.next_hump,
                                                 self.next_pull)     #Arreglar esto es para que corra por mientras nomas

                else:
                    self.tiempo_simulacion = min(siguiente_tren(self.inbound),
                                                 self.next_hump,
                                                 self.next_pull)

                # 1) Toma los inbound trains
                if siguiente_tren(self.inbound) == self.tiempo_simulacion:
                    self.llegada_tren()

                # 2) Hace el humpeo
                if self.next_hump == self.tiempo_simulacion:    # Si es tiempo del proximo hump
                    self.humpearle_outbound_combination()

                # 3) Hace el pulling
                if self.next_pull == self.tiempo_simulacion:
                   self.pullearle_fecha()

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

            datetimes = []
            largo = len(self.ending)
            for i in self.ending:
                datetimes.append(i.salida - i.llegada)
            try:
                average_timedelta = sum(datetimes, timedelta()) / len(datetimes)
                print("Tiempo promedio de un carro: {}\n".format(average_timedelta))
            except:
                pass
            print("Vagones Enviados: {}".format(len(self.ending)))
            print("N Vagones en la estacion: {}\n".format(self.estacion.ocupado))

            print("Clasificacion ocupados: {} / Clasificacion capacidad: {}\n".format(self.estacion.ocupado_cla, self.estacion.capacidad_cla))

# ESTACION
# rec_number, rec_cap, cla_number, cla_cap, dep_number, dep_cap,
# hump_rate, hump_interval,
# pull_time, multi_pull, max_outbound, min_outbound


i=3
trenes = ordenar_trenes(filtrar_trenes(str(i), leer_inbound()))
estacion = Estacion(4, 40, 6, 50, 4, 40, 2, 8, 5, 5, 40, 30)
sim = Simulacion(i, estacion, trenes, "09:00", "12:30")
sim.run()