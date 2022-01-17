from datetime import datetime
from datetime import timedelta

class Tren:

    def __init__(self, nombre, vagones, cantidad, llegada, dia):  # Esta funcion es para instanciar cualquier objeto de tipo tren.

        self.vagones = []
        for i in [j for j in range(len(vagones))]:
            self.vagones.append((vagones[i], cantidad[i]))  # Lista de tuplas de vagones = (tipo, cantidad). EJ: [(B1, 35), (B2, 15)]
        self.nombre = nombre     # String

        self.llegada = datetime.strptime(llegada, '%H:%M').time().strftime('%H:%M')  # String, Datetime?
        self.dia = dia

    def largo(self):
        suma = 0
        for i in self.vagones:
            suma += int(i[1])
        return suma

    def __repr__(self):     # Esta funcion es para representar el tren cuando se le hace un print al objeto.

        return "Tren {}: {}".format(self.nombre, self.vagones)




class Vagon:

    def __init__(self, tipo):
        pass


class Track:

    def __init__(self, numero, tipo, capacidad):

        self.numero = numero
        self.tipo = tipo
        self.vagones = []
        self.capacidad = int(capacidad)
        self._ocupado = 0

    # Esta property actualiza la cantidad de vagones actuales que se encuentran en el track.
    @property
    def ocupado(self):
        suma = 0
        for i in self.vagones:
            suma += int(i[1])
        self._ocupado = suma
        return self._ocupado

    def __repr__(self):
        if self.tipo == 1:
            return "Receiving Track Nr° {}: Tiene {} / {} vagones".format(self.numero, self.ocupado, self.capacidad)
        elif self.tipo == 2:
            return "Classification Track Nr° {}: Tiene {} / {} vagones".format(self.numero, self.ocupado, self.capacidad)
        elif self.tipo == 3:
            return "Departure Track Nr° {}: Tiene {} / {} vagones".format(self.numero, self.ocupado, self.capacidad)
        else:
            return "No existe"

    def disponibilidad(self, cantidad):
        if int(cantidad) + int(self.ocupado) > int(self.capacidad):
            return False
        else:
            return True


class Hump:

        def __init__(self, hump_rate, interval):
            self.hump_rate = hump_rate  # cart/min
            self.cart_min = 1 / hump_rate   # min/cart
            self.interval = interval
            self.disponible = True
            self.humping = False
            self.track_actual = 1

            self.waiting = False
            self.humping_ready = False

        def humpeo(self, n_vagones, tiempo_actual):
            tiempo = n_vagones * self.cart_min
            input = datetime.strptime(tiempo_actual, '%H:%M')
            output = input + timedelta(minutes=tiempo)
            output = output.strftime('%H:%M')
            return output

        def descanso(self, interval, tiempo_actual):
            input = datetime.strptime(tiempo_actual, '%H:%M')
            output = input + timedelta(minutes=int(interval))
            output = output.strftime('%H:%M')
            return output


class Pullback:

        def __init__(self, pull_time, multi_pull, horizonte):
            self.disponible = True
            self.pull_time = pull_time
            self.multi_pull = multi_pull
            self.descanso = horizonte
            self.pulling = horizonte

        def pull(self, tiempo_actual):
            input = datetime.strptime(tiempo_actual, '%H:%M')
            output = input + timedelta(minutes=int(self.pull_time))
            output = output.strftime('%H:%M')
            return output

        def descansar(self, tiempo_actual):
            input = datetime.strptime(tiempo_actual, '%H:%M')
            output = input + timedelta(minutes=int(self.multi_pull))
            output = output.strftime('%H:%M')
            return output


class Estacion:

    def __init__(self, rec_number, rec_cap, cla_number, cla_cap, dep_number, dep_cap, hump_rate, hump_interval,
                 pull_time, multi_pull, max_outbound, min_outbound):

        self.hump_rate = hump_rate
        self.hump_interval = int(hump_interval)
        self.pull_time = pull_time
        self.multi_pull = multi_pull
        self.max_outbound = max_outbound
        self.min_outbound = min_outbound

        # Creamos los tracks de recepción
        self.rec_n = rec_number
        self.rec_cap = int(rec_cap)
        self.rec_tracks = []
        for i in [j for j in range(self.rec_n)]:
            track = Track(i+1, 1, self.rec_cap)
            self.rec_tracks.append(track)

        # Creamos los tracks de clasificacion
        self.cla_number = cla_number
        self.cla_cap = int(cla_cap)
        self.cla_tracks = []
        for i in [j for j in range(self.cla_number)]:
            track = Track(i+1, 2, self.cla_cap)
            self.cla_tracks.append(track)

        # Creamos los tracks de departure
        self.dep_number = dep_number
        self.dep_cap = int(dep_cap)
        self.dep_tracks = []
        for i in [j for j in range(dep_number)]:
            track = Track(i+1, 3, self.dep_cap)
            self.dep_tracks.append(track)

