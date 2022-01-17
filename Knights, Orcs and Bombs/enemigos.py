from PyQt5.QtWidgets import QLabel, QProgressBar
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QPixmap, QTransform
from time import sleep
from random import randint
import math



class MoveMyImageEvent:

    def __init__(self, label, x, y):
        self.label = label
        self.x = x
        self.y = y


class Enemy(QThread):
    trigger = pyqtSignal(MoveMyImageEvent)
    ID = 0

    def __init__(self, parent=None, x=int, y=int, max_width=int, max_height=int, tamano=int):
        super().__init__()
        self.id = Enemy.ID
        Enemy.ID += 1
        self.pausa = False
        self.tamano = tamano
        if self.tamano != 1:
            self.size = 25 + self.tamano*25
        else:
            self.size = 25 * self.tamano
        self.life = (self.tamano * 20) + 100
        self.life_max = self.life
        self.danio = round(self.tamano * 1/10 * self.life_max, 0)
        self. vision = 150
        self.atento = False

        # Creo la barra de vida del monito
        #self.progress = QProgressBar(self)
        #self.progress.setGeometry(200, 80, 250, 20)
        #self.progress.setRange(0, self.life)
        #self.progress.setValue(self.life)
        #self.progress.show()

        # Guardamos el path de la imagen que tendrá el Label
        self.food_image = 'Assets/pato_malo.png'
        # Creamos el Label y definimos su tamaño
        self.label = QLabel(parent)
        self.label.setGeometry(x, y, self.size, self.size)
        self.label.setPixmap(QPixmap(self.food_image))
        self.label.setScaledContents(True)
        self.label.show()
        self.label.setVisible(True)
        # Seteamos la posición inicial y la guardamos para usarla como una property
        self.__position = (0, 0)
        self.position = (x, y)
        self.__size = self.size
        self.__hitbox = (self.position[0], self.position[1],
                       self.position[0] + self.size, self.position[0] + self.size)
        # Guardamos los limites de la ventana para que no pueda salirse de ella
        self.max_width = max_width
        self.max_height = max_height
        self.start()
        self.desicion = randint(1, 8)
        self.hitbox_heroe = (0, 0, 0, 0)
        self.size_heroe = 25
        self.dead = False
        self.heroe_inmortal = False

    def rotacion_malo(self, valor):
        pixmap = QPixmap('Assets/pato_malo.png')
        pixmap = pixmap.scaled(75, 75)
        pixmap = pixmap.transformed(
            QTransform().rotate(valor))
        self.label.setPixmap(QPixmap(pixmap))

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, value):
        self.__size = value

    @property
    def hitbox(self):
         return self.__hitbox

    @hitbox.setter
    def hitbox(self, value):
        self.__hitbox = value

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        self.__position = value
        # El trigger emite su señal a la ventana cuando cambiamos la posición
        self.trigger.emit(MoveMyImageEvent(
            self.label, self.position[0], self.position[1]
        ))

    def choque_malos(self, entity):

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

    def rango_vision(self):
        punto = (((self.hitbox[0] + self.hitbox[2]) / 2),
                 ((self.hitbox[1] + self.hitbox[3]) / 2))
        punto_heroe = (((self.hitbox_heroe[0] + self.hitbox_heroe[2]) / 2),
                       ((self.hitbox_heroe[1] + self.hitbox_heroe[3]) / 2))
        dist = math.hypot(punto_heroe[0] - punto[0], punto_heroe[1] - punto[1])
        if dist <= self.vision:
            self.atento = True

    def rango_escape(self):
        punto = (((self.hitbox[0] + self.hitbox[2]) / 2),
                 ((self.hitbox[1] + self.hitbox[3]) / 2))
        punto_heroe = (((self.hitbox_heroe[0] + self.hitbox_heroe[2]) / 2),
                       ((self.hitbox_heroe[1] + self.hitbox_heroe[3]) / 2))
        dist = math.hypot(punto_heroe[0] - punto[0], punto_heroe[1] - punto[1])
        if dist <= self.vision * 1.5 and self.atento:
            return True
        else:
            self.atento = False
            return False

    # No implementado :''''(
    def animacion_malo(self):
        valor = 16
        self.food_image = 'Assets/enemigo/{}.png'.format(valor)
        # Creamos el Label y definimos su tamaño
        self.label.setPixmap(QPixmap(self.food_image))
        valor += 1
        if valor == 22:
            valor = 16

    def run(self):
        while self.life > 0:
            while self.pausa:
                sleep(0.1)
            sleep(0.01)     # Podria hacer una property de esto!

            #self.animacion_malo()

            # Aca muevo al enemigo a una nueva posicion con el ritmo de sleep
            if self.choque_malos(self.hitbox_heroe) and not (self.size_heroe > self.size) and self.rango_escape():
                new_x = self.position[0]
                new_y = self.position[1]
            else:
                self.rango_vision()
                if (self.size_heroe <= self.size) and self.rango_escape() and not self.heroe_inmortal:
                    if self.hitbox_heroe[0] < self.hitbox[0] and self.hitbox_heroe[1] < self.hitbox[1]:
                        desicion = 4
                    if self.hitbox_heroe[0] < self.hitbox[0] and self.hitbox_heroe[1] == self.hitbox[1]:
                        desicion = 7
                    if self.hitbox_heroe[0] == self.hitbox[0] and self.hitbox_heroe[1] < self.hitbox[1]:
                        desicion = 8
                    if self.hitbox_heroe[0] > self.hitbox[0] and self.hitbox_heroe[1] > self.hitbox[1]:
                        desicion = 3
                    if self.hitbox_heroe[0] > self.hitbox[0] and self.hitbox_heroe[1] == self.hitbox[1]:
                        desicion = 1
                    if self.hitbox_heroe[0] == self.hitbox[0] and self.hitbox_heroe[1] > self.hitbox[1]:
                        desicion = 2
                    if self.hitbox_heroe[0] > self.hitbox[0] and self.hitbox_heroe[1] < self.hitbox[1]:
                        desicion = 5
                    if self.hitbox_heroe[0] < self.hitbox[0] and self.hitbox_heroe[1] > self.hitbox[1]:
                        desicion = 6

                elif (self.size_heroe > self.size) and self.rango_escape() and not self.heroe_inmortal:
                    if self.hitbox_heroe[0] > self.hitbox[0] and self.hitbox_heroe[1] > self.hitbox[1]:
                        desicion = 4
                    if self.hitbox_heroe[0] > self.hitbox[0] and self.hitbox_heroe[1] == self.hitbox[1]:
                        desicion = 7
                    if self.hitbox_heroe[0] == self.hitbox[0] and self.hitbox_heroe[1] > self.hitbox[1]:
                        desicion = 8
                    if self.hitbox_heroe[0] < self.hitbox[0] and self.hitbox_heroe[1] < self.hitbox[1]:
                        desicion = 3
                    if self.hitbox_heroe[0] < self.hitbox[0] and self.hitbox_heroe[1] == self.hitbox[1]:
                        desicion = 1
                    if self.hitbox_heroe[0] == self.hitbox[0] and self.hitbox_heroe[1] < self.hitbox[1]:
                        desicion = 2
                    if self.hitbox_heroe[0] < self.hitbox[0] and self.hitbox_heroe[1] > self.hitbox[1]:
                        desicion = 5
                    if self.hitbox_heroe[0] > self.hitbox[0] and self.hitbox_heroe[1] < self.hitbox[1]:
                        desicion = 6

                else:
                    cambio = randint(1, 30)
                    if cambio == 4:
                        desicion = randint(1, 8)
                    else:
                        desicion = self.desicion

                if desicion == 1:
                    # Derecha
                    if self.position[0] < (int(self.max_width) - int(self.size)):
                        self.rotacion_malo(90)
                        new_x = self.position[0] + 1
                        new_y = self.position[1]
                    else:
                        new_x = self.position[0]
                        new_y = self.position[1]
                elif desicion == 2:
                    # Abajo
                    if self.position[1] < (int(self.max_height) - int(self.size)):
                        self.rotacion_malo(180)
                        new_x = self.position[0]
                        new_y = self.position[1] + 1
                    else:
                        new_x = self.position[0]
                        new_y = self.position[1]
                elif desicion == 3:
                    # Diagonal Abajo Derecha
                    if self.position[0] < (int(self.max_width) - int(self.size)) \
                            and self.position[1] < (int(self.max_height) - int(self.size)):
                        self.rotacion_malo(135)
                        new_x = self.position[0] + 1
                        new_y = self.position[1] + 1
                    else:
                        new_x = self.position[0]
                        new_y = self.position[1]
                elif desicion == 4:
                    # Diagonal Arriba Izquierda
                    if self.position[0] > 0 and self.position[1] > 45:
                        self.rotacion_malo(315)
                        new_x = self.position[0] - 1
                        new_y = self.position[1] - 1
                    else:
                        new_x = self.position[0]
                        new_y = self.position[1]
                elif desicion == 5:
                    # Diagonal Arriba Derecha
                    if self.position[0] < (int(self.max_width) - int(self.size)) and self.position[1] > 45:
                        self.rotacion_malo(45)
                        new_x = self.position[0] + 1
                        new_y = self.position[1] - 1
                    else:
                        new_x = self.position[0]
                        new_y = self.position[1]
                elif desicion == 6:
                    # Diagonal Abajo Izquierda
                    if self.position[0] > 0 and self.position[1] < (int(self.max_height) - int(self.size)):
                        self.rotacion_malo(225)
                        new_x = self.position[0] - 1
                        new_y = self.position[1] + 1
                    else:
                        new_x = self.position[0]
                        new_y = self.position[1]
                elif desicion == 7:
                    # Izquierda
                    if self.position[0] > 0:
                        self.rotacion_malo(270)
                        new_x = self.position[0] - 1
                        new_y = self.position[1]
                    else:
                        new_x = self.position[0]
                        new_y = self.position[1]
                elif desicion == 8:
                    # Abajo
                    if self.position[1] > 45:
                        self.rotacion_malo(360)
                        new_x = self.position[0]
                        new_y = self.position[1] - 1
                    else:
                        new_x = self.position[0]
                        new_y = self.position[1]
                self.desicion = desicion
            self.position = (new_x, new_y)
            self.hitbox = (self.position[0], self.position[1],
                           self.position[0]+self.size, self.position[1]+self.size)
        self.food_image = 'Assets/enemigo/37.png'
        # Creamos el Label y definimos su tamaño
        self.label.setPixmap(QPixmap(self.food_image))
        self.quit()
        self.dead = True
        sleep(1)
        self.label.deleteLater()