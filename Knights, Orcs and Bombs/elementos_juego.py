from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QLabel
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from time import sleep
import math


class Bomba(QThread):

    def __init__(self, parent=None, x=int, y=int, max_width=int, max_height=int, size=int):
        super().__init__()

        self.pausa = False
        self.food_image = 'Assets/bomba_lais.png'
        # Creamos label del timer

        # Creamos el Label y definimos su tamaño

        self.label = QLabel(parent)
        self.label.setGeometry(x, y, size, size)
        self.label.setPixmap(QPixmap(self.food_image))
        self.label.setScaledContents(True)
        self.label.show()
        self.label.setVisible(True)
        # Seteamos la posición inicial y la guardamos para usarla como una property
        self.position = (x, y)
        self.__size = size
        self.__hitbox = (self.position[0], self.position[1],
                         self.position[0] + size, self.position[1] + size)
        self.max_width = max_width
        self.max_height = max_height
        self.dead = False
        self.hitbox_heroe = (0, 0, 0, 0)
        self.lista_malos = []
        self.rango_explosion = 90
        self.start()

    @property
    def size(self):
        return self.__size

    @property
    def hitbox(self):
        return self.__hitbox

    def choque(self, entity):

        if (self.hitbox[0] <= entity[2]) and (self.hitbox[0] >= entity[0]) and \
                (self.hitbox[3] >= entity[1]) and self.hitbox[3] <= entity[3]:
            return True
        if (self.hitbox[2] <= entity[2]) and (self.hitbox[2] >= entity[0]) and \
                (self.hitbox[3] >= entity[1]) and self.hitbox[3] <= entity[3]:
            return True
        if (self.hitbox[0] <= entity[2]) and (self.hitbox[0] >= entity[0]) and \
                (self.hitbox[1] >= entity[1]) and (self.hitbox[1] <= entity[3]):
            return True
        if (self.hitbox[2] <= entity[2]) and (self.hitbox[2] >= entity[0]) and \
                (self.hitbox[1] >= entity[1]) and (self.hitbox[1] <= entity[3]):
            return True
        else:
            return False

    def choque_malos(self, lista_malos):
        for malo in lista_malos:
            if self.choque(malo.hitbox):
                return True
        return False

    def range_explode(self, hitbox):
        punto = (((int(self.hitbox[0]) + int(self.hitbox[2])) / 2),
                 ((int(self.hitbox[1]) + int(self.hitbox[3])) / 2))
        punto_heroe = (((hitbox[0] + hitbox[2]) / 2),
                       ((hitbox[1] + hitbox[3]) / 2))
        dist = math.hypot(punto_heroe[0] - punto[0], punto_heroe[1] - punto[1])
        if dist <= self.rango_explosion + self.size:
            return True
        return False

    def run(self):
        while not self.dead:
            sleep(0.01)
            if self.choque(self.hitbox_heroe) or self.choque_malos(self.lista_malos):
                self.label.setPixmap(QPixmap('Assets/bomba_1.png'))
                while self.pausa:
                    sleep(0.1)
                self.sleep(1)
                while self.pausa:
                    sleep(0.1)
                while self.pausa:
                    sleep(0.1)
                self.label.setPixmap(QPixmap('Assets/bomba_2.png'))
                while self.pausa:
                    sleep(0.1)
                self.sleep(1)
                while self.pausa:
                    sleep(0.1)
                self.label.setPixmap(QPixmap('Assets/bomba_3.png'))
                while self.pausa:
                    sleep(0.1)
                self.sleep(1)
                while self.pausa:
                    sleep(0.1)
                self.dead = True
                self.label.setPixmap(QPixmap('Assets/explosion2.png'))
                self.label.setGeometry(self.position[0] - 25, self.position[1] - 25, self.size * 2, self.size * 2)
        sleep(1)
        self.label.deleteLater()
        self.quit()


class SafeZone(QThread):

    def __init__(self, parent=None, x=int, y=int, max_width=int, max_height=int, size=int):
        super().__init__()

        self.food_image = 'Assets/safe_zone2.png'
        # Creamos el Label y definimos su tamaño
        self.label = QLabel(parent)
        self.label.setGeometry(x, y, size, size)
        self.label.setPixmap(QPixmap(self.food_image))
        self.label.setScaledContents(True)
        self.label.show()
        self.label.setVisible(True)
        # Seteamos la posición inicial y la guardamos para usarla como una property
        self.position = (x, y)
        self.__size = size
        self.__hitbox = (self.position[0], self.position[1],
                         self.position[0] + self.size, self.position[1] + self.size)
        self.max_width = max_width
        self.max_height = max_height
        self.hitbox_heroe = (0, 0, 0, 0)
        self.dead = False
        self.rango_explosion = 21
        self.salvatres = False
        self.start()


    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, value):
        self.__size = value

    @property
    def hitbox(self):
        return self.__hitbox

    def choque(self, entity):

        if (self.hitbox[0] <= entity[2]) and (self.hitbox[0] >= entity[0]) and \
                (self.hitbox[3] >= entity[1]) and self.hitbox[3] <= entity[3]:
            return True
        elif (self.hitbox[2] <= entity[2]) and (self.hitbox[2] >= entity[0]) and \
                (self.hitbox[3] >= entity[1]) and self.hitbox[3] <= entity[3]:
            return True
        elif (self.hitbox[0] <= entity[2]) and (self.hitbox[0] >= entity[0]) and \
                (self.hitbox[1] >= entity[1]) and (self.hitbox[1] <= entity[3]):
            return True
        elif (self.hitbox[2] <= entity[2]) and (self.hitbox[2] >= entity[0]) and \
                (self.hitbox[1] >= entity[1]) and (self.hitbox[1] <= entity[3]):
            return True
        else:
            return False

    def range_explode(self, hitbox):
        punto = (((int(self.hitbox[0]) + int(self.hitbox[2])) / 2),
                 ((int(self.hitbox[1]) + int(self.hitbox[3])) / 2))
        punto_heroe = (((hitbox[0] + hitbox[2]) / 2),
                       ((hitbox[1] + hitbox[3]) / 2))
        dist = math.hypot(punto_heroe[0] - punto[0], punto_heroe[1] - punto[1])
        if dist <= self.rango_explosion + self.size:
            return True
        return False

    def run(self):
        while not self.dead:
            sleep(0.3)
            if self.range_explode(self.hitbox_heroe):
                self.salvatres = True
                print('Salvado')
            else:
                self.salvatres = False


