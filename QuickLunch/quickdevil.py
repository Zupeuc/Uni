from productos import*


class QuickDevil:

    def __init__(self):
        snacks = filter(lambda x: x[1] == 'Snack', leer_productos())
        self.snacks = [Producto(i[0], i[1], i[2], i[3], i[4]) for i in snacks]
        comidas = filter(lambda x: x[1] == 'Fondo', leer_productos())
        self.comidas = [Producto(i[0], i[1], i[2], i[3], i[4]) for i in comidas]


    def minimo_comida(self):
        """Retorna la comida mas barata del QuickDevil para ver si alumno se meure de hambre o no"""
        return min(list(map(lambda x: x.precio, self.comidas)))



