import sys
from PyQt6 import uic, QtCore, QtGui, QtWidgets
from functions import Functions
        
class Main(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("_internal/_screens/main.ui", self)
        self.setWindowTitle('Certidão de Débitos')
        self.setWindowIcon(QtGui.QIcon('_internal/_assets/icon.ico'))
        self.functions = Functions(self)

def main():
    """
    Função principal para inicializar e executar a aplicação PyQt.
    """
    app = QtWidgets.QApplication(sys.argv)
    # Cria a janela principal do aplicativo
    window = Main()
    window.show()    
    # Executa o loop principal do PyQt
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