class PuntosExtra(QThread):

    def __init__(self, parent=None, x=int, y=int, max_width=int, max_height=int, size=int):
        super().__init__()

        self.food_image = 'Assets/tesoro.png'
        # Creamos el Label y definimos su tamaño
        self.label = QLabel(parent)
        self.label.setGeometry(x, y, size, size)
        self.label.setPixmap(QPixmap(self.food_image))
        self.label.setScaledContents(True)
        self.label.show()
        self.label.setVisible(True)
        # Seteamos la posición inicial y la guardamos para usarla como una property
        self.position = (x, y)
        self.__size = size
        self.__hitbox = (self.position[0], self.position[1],
                         self.position[0] + self.size, self.position[1] + self.size)
        self.max_width = max_width
        self.max_height = max_height

        self.hitbox_heroe = (0, 0, 0, 0)
        self.dead = False
        self.exp = False
        self.valor = 1000
        self.start()

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, value):
        self.__size = value

    @property
    def hitbox(self):
        return self.__hitbox

    def choque(self, entity):

        if (self.hitbox[0] <= entity[2]) and (self.hitbox[0] >= entity[0]) and \
                (self.hitbox[3] >= entity[1]) and self.hitbox[3] <= entity[3]:
            return True
        if (self.hitbox[2] <= entity[2]) and (self.hitbox[2] >= entity[0]) and \
                (self.hitbox[3] >= entity[1]) and self.hitbox[3] <= entity[3]:
            return True
        if (self.hitbox[0] <= entity[2]) and (self.hitbox[0] >= entity[0]) and \
                (self.hitbox[1] >= entity[1]) and (self.hitbox[1] <= entity[3]):
            return True
        if (self.hitbox[2] <= entity[2]) and (self.hitbox[2] >= entity[0]) and \
                (self.hitbox[1] >= entity[1]) and (self.hitbox[1] <= entity[3]):
            return True
        else:
            return False

    def run(self):
        while not self.dead:
            sleep(0.01)
            if self.choque(self.hitbox_heroe):
                self.exp = True
                print('EXP para ti')
                self.dead = True
                self.label.deleteLater()
                self.quit()
            else:
                pass


class VidaExtra(QThread):

    def __init__(self, parent=None, x=int, y=int, max_width=int, max_height=int, size=int):
        super().__init__()

        self.food_image = 'Assets/vida_extra2.png'
        # Creamos el Label y definimos su tamaño
        # Creamos el Label y definimos su tamaño
        self.label = QLabel(parent)
        self.label.setGeometry(x, y, size, size)
        self.label.setPixmap(QPixmap(self.food_image))
        self.label.setScaledContents(True)
        self.label.show()
        self.label.setVisible(True)
        # Seteamos la posición inicial y la guardamos para usarla como una property
        self.position = (x, y)
        self.__size = size
        self.__hitbox = (self.position[0], self.position[1],
                         self.position[0] + self.size, self.position[1] + self.size)
        self.max_width = max_width
        self.max_height = max_height

        self.hitbox_heroe = (0, 0, 0, 0)
        self.dead = False
        self.vida = False
        self.start()

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, value):
        self.__size = value

    @property
    def hitbox(self):
        return self.__hitbox

    def choque(self, entity):

        if (self.hitbox[0] <= entity[2]) and (self.hitbox[0] >= entity[0]) and \
                (self.hitbox[3] >= entity[1]) and self.hitbox[3] <= entity[3]:
            return True
        if (self.hitbox[2] <= entity[2]) and (self.hitbox[2] >= entity[0]) and \
                (self.hitbox[3] >= entity[1]) and self.hitbox[3] <= entity[3]:
            return True
        if (self.hitbox[0] <= entity[2]) and (self.hitbox[0] >= entity[0]) and \
                (self.hitbox[1] >= entity[1]) and (self.hitbox[1] <= entity[3]):
            return True
        if (self.hitbox[2] <= entity[2]) and (self.hitbox[2] >= entity[0]) and \
                (self.hitbox[1] >= entity[1]) and (self.hitbox[1] <= entity[3]):
            return True
        else:
            return False

    def run(self):
        while not self.dead:
            sleep(0.03)
            if self.choque(self.hitbox_heroe):
                self.vida = True
                print('VIDAAAAAA')
                self.dead = True
                self.label.deleteLater()
                self.quit()

