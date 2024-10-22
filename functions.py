from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QMessageBox

from workers import *

class Functions(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        # Instância do WorkerThread
        self.worker = WorkerThread(parent=self)
        self.worker.load_data()
        # Conectar sinais do WorkerThread
        self.worker.signals.success.connect(self.show_success_message)
        self.worker.signals.error.connect(self.show_error_message)
        self.worker.signals.warning.connect(self.show_warning_message)
        
        self.parent.coin_select.setCurrentIndex(-1)
        self.parent.coin_select.currentIndexChanged.connect(self.start_update_cambio)

    def show_success_message(self, message):
        QMessageBox.information(self.parent, "Sucesso", message)

    def show_error_message(self, error):
        QMessageBox.critical(self.parent, "Erro", error)

    def show_warning_message(self, message):
        QMessageBox.warning(self.parent, "Aviso", message)

    def start_update_cambio(self):
        # Cria e inicia o worker para atualizar o câmbio
        cambio_worker = UpdateCambioWorker(self.parent.coin_select, self.parent.cambio_edit, parent=self)
        cambio_worker.start()
