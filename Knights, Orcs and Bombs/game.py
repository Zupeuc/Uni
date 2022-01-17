import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QProgressBar
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtCore import Qt, QTimer
from enemigos import Enemy
import random
from elementos_juego import Bomba, SafeZone, PuntosExtra, VidaExtra
import math
from tiendilla import Tiendilla, Historial
import constantes
import backend
import time

login = uic.loadUiType('qtdesigner\login.ui')
mainwindow = uic.loadUiType('qtdesigner\mainwindow.ui')
qt_name, QtClass = uic.loadUiType('qtdesigner\login.ui')


class LoginWindow(qt_name, QtClass):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Login')
        #self.label.setText("<font color='white'>¡Bienvenido Guerrero!</font>")
        self.pushButton.setStyleSheet("background-color: brown;\n"
                                    "border:1px solid rgb(255, 170, 255);")
        self.pushButton_2.setStyleSheet("background-color: brown;\n"
                                    "border:1px solid rgb(255, 170, 255);")
        self.pushButton_3.setStyleSheet("background-color: brown;\n"
                                    "border:1px solid rgb(255, 170, 255);")
        self.pushButton.clicked.connect(self.click_button)
        self.pushButton_2.clicked.connect(self.click_historial)
        self.pushButton_3.clicked.connect(self.click_multiplayer)

        caballero = QPixmap('heroe/lancero.png')
        caballero = caballero.scaled(121, 91)
        self.label_3.setPixmap(caballero)

        caballero2 = QPixmap('heroe/knight2.png')
        caballero2 = caballero2.scaled(91, 91)
        self.label_4.setPixmap(caballero2)

        caballero3 = QPixmap('heroe/ogre.png')
        caballero3 = caballero3.scaled(171, 141)
        self.label_7.setPixmap(caballero3)

        fondo = QPixmap('Assets/login_background')
        fondo = fondo.scaled(625, 600)
        self.labelFondo.setPixmap(fondo)
        self.labelFondo.setGeometry(0, 0, 625, 625)
        self.labelFondo.lower()

    def click_button(self):
        usuario = self.lineEdit.text()
        self.usuario = usuario
        self.hide()
        self.algo = MainWindow(usuario, multiplayer=False)
        self.algo.show()

    def click_historial(self):
        self.historial = Historial()
        self.historial.show()

    def click_multiplayer(self):
        usuario = self.lineEdit.text()
        self.usuario = usuario
        self.hide()
        self.multiplayer = MainWindow(usuario, multiplayer=True)
        self.multiplayer.show()


