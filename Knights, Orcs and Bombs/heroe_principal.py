from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QProgressBar

from PyQt5.QtGui import QPixmap, QTransform
from PyQt5 import QtCore


class Heroe(QWidget):

    def __init__(self, size, pos=(100, 100),
                 parent=None, hp_visible=False):
        super().__init__(parent)

        self.hero_image = 'heroe/knight.png'
        self.label = QLabel(parent)
        self.label.setGeometry(pos[0], pos[1], size, size)
        self.label.setScaledContents(True)
        self.label.setPixmap(QPixmap(self.hero_image))

        self.label.show()
        self.label.setVisible(True)
        self._size = size
        self.__cord_x = pos[0]
        self.__cord_y = pos[1]
        self.__angulo = 0
        #self.setAlignment(QtCore.Qt.AlignCenter)


    @property
    def angulo(self):
        return self.__angulo

    @angulo.setter
    def angulo(self, angulo):
        self.__angulo = angulo

    @property
    def cord_x(self):
        return self.__cord_x

    @cord_x.setter
    def cord_x(self, cord):
        self.__cord_x = cord
        #self.move(self.cord_x, self.cord_y)

    @property
    def cord_y(self):
        return self.__cord_y

    @cord_y.setter
    def cord_y(self, cord):
        self.__cord_y = cord
        #self.move(self.cord_x, self.cord_y)

    @property
    def getsize(self):
        return self._size

    def updatePixmap(self):
        self.__pixmap = QPixmap('heroe/knight.png')
        self.__pixmap = self.__pixmap.scaled(self._size[0], self._size[1])
        self.__pixmap = self.__pixmap.transformed(
            QTransform().rotate(self.angulo))
        self._base_label.setPixmap(self.__pixmap)
        self._base_label.show()

    def change_pixmap(self, image):
        self._base_image = image
        self.updatePixmap()

    def setFixedSize(self, x, y):
        super().setFixedSize(x, y)
        self._base_label.setFixedSize(x, y)

    def setAlignment(self, alignment):
        self._base_label.setAlignment(alignment)