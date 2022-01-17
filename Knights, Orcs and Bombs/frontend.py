from game import *

if __name__ == '__main__':
    # Inicializamos la aplicación
    def hook(type, value, traceback):
        print(type)
        print(traceback)
    sys.__excepthook__ = hook

    app = QApplication([])
    form = LoginWindow()
    form.show()
    app.exec_()