class MainWindow(mainwindow[0], mainwindow[1]):

    def __init__(self, usuario, multiplayer=False):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Dungeon')
        self.multiplayer = multiplayer
        self.usuario = usuario
        self.pausa = False
        self.tienda = Tiendilla()
        self.booltienda = False
        self.setFixedSize(800, 640)
        self.setGeometry(250, 50, 800, 640)

        #   Init imagen de fondo

        fondobarra = QPixmap('Assets/barradorado.png')
        fondo2 = fondobarra.scaled(800, 640)
        self.fondo2.setPixmap(fondo2)
        self.fondo2.setGeometry(0, 0, 800, 47)
        self.fondo2.lower()

        fondo = QPixmap('Assets/dungeon_normal.png')
        fondo = fondo.scaled(800, 640)
        self.labelFondo.setPixmap(fondo)
        self.labelFondo.setGeometry(0, 47, 800, 640)
        self.labelFondo.lower()

        #self.centralWidget.setGeometry()
        self.__timer = QTimer(self)
        self.__entidades = []
        self.__enemigos = []
        self.init_heroe()
        if multiplayer:
            self.init_heroe2()
        self.init_malos()
        self.init_menu()
        self.init_timers()

        #   Init del heroe
    def init_heroe(self):
        imagen1 = QPixmap('heroe/knight.png')
        imagen1 = imagen1.scaled(100, 100)
        self.heroe.setGeometry(100, 100, 25, 25)    # Tamaño inicial del héroe
        #self.heroe.setGeometry(self.heroe.__cord_x, self.heroe.__cord_y, self.heroe.size, self.heroe.size)
        self.heroe.setScaledContents(True)
        self.heroe.setAlignment(Qt.AlignCenter)
        self.heroe.setPixmap(imagen1)
        #self.heroe = Heroe(75, (100, 100))
        self.heroe.angulo = 0
        self.heroe.__cord_x = 100
        self.heroe.__cord_y = 100
        self.heroe.nivel_actual = 1
        self.heroe.tamano_actual = 1
        self.heroe.bonus = 0
        self.heroe.size = 25    # Tamaño inicial del héroe
        self.heroe.life = self.heroe.tamano_actual * 20 + 100 + self.heroe.bonus
        self.heroe.life_max = self.heroe.tamano_actual * 20 + 100 + self.heroe.bonus
        self.heroe.ataque = 1000
        self.heroe.danio = round(self.heroe.tamano_actual * 1/10 * self.heroe.life_max)

        self.heroe.experiencia_nivel = 0
        self.heroe.experiencia_total = constantes.PUNTAJE_INICIO
        self.heroe.puntaje_tiempo = constantes.PUNTAJE_TIEMPO
        self.heroe.puntaje_enemigo = constantes.PUNTAJE_ENEMIGO
        self.heroe.puntaje_nivel = constantes.PUNTAJE_NIVEL

        self.heroe.hitbox = (self.heroe.__cord_x, self.heroe.__cord_y,
                             self.heroe.__cord_x + self.heroe.size, self.heroe.__cord_y + self.heroe.size)
        self.pressed = []
        self.thread = QTimer(self)
        self.thread.timeout.connect(self.key_thread)
        self.thread.start(70)   # Velocidad del mono
        self.show()

    def init_heroe2(self):
        imagen1 = QPixmap('heroe/player2.png')
        imagen1 = imagen1.scaled(100, 100)
        self.heroe2.setGeometry(600, 100, 25, 25)    # Tamaño inicial del héroe
        #self.heroe.setGeometry(self.heroe.__cord_x, self.heroe.__cord_y, self.heroe.size, self.heroe.size)
        self.heroe2.setScaledContents(True)
        self.heroe2.setAlignment(Qt.AlignCenter)
        self.heroe2.setPixmap(imagen1)
        #self.heroe = Heroe(75, (100, 100))
        self.heroe2.angulo = 0
        self.heroe2.__cord_x = 600
        self.heroe2.__cord_y = 100
        self.heroe2.nivel_actual = 1
        self.heroe2.tamano_actual = 1
        self.heroe2.bonus = 0
        self.heroe2.size = 25    # Tamaño inicial del héroe
        self.heroe2.life = self.heroe.tamano_actual * 20 + 100 + self.heroe.bonus
        self.heroe2.life_max = self.heroe.tamano_actual * 20 + 100 + self.heroe.bonus
        self.heroe2.ataque = 1000
        self.heroe2.danio = round(self.heroe.tamano_actual * 1/10 * self.heroe.life_max)

        self.heroe2.experiencia_nivel = 0
        self.heroe2.experiencia_total = constantes.PUNTAJE_INICIO
        self.heroe2.puntaje_tiempo = constantes.PUNTAJE_TIEMPO
        self.heroe2.puntaje_enemigo = constantes.PUNTAJE_ENEMIGO
        self.heroe2.puntaje_nivel = constantes.PUNTAJE_NIVEL

        self.heroe2.hitbox = (self.heroe.__cord_x, self.heroe.__cord_y,
                             self.heroe.__cord_x + self.heroe.size, self.heroe.__cord_y + self.heroe.size)
        #self.pressed = []
        #self.thread = QTimer(self)
        #self.thread.timeout.connect(self.key_thread)
        #self.thread.start(70)   # Velocidad del mono
        #self.show()

    def init_malos(self):
        self.malos_created = 0
        self.malo_creator_timer = QTimer(self)
        self.malo_creator_timer.timeout.connect(self.malo_creator)
        tiempo = backend.aparicion_enemigos(self.heroe.nivel_actual)
        self.malo_creator_timer.start(tiempo*1000)
        self.malos = []
        self.heroe_inmortal = False

    def init_menu(self):
        if not self.multiplayer:
            self.BarraVida_2.hide()
            self.LabelVidaP2.hide()
            self.BarraNivel_2.hide()
            self.labelNivelP2.hide()
            self.labelNivelP2numero.hide()
            self.labelPuntajeP2.hide()
            self.labelPuntajeP2numero.hide()

        # Barras Player 2
        else:
            self.BarraVida_2.setRange(0, self.heroe2.life)
            self.BarraVida_2.setValue(self.heroe2.life)
            self.BarraNivel_2.setRange(0, 1000)
            self.BarraNivel_2.setValue(self.heroe2.experiencia_nivel)

        # Barras Player 1
        self.BarraVida.setRange(0, self.heroe.life)
        self.BarraVida.setValue(self.heroe.life)

        self.labelPausa.hide()
        self.labelMuerte.hide()
        self.labelVictoria.hide()
        self.labelExp.setText(str(self.heroe.experiencia_total))
        self.labelNivel.setText(str(self.heroe.nivel_actual))
        self.BarraNivel.setRange(0, 1000)
        self.BarraNivel.setValue(self.heroe.experiencia_nivel)

        self.tiendaButton.clicked.connect(self.click_tienda)
        self.tiendaButton.setStyleSheet("background-color: brown;\n"
                                    "border:1px solid rgb(255, 170, 255);")
        self.pausaButton.clicked.connect(self.click_pausa)
        self.pausaButton.setStyleSheet("background-color: brown;\n"
                                    "border:1px solid rgb(255, 170, 255);")
        self.salirButton.clicked.connect(self.click_salida)
        self.salirButton.setStyleSheet("background-color: brown;\n"
                                    "border:1px solid rgb(255, 170, 255);")

    def init_timers(self):

        #   Init Bombas

        self.bombas_created = 0
        self.bomba_creator_timer = QTimer(self)
        self.bomba_creator_timer.timeout.connect(self.bomba_creator)
        self.bomba_creator_timer.start(random.randint(1, 30) * 1000)
        self.bombas = []

        #   Init Vidas

        self.vidas_timer = QTimer(self)
        self.vidas_timer.timeout.connect(self.vidas_creator)
        self.vidas_timer.start(random.randint(1, 30) * 1000)
        self.vidasextra = []

        #   Init Save-zone

        self.save_zone_timer = QTimer(self)
        self.save_zone_timer.timeout.connect(self.zoner_creator)
        self.save_zone_timer.start(random.randint(1, 30) * 1000)
        self.savezones = []

        #   Init experiencias

        self.experiencias_timer = QTimer(self)
        self.experiencias_timer.timeout.connect(self.experiencias_creator)
        self.experiencias_timer.start(random.randint(1, 30) * 1000)
        self.expriencias = []

        # Choque

        self.choques_timer = QTimer(self)
        self.choques_timer.timeout.connect(self.hero_choque)
        self.choques_timer.start(50)

        # Choque 2

        self.choques2_timer = QTimer(self)
        self.choques2_timer.timeout.connect(self.choques_zonas)
        self.choques2_timer.start(59)

        # Timer Bombas

        self.bombas_timer = QTimer(self)
        self.bombas_timer.timeout.connect(self.choques_bombas)
        self.bombas_timer.start(60)

        # Timer Choques Vidas

        self.choquevidas_timer = QTimer(self)
        self.choquevidas_timer.timeout.connect(self.choque_vidas)
        self.choquevidas_timer.start(50)

        # Ataque heroe!

        self.ataques_timer = QTimer(self)
        self.ataques_timer.timeout.connect(self.hero_ataque)
        self.ataques_timer.start(1000)

        # Ataque bestias!

        self.bestias_timer = QTimer(self)
        self.bestias_timer.timeout.connect(self.bestias_ataque)
        self.bestias_timer.start(1000)

        #   Timer puntajes

        self.puntaje_timer = QTimer(self)
        self.puntaje_timer.timeout.connect(self.puntaje_calculator)
        self.puntaje_timer.start(1000)
        self.adiosin = QTimer(self)
        self.adiosin.timeout.connect(self.click_salida)

    def puntaje_calculator(self):
        if not self.pausa:
            self.heroe.experiencia_total += self.heroe.puntaje_tiempo
            self.labelExp.setText(str(self.heroe.experiencia_total))

    def muerte(self):
        if self.heroe.life <= 0:
            self.BarraVida.setValue(self.heroe.life)
            self.labelMuerte.show()
            self.pausa = True
            backend.escribir_puntaje(self.usuario, self.heroe.experiencia_total)
            self.adiosin.start(2000)

    def victoria(self):
        if self.heroe.nivel_actual == 6:
            self.pausa = True
            self.labelVictoria.show()
            backend.escribir_puntaje(self.usuario, self.heroe.experiencia_total)
            self.adiosin.start(2000)

    def click_tienda(self):
        self.booltienda = False
        self.pausa = True
        self.labelPausa.show()
        self.tienda.show()

    def click_pausa(self):
        if self.pausa:
            self.pausa = False
            self.labelPausa.hide()
        else:
            self.pausa = True
            self.labelPausa.show()

    def click_salida(self):
        self.salir = LoginWindow()

        self.puntaje_timer.stop()
        self.bestias_timer.stop()
        self.ataques_timer.stop()
        self.ataques_timer.stop()
        self.choquevidas_timer.stop()
        self.bombas_timer.stop()
        self.choques2_timer.stop()
        self.choques_timer.stop()
        self.experiencias_timer.stop()
        self.save_zone_timer.stop()
        self.vidas_timer.stop()
        self.bomba_creator_timer.stop()
        self.adiosin.stop()

        backend.escribir_puntaje(self.usuario, self.heroe.experiencia_total)
        self.salir.labelAlias.setText(str(self.usuario))
        self.salir.labelPuntaje.setText(str(self.heroe.experiencia_total))

        self.salir.show()
        self.close()

    @property
    def heroe_hitbox(self):
        self.heroe.hitbox = (self.heroe.__cord_x, self.heroe.__cord_y,
                                 self.heroe.__cord_x + self.heroe.size, self.heroe.__cord_y + self.heroe.size)
        return self.heroe.hitbox

    # Maneja el danño de los malos
    def bestias_ataque(self):
        if self.booltienda:
            self.click_tienda()
        if not self.pausa:
            if not self.heroe_inmortal:
                for malo in self.malos:
                    if malo.choque_malos(self.heroe_hitbox):
                        self.heroe.life -= malo.danio
                        #print('Vida heroe: ' + str(self.heroe.life))
                        #print('Vida malo: ' + str(malo.life))

    # Maneja el daño del heroe
    def hero_ataque(self):
        if not self.pausa:
            for malo in self.malos:
                if malo.choque_malos(self.heroe_hitbox):
                    malo.life -= self.heroe.danio
                    #print('Vida heroe: ' + str(self.heroe.life))
                    #print('Vida malo: ' + str(malo.life))

    # Funcion maneja el choque de las savezones y las experiencias extras.
    def choques_zonas(self):
        if not self.pausa:
            for zone in self.savezones:
                zone.hitbox_heroe = self.heroe_hitbox
                if zone.salvatres:
                    self.heroe_inmortal = True
                    self.heroe.hide()
                else:
                    self.heroe_inmortal = False
                    self.heroe.show()
            for experiencia in self.expriencias:
                experiencia.hitbox_heroe = self.heroe_hitbox
                if experiencia.exp:
                    experiencia.exp = False
                    self.heroe.experiencia_total += experiencia.valor
                    self.labelExp.setText(str(self.heroe.experiencia_total))
                    self.expriencias.remove(experiencia)

    def choque_vidas(self):
        if not self.pausa:
            for vida in self.vidasextra:
                vida.hitbox_heroe = self.heroe_hitbox
                if vida.vida:
                    vida.vida = False
                    self.heroe.life = self.heroe.tamano_actual * 20 + 100 + self.heroe.bonus
                    self.vidasextra.remove(vida)

    def choques_bombas(self):
            for bomba in self.bombas:
                bomba.pausa = self.pausa
                bomba.hitbox_heroe = self.heroe_hitbox
                bomba.lista_malos = self.malos
                if bomba.dead:
                    if bomba.range_explode(self.heroe_hitbox):
                        self.heroe.life = 0
                    for malo in self.malos:
                        if bomba.range_explode(malo.hitbox):
                            malo.life = 0
                    self.bombas.remove(bomba)

    #   Esta funcion actualiza el choque con los malos y ademas la experiencia con la subida de nivel del heroe
    def hero_choque(self):
        if not self.pausa:
            self.muerte()       # Veo si muere
            self.victoria()     # Veo si gana
            if self.heroe.life >= 0:
                self.BarraVida.setValue(self.heroe.life)
            else:
                self.BarraVida.setValue(0)
            for malo in self.malos:
                malo.pausa = self.pausa
                malo.heroe_inmortal = self.heroe_inmortal
                malo.hitbox_heroe = self.heroe_hitbox
                malo.size_heroe = self.heroe.size
                if malo.dead:
                    self.heroe.experiencia_total += \
                        1000*constantes.PUNTAJE_ENEMIGO * max(malo.tamano - self.heroe.tamano_actual, 0)
                    self.heroe.experiencia_nivel += 100*max(malo.tamano-self.heroe.tamano_actual + 3, 1)
                    if self.heroe.experiencia_nivel >= 500 and self.heroe.experiencia_nivel <= 900:
                        # Cuando el heroe gana 500 EXP
                        if not self.heroe.tamano_actual % 2 == 0:
                            self.heroe.tamano_actual += 1
                            self.heroe.size = int(25 + self.heroe.tamano_actual*25)
                            self.heroe.setGeometry(self.heroe.__cord_x, self.heroe.__cord_y,
                                                   self.heroe.size, self.heroe.size)
                            self.heroe.life_max = self.heroe.tamano_actual * 20 + 100 + self.heroe.bonus
                            self.heroe.danio = round(self.heroe.tamano_actual * 1 / 10 * self.heroe.life_max)

                            self.BarraVida.setRange(0, self.heroe.life_max)
                            #self.BarraVida.setValue(self.heroe.life_max)

                    if self.heroe.experiencia_nivel >= 1000:
                        #   Actualizamos al heroe que sube de nivel!
                        self.heroe.experiencia_nivel = 1000
                        self.heroe.nivel_actual += 1
                        self.heroe.tamano_actual += 1
                        self.heroe.life = self.heroe.tamano_actual * 20 + 100 + self.heroe.bonus
                        self.heroe.life_max = self.heroe.tamano_actual * 20 + 100 + self.heroe.bonus
                        self.heroe.danio = round(self.heroe.tamano_actual * 1 / 10 * self.heroe.life_max)
                        #   Actualizamos las barras
                        self.BarraVida.setRange(0, self.heroe.life_max)
                        self.BarraVida.setValue(self.heroe.life_max)
                        self.BarraNivel.setRange(0, 1000)
                        self.heroe.experiencia_nivel = 0
                        self.BarraNivel.setValue(self.heroe.experiencia_nivel)
                        self.labelNivel.setText(str(self.heroe.nivel_actual))
                        #   Actualizamos el tamanio
                        self.heroe.size = int(25 + self.heroe.tamano_actual*25)
                        self.heroe.setGeometry(self.heroe.__cord_x, self.heroe.__cord_y,
                                               self.heroe.size, self.heroe.size)
                        #   Puntaje cada nivel :)
                        self.heroe.experiencia_total += 1500 + constantes.PUNTAJE_NIVEL * self.heroe.nivel_actual

                    self.BarraNivel.setValue(self.heroe.experiencia_nivel)
                    self.malos.remove(malo)
        else:
            for malo in self.malos:
                malo.pausa = self.pausa

    # Esta funcion crea a los malos!
    def malo_creator(self):
        if len(self.malos) < 20: # Cantidad de malos que spawnean, puse un maximo de 20 por que si nomas!
            if not self.pausa:
                tamanio = backend.tamano_enemigos(self.heroe.nivel_actual)
                new_malo = Enemy(parent=self, x=random.randint(0, self.width()-100),
                                 y=random.randint(45, self.height()-100),
                                 max_width=self.width(), max_height=self.height(), tamano=tamanio)
                new_malo.trigger.connect(self.mover_malo)
                self.malos.append(new_malo)
                self.malo_creator_timer.setInterval(backend.aparicion_enemigos(self.heroe.nivel_actual)*1000)
                for malo in self.malos:
                    malo.malos = self.malos
                self.malos_created += 1

    #   Spawnea las bombas
    def bomba_creator(self):
        if len(self.bombas) < 2:
            if not self.pausa:
                new_bomba = Bomba(parent=self, x=random.randint(0, self.width()-100),
                                 y=random.randint(45, self.height()-100),
                                 max_width=self.width(), max_height=self.height(), size=40)
                self.bombas.append(new_bomba)

    def zoner_creator(self):
        if len(self.savezones) < 1:
            if not self.pausa:
                new_zone = SafeZone(parent=self, x=random.randint(0, self.width()-100),
                                     y=random.randint(45, self.height()-100),
                                     max_width=self.width(), max_height=self.height(), size=40)
                self.savezones.append(new_zone)

    def experiencias_creator(self):
        if len(self.expriencias) < 2:
            if not self.pausa:
                new_zone = PuntosExtra(parent=self, x=random.randint(0, self.width()-100),
                                     y=random.randint(45, self.height()-100),
                                     max_width=self.width(), max_height=self.height(), size=25)
                self.expriencias.append(new_zone)

    def vidas_creator(self):
        if len(self.vidasextra) < 2:
            if not self.pausa:
                new_vida = VidaExtra(parent=self, x=random.randint(0, self.width()-100),
                                     y=random.randint(45, self.height()-100),
                                     max_width=self.width(), max_height=self.height(), size=20)
                self.vidasextra.append(new_vida)

    @staticmethod
    def mover_malo(myImageEvent):
        label = myImageEvent.label
        label.move(myImageEvent.x, myImageEvent.y)

    def choque_derecha(self):
        for malo in self.malos:
            if (self.heroe.hitbox[1] >= malo.hitbox[1]) and (self.heroe.hitbox[1] <= malo.hitbox[3]) or (
                        self.heroe.hitbox[1] <= malo.hitbox[1]) and (self.heroe.hitbox[3] >= malo.hitbox[1]):
                if (self.heroe.hitbox[0] >= malo.hitbox[0]) and (self.heroe.hitbox[0] <= malo.hitbox[2]):
                    return True
                else:
                    continue
            else:
                pass
        for bomba in self.bombas:
            if (self.heroe.hitbox[1] >= bomba.hitbox[1]) and (self.heroe.hitbox[1] <= bomba.hitbox[3]) or (
                        self.heroe.hitbox[1] <= bomba.hitbox[1]) and (self.heroe.hitbox[3] >= bomba.hitbox[1]):
                if (self.heroe.hitbox[0] >= bomba.hitbox[0]) and (self.heroe.hitbox[0] <= bomba.hitbox[2]):
                    return True
                else:
                    continue
            else:
                pass
        for safezone in self.savezones:
            if (self.heroe.hitbox[1] >= safezone.hitbox[1]) and (self.heroe.hitbox[1] <= safezone.hitbox[3]) or (
                        self.heroe.hitbox[1] <= safezone.hitbox[1]) and (self.heroe.hitbox[3] >= safezone.hitbox[1]):
                if (self.heroe.hitbox[0] >= safezone.hitbox[0]) and (self.heroe.hitbox[0] <= safezone.hitbox[2]):
                    return True
                else:
                    continue
            else:
                pass
        return False

    def choque_izquierda(self):
        for malo in self.malos:
            if (self.heroe.hitbox[1] >= malo.hitbox[1]) and (self.heroe.hitbox[1] <= malo.hitbox[3]) or (
                        self.heroe.hitbox[1] <= malo.hitbox[1]) and (self.heroe.hitbox[3] >= malo.hitbox[1]):
                if (self.heroe.hitbox[2] >= malo.hitbox[0]) and (self.heroe.hitbox[2] <= malo.hitbox[2]):
                    return True
                else:
                    continue
            else:
                pass
        for bomba in self.bombas:
            if (self.heroe.hitbox[1] >= bomba.hitbox[1]) and (self.heroe.hitbox[1] <= bomba.hitbox[3]) or (
                        self.heroe.hitbox[1] <= bomba.hitbox[1]) and (self.heroe.hitbox[3] >= bomba.hitbox[1]):
                if (self.heroe.hitbox[2] >= bomba.hitbox[0]) and (self.heroe.hitbox[2] <= bomba.hitbox[2]):
                    return True
                else:
                    continue
            else:
                pass
        for safezone in self.savezones:
            if (self.heroe.hitbox[1] >= safezone.hitbox[1]) and (self.heroe.hitbox[1] <= safezone.hitbox[3]) or (
                        self.heroe.hitbox[1] <= safezone.hitbox[1]) and (self.heroe.hitbox[3] >= safezone.hitbox[1]):
                if (self.heroe.hitbox[2] >= safezone.hitbox[0]) and (self.heroe.hitbox[2] <= safezone.hitbox[2]):
                    return True
                else:
                    continue
            else:
                pass
        return False

    def choque_abajo(self):
        for malo in self.malos:
            if (self.heroe.hitbox[0] >= malo.hitbox[0]) and (self.heroe.hitbox[0] <= malo.hitbox[2]) or (
                        self.heroe.hitbox[0] <= malo.hitbox[0]) and (self.heroe.hitbox[2] >= malo.hitbox[0]):
                if (self.heroe.hitbox[1] >= malo.hitbox[1]) and (self.heroe.hitbox[1] <= malo.hitbox[3]):
                    return True
                else:
                    continue
            else:
                pass
        for bomba in self.bombas:
            if (self.heroe.hitbox[0] >= bomba.hitbox[0]) and (self.heroe.hitbox[0] <= bomba.hitbox[2]) or (
                        self.heroe.hitbox[0] <= bomba.hitbox[0]) and (self.heroe.hitbox[2] >= bomba.hitbox[0]):
                if (self.heroe.hitbox[1] >= bomba.hitbox[1]) and (self.heroe.hitbox[1] <= bomba.hitbox[3]):
                    return True
                else:
                    continue
            else:
                pass
        for safezone in self.savezones:
            if (self.heroe.hitbox[0] >= safezone.hitbox[0]) and (self.heroe.hitbox[0] <= safezone.hitbox[2]) or (
                        self.heroe.hitbox[0] <= safezone.hitbox[0]) and (self.heroe.hitbox[2] >= safezone.hitbox[0]):
                if (self.heroe.hitbox[1] >= safezone.hitbox[1]) and (self.heroe.hitbox[1] <= safezone.hitbox[3]):
                    return True
                else:
                    continue
            else:
                pass
        return False

    def choque_arriba(self):
        for malo in self.malos:
            if (self.heroe.hitbox[0] >= malo.hitbox[0]) and (self.heroe.hitbox[0] <= malo.hitbox[2]) or (
                        self.heroe.hitbox[0] <= malo.hitbox[0]) and (self.heroe.hitbox[2] >= malo.hitbox[0]):
                if (self.heroe.hitbox[3] >= malo.hitbox[1]) and (self.heroe.hitbox[3] <= malo.hitbox[3]):
                    return True
                else:
                    continue
            else:
                pass
        for bomba in self.bombas:
            if (self.heroe.hitbox[0] >= bomba.hitbox[0]) and (self.heroe.hitbox[0] <= bomba.hitbox[2]) or (
                        self.heroe.hitbox[0] <= bomba.hitbox[0]) and (self.heroe.hitbox[2] >= bomba.hitbox[0]):
                if (self.heroe.hitbox[3] >= bomba.hitbox[1]) and (self.heroe.hitbox[3] <= bomba.hitbox[3]):
                    return True
                else:
                    continue
            else:
                pass
        for savezone in self.savezones:
            if (self.heroe.hitbox[0] >= savezone.hitbox[0]) and (self.heroe.hitbox[0] <= savezone.hitbox[2]) or (
                        self.heroe.hitbox[0] <= savezone.hitbox[0]) and (self.heroe.hitbox[2] >= savezone.hitbox[0]):
                if (self.heroe.hitbox[3] >= savezone.hitbox[1]) and (self.heroe.hitbox[3] <= savezone.hitbox[3]):
                    return True
                else:
                    continue
            else:
                pass
        return False

    def rotacion_heroe3(self):
        pixmap = QPixmap('heroe/player2.png')
        transform = QTransform().rotate(self.heroe2.angulo)
        pixmap = pixmap.transformed(transform, Qt.SmoothTransformation)
        self.heroe2.setPixmap(pixmap)

    def rotacion_heroe2(self):
        pixmap = QPixmap('heroe/knight.png')
        pixmap = pixmap.scaled(75, 75)
        pixmap = pixmap.transformed(
            QTransform().rotate(self.heroe.angulo))
        self.heroe.setPixmap(pixmap)

    # Key parser para movimiento fluido del heroe
    def key_parser(self, keys):
        if Qt.Key_W in keys:
            if not self.pausa:
                angulo = self.heroe.angulo*3.14159/180
                avance_x = math.cos(angulo)*10
                avance_y = math.sin(angulo)*10
                #   Controlar avance eje X
                if self.heroe.__cord_x <= 0 and avance_x < 0:
                    self.heroe.__cord_x = 0
                else:
                    if (avance_x < 0) and not self.choque_derecha():
                        self.heroe.__cord_x += avance_x
                    elif (avance_x >= 0)and not self.choque_izquierda():
                        self.heroe.__cord_x += avance_x
                if self.heroe.__cord_x >= self.width() - self.heroe.size and avance_x > 0:
                    self.heroe.__cord_x = self.width() - self.heroe.size
                else:
                    if (avance_x < 0) and not self.choque_derecha():
                        self.heroe.__cord_x += avance_x
                    elif (avance_x >= 0)and not self.choque_izquierda():
                        self.heroe.__cord_x += avance_x
                if self.heroe.__cord_y <= 45 and avance_y < 0:
                    self.heroe.__cord_y = 45
                else:
                    if avance_y > 0 and not self.choque_arriba():
                        self.heroe.__cord_y += avance_y
                    elif avance_y <= 0 and not self.choque_abajo():
                        self.heroe.__cord_y += avance_y
                if self.heroe.__cord_y >= self.height() - self.heroe.size and avance_y > 0:
                    self.heroe.__cord_y = self.height() - self.heroe.size
                else:
                    if avance_y > 0 and not self.choque_arriba():
                        self.heroe.__cord_y += avance_y
                    elif avance_y <= 0 and not self.choque_abajo():
                        self.heroe.__cord_y += avance_y
                self.heroe.move(self.heroe.__cord_x, self.heroe.__cord_y)

        if Qt.Key_A in keys:
            if not self.pausa:
                self.heroe.angulo -= 10
                self.rotacion_heroe2()

        if Qt.Key_D in keys:
            if not self.pausa:
                self.heroe.angulo += 10
                self.rotacion_heroe2()

        if Qt.Key_S in keys:
            if not self.pausa:
                angulo = self.heroe.angulo * 3.14159 / 180
                avance_x = math.cos(angulo) * 3
                avance_y = math.sin(angulo) * 3
                if self.heroe.__cord_x <= 0 and avance_x > 0:
                    self.heroe.__cord_x = 0
                else:
                    if (avance_x < 0) and not self.choque_derecha():
                        self.heroe.__cord_x -= avance_x
                    elif (avance_x >= 0)and not self.choque_izquierda():
                        self.heroe.__cord_x -= avance_x
                if self.heroe.__cord_x >= self.width() - self.heroe.size and avance_x < 0:
                    self.heroe.__cord_x = self.width() - self.heroe.size
                else:
                    if (avance_x > 0) and not self.choque_derecha():
                        self.heroe.__cord_x -= avance_x
                    elif (avance_x <= 0)and not self.choque_izquierda():
                        self.heroe.__cord_x -= avance_x
                if self.heroe.__cord_y <= 45 and avance_y > 0:
                    self.heroe.__cord_y = 45
                else:
                    if avance_y < 0 and not self.choque_arriba():
                        self.heroe.__cord_y -= avance_y
                    elif avance_y >= 0 and not self.choque_abajo():
                        self.heroe.__cord_y -= avance_y
                if self.heroe.__cord_y >= self.height() - self.heroe.size and avance_y < 0:
                    self.heroe.__cord_y = self.height() - self.heroe.size
                else:
                    if avance_y < 0 and not self.choque_arriba():
                        self.heroe.__cord_y -= avance_y
                    elif avance_y >= 0 and not self.choque_abajo():
                        self.heroe.__cord_y -= avance_y
                self.heroe.move(self.heroe.__cord_x, self.heroe.__cord_y)

        if Qt.Key_Control in keys and Qt.Key_S in keys:
            self.click_pausa()

        if Qt.Key_Control in keys and Qt.Key_T in keys:
            self.booltienda = True

        self.moviemiento_player2(keys)

    # Mueve al Player 2
    def moviemiento_player2(self, keys):
        if self.multiplayer:
            if Qt.Key_I in keys:
                if not self.pausa:
                    angulo = self.heroe2.angulo * 3.14159 / 180
                    avance_x = math.cos(angulo) * 10
                    avance_y = math.sin(angulo) * 10
                    #   Controlar avance eje X
                    if self.heroe2.__cord_x <= 0 and avance_x < 0:
                        self.heroe2.__cord_x = 0
                    else:
                        if (avance_x < 0) and not self.choque_derecha():
                            self.heroe2.__cord_x += avance_x
                        elif (avance_x >= 0) and not self.choque_izquierda():
                            self.heroe2.__cord_x += avance_x
                    if self.heroe2.__cord_x >= self.width() - self.heroe2.size and avance_x > 0:
                        self.heroe2.__cord_x = self.width() - self.heroe2.size
                    else:
                        if (avance_x < 0) and not self.choque_derecha():
                            self.heroe2.__cord_x += avance_x
                        elif (avance_x >= 0) and not self.choque_izquierda():
                            self.heroe2.__cord_x += avance_x
                    if self.heroe2.__cord_y <= 45 and avance_y < 0:
                        self.heroe2.__cord_y = 45
                    else:
                        if avance_y > 0 and not self.choque_arriba():
                            self.heroe2.__cord_y += avance_y
                        elif avance_y <= 0 and not self.choque_abajo():
                            self.heroe2.__cord_y += avance_y
                    if self.heroe2.__cord_y >= self.height() - self.heroe2.size and avance_y > 0:
                        self.heroe2.__cord_y = self.height() - self.heroe2.size
                    else:
                        if avance_y > 0 and not self.choque_arriba():
                            self.heroe2.__cord_y += avance_y
                        elif avance_y <= 0 and not self.choque_abajo():
                            self.heroe2.__cord_y += avance_y
                    self.heroe2.move(self.heroe2.__cord_x, self.heroe2.__cord_y)

            if Qt.Key_J in keys:
                if not self.pausa:
                    self.heroe2.angulo -= 10
                    self.rotacion_heroe3()

            if Qt.Key_L in keys:
                if not self.pausa:
                    self.heroe2.angulo += 10
                    self.rotacion_heroe3()

            if Qt.Key_K in keys:
                if not self.pausa:
                    angulo = self.heroe2.angulo * 3.14159 / 180
                    avance_x = math.cos(angulo) * 3
                    avance_y = math.sin(angulo) * 3
                    self.heroe2.__cord_x -= avance_x
                    self.heroe2.__cord_y -= avance_y
                    self.heroe2.move(self.heroe2.__cord_x, self.heroe2.__cord_y)

    def key_thread(self):
        self.key_parser(self.pressed)

    def keyPressEvent(self, e):
        tecla = e.key()
        if tecla not in self.pressed:
            self.pressed.append(tecla)

    def keyReleaseEvent(self, e):
        tecla = e.key()
        if tecla in self.pressed:
            self.pressed.remove(tecla)
