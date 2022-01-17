
class Tren:

    def __init__(self, nombre, cantidad, llegada, dia):

        self.nombre = nombre
        self.cantidad = int(cantidad)
        self.llegada = llegada
        self.salida = "oli"
        self.estado = "llegada"
        self.dia = dia
        self.vagones = []

    def __repr__(self):

        return "Tren {} Cantidad: {} vagones. Horario: {}.".format(self.nombre, self.cantidad, self.llegada)


class Vagon:

    def __init__(self, llegada, tipo):

        self.llegada = llegada
        self.salida = "oli"
        self.tipo = tipo
        self.actual = "oli"

    def __repr__(self):

        return "Vagon tipo: {} Entrada: {} Salida: {}".format(self.tipo, self.llegada, self.salida)


class Track:

    def __init__(self, numero, tipo, capacidad):

        self.numero = numero
        self.tipo = tipo
        self.vagones = []
        self.capacidad = int(capacidad)
        self._ocupado = 0
        self.combination = []
        self.estado = False

        self.valor = 0

    # Esta property actualiza la cantidad de vagones actuales que se encuentran en el track.
    @property
    def ocupado(self):
        suma = 0
        for i in self.vagones:
            suma += 1
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


class Estacion:

    def __init__(self, rec_number, rec_cap, cla_number, cla_cap, dep_number, dep_cap, hump_rate, hump_interval,
                 pull_time, multi_pull, max_outbound, min_outbound):

        self.hump_rate = hump_rate  # vagones que humpea al minuto
        self.hump_interval = int(hump_interval)  # descanso del hump
        self.pull_time = pull_time  # tiempo que se demora un pull
        self.multi_pull = multi_pull
        self.max_outbound = max_outbound    # minima capacidad de un outbound train
        self.min_outbound = min_outbound    # maxima capacidad de un outbound train
        self._ocupado = 0
        self.capacidad_cla = (cla_number * cla_cap)
        self._ocupado_cla = 0
        self._ocupado_tracks = 0

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

        # Creamos una track para los trenes que sobran

        self.sobra = []


    @property
    def ocupado(self):
        suma = 0
        for track in self.cla_tracks:
            suma += track.ocupado
        for track in self.rec_tracks:
            suma += track.ocupado
        for track in self.dep_tracks:
            suma += track.ocupado
        self._ocupado = suma
        return self._ocupado

    @property
    def ocupado_cla(self):
        suma = 0
        for track in self.cla_tracks:
            suma += track.ocupado
        self._ocupado_cla = suma
        return self._ocupado_cla

    @property
    def ocupado_tracks(self):
        suma = 0
        for i in self.cla_tracks:
            if i.ocupado > 0:
                suma += 1
        self._ocupado_tracks = suma
        return self._ocupado_tracks

    def clasi_llena(self):

        if self.ocupado_tracks == self.cla_number:
            return True
        return False
