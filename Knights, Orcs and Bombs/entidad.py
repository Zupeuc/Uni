from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QProgressBar

from PyQt5.QtGui import QPixmap, QTransform
from PyQt5 import QtCore



class Entidad(QWidget):

    def __init__(self, imagen, size, hp=200, pos=(0, 0),
                 parent = None, hp_visible=True):
        super().__init__(parent)
        self._base_label = QLabel(self)
        self._imagen = imagen
        self._size = size
        self.__cord_x = pos[0]
        self.__cord_y = pos[1]
        self.__angle = 0
        self._hp_max = hp
        self.__hp_bar = QProgressBar(self)
        self.__hp_bar.setMaximum(self._hp_max)
        self.__hp_bar.setValue(self._hp_max)
        self.__pixmap = None
        if not hp_visible:
            self.__hp_bar.hide()
        self.setAlignment(QtCore.Qt.AlignCenter)

    @property
    def health(self):
        return self.__hp_bar.value()

    @health.setter
    def health(self, hp):
        if hp > self._hp_max:
            hp = self._hp_max
        elif hp < 0:
            hp = 0
        self.__hp_bar.setValue(hp)
        self.actualizar()

    @property
    def angle(self):
        return self.__angle

    @angle.setter
    def angle(self, angle):
        self.__angle = angle
        self.updatePixmap()

    @property
    def cord_x(self):
        return self.__cord_x

    @cord_x.setter
    def cord_x(self, cord):
        self.__cord_x = cord
        self.move(self.cord_x, self.cord_y)

    @property
    def cord_y(self):
        return self.__cord_y

    @cord_y.setter
    def cord_y(self, cord):
        self.__cord_y = cord
        self.move(self.cord_x, self.cord_y)

    @property
    def getsize(self):
        return self._size

    def updatePixmap(self):
        path = get_asset_path(self._base_image)
        self.__pixmap = QPixmap(path)
        self.__pixmap = self.__pixmap.scaled(self._size[0], self._size[1])
        self.__pixmap = self.__pixmap.transformed(
            QTransform().rotate(self.angle))
        self._base_label.setPixmap(self.__pixmap)
        self._base_label.show()

    def change_pixmap(self, image):
        self._base_image = image
        self.updatePixmap()