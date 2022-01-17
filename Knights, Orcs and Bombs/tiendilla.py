from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFrame, QApplication, QLabel
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag
import backend

tienda = uic.loadUiType('qtdesigner\latienda.ui')
history = uic.loadUiType('qtdesigner\historial.ui')


class DropBox(QFrame):
    def __init__(self, parent):
        QFrame.__init__(self, parent)
        self.setAcceptDrops(True)  # Aceptar objetos
        self.setStyleSheet("background-color: #E6E6E6;")

    def dragEnterEvent(self, event):
        # Ignorar objetos arrastrados sin información
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        # Establecer el widget en una nueva posición
            pos = event.pos()
            self.label = event.source()
            self.label.setParent(self)
            self.label.setGeometry(self.label.x(), self.label.y(), 71, 71)
            self.label.show()
            event.acceptProposedAction()

class DraggableLabel(QLabel):
    def __init__(self, parent):
        QLabel.__init__(self, parent)

    def mousePressEvent(self, event):
        # Inicializar el arrastre con el botón derecho
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        # Chequear que se esté presionando el botón derecho
        if not (event.buttons() and Qt.LeftButton):
            return

        # Verificar que sea una posición válida
        if ((event.pos() - self.drag_start_position).manhattanLength()
                < QApplication.startDragDistance()):
            return

        drag = QDrag(self)
        mime_data = QMimeData()

        # Establecer el contenido del widget como dato
        mime_data.setText(self.text())
        drag.setMimeData(mime_data)

        # Ejecutar la acción
        self.drop_action = drag.exec_(Qt.CopyAction | Qt.MoveAction)


class Tiendilla(tienda[0], tienda[1]):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('La Tienda')

        fondo = QPixmap('Assets/fondo_madera.png')
        fondo = fondo.scaled(800, 430)
        self.labelFondo.setPixmap(fondo)
        self.labelFondo.setGeometry(0, 0, 800, 430)
        self.labelFondo.lower()

        self.dropboxvida = DropBox(self)
        self.dropboxvida.setGeometry(self.vidaLabel.geometry())
        self.dropboxvelocidad = DropBox(self)
        self.dropboxvelocidad.setGeometry(self.velocidadLabel.geometry())
        self.dropboxataque = DropBox(self)
        self.dropboxataque.setGeometry(self.ataqueLabel.geometry())

        self.dropbox1 = DropBox(self)
        self.dropbox1.setGeometry(150, 320, 71, 71)
        self.dropbox2 = DropBox(self)
        self.dropbox2.setGeometry(250, 320, 71, 71)
        self.dropbox3 = DropBox(self)
        self.dropbox3.setGeometry(350, 320, 71, 71)
        self.dropbox4 = DropBox(self)
        self.dropbox4.setGeometry(450, 320, 71, 71)
        self.dropbox5 = DropBox(self)
        self.dropbox5.setGeometry(550, 320, 71, 71)

        vida_image = QPixmap('Assets/heart')
        vida_image = vida_image.scaled(71, 71)
        self.vidaLabel2 = DraggableLabel(self.dropboxvida)
        #self.vidaLabel.setGeometry(10, 10, 150, 20)
        self.vidaLabel2.setPixmap(vida_image)

        velocidad_image = QPixmap('Assets/boots')
        velocidad_image = velocidad_image.scaled(71, 71)
        self.velocidadLabel2 = DraggableLabel(self.dropboxvelocidad)
        self.velocidadLabel2.setPixmap(velocidad_image)

        ataque_image = QPixmap('Assets/attack_speed')
        ataque_image = ataque_image.scaled(71, 71)
        self.ataqueLabel2 = DraggableLabel(self.dropboxataque)
        self.ataqueLabel2.setPixmap(ataque_image)


class Historial(history[0], history[1]):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Liga de los mejores')

        fondo = QPixmap('Assets/papel_antiguo.png')
        fondo = fondo.scaled(381, 513)
        self.labelFondo.setPixmap(fondo)
        self.labelFondo.setGeometry(0, 0, 381, 513)
        self.labelFondo.lower()

        diccionario = backend.entregar_top(backend.leer_historial())
        lista = []
        for i in diccionario.keys():
            lista.append([str(i), str(diccionario[i])])
        for i in lista:
            if i[0] == '':
                i[0] = 'NoName'
        try:
            self.label_2.setText('- ' + lista[0][0] + ': ' + lista[0][1])
        except IndexError:
            self.label_2.setText('- ')
        try:
            self.label_3.setText('- ' + lista[1][0] + ': ' + lista[1][1])
        except IndexError:
            self.label_3.setText('- ')
        try:
            self.label_4.setText('- ' + lista[2][0] + ': ' + lista[2][1])
        except IndexError:
            self.label_4.setText('- ')
        try:
            self.label_5.setText('- ' + lista[3][0] + ': ' + lista[3][1])
        except IndexError:
            self.label_5.setText('- ')
        try:
            self.label_6.setText('- ' + lista[4][0] + ': ' + lista[4][1])
        except IndexError:
            self.label_6.setText('- ')
        try:
            self.label_7.setText('- ' + lista[5][0] + ': ' + lista[5][1])
        except IndexError:
            self.label_7.setText('- ')
        try:
            self.label_8.setText('- ' + lista[6][0] + ': ' + lista[6][1])
        except IndexError:
            self.label_8.setText('- ')
        try:
            self.label_9.setText('- ' + lista[7][0] + ': ' + lista[7][1])
        except IndexError:
            self.label_9.setText('- ')
        try:
            self.label_10.setText('- ' + lista[8][0] + ': ' + lista[8][1])
        except IndexError:
            self.label_10.setText('- ')
        try:
            self.label_11.setText('- ' + lista[9][0] + ': ' + lista[9][1])
        except IndexError:
            self.label_11.setText('- ')
