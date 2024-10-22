from PyQt6.QtCore import QThread, pyqtSignal, QObject

import os
import json
import requests

class WorkerSignals(QObject):
    start_process = pyqtSignal()  # Inicia o processo
    finished = pyqtSignal()       # Finaliza o processo
    result = pyqtSignal(object)   # Pode enviar qualquer tipo de dado (str, int, dict, etc.)
    error = pyqtSignal(str)       # Envia erros em formato de string
    progress = pyqtSignal(int)     # Sinal para enviar o progresso em porcentagem
    warning = pyqtSignal(str)      # Sinal para enviar avisos
    success = pyqtSignal(str)      # Sinal para enviar mensagem de sucesso

class WorkerThread(QThread):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.signals = WorkerSignals()
        self.is_running = True
        self.parent = parent
        self.data = None
        self.value = 0
        
    def load_data(self):
        if os.path.exists('_internal/_info/simple_data.json'):
            with open('_internal/_info/simple_data.json', 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        else:
            self.data = {"coins": []}

    def handle_success(self, message):
        self.signals.success.emit(message)
        
    def handle_error(self, error):
        self.signals.error.emit(error)
    
    def handle_warning(self, message):
        self.signals.warning.emit(message)
        
    def stop(self):
        # Método para parar o thread de maneira segura
        self.is_running = False
        self.signals.finished.emit()

class UpdateCambioWorker(WorkerThread):
    def __init__(self, coin, cambio_edit, parent=None):
        super().__init__(parent)
        self.coin = coin
        self.cambio_edit = cambio_edit
        # Conectar sinais da instância do WorkerThread

    def run(self):
        self.signals.start_process.emit()
        try:
            new_value = self.get_exchange_rate()
            self.cambio_edit.setText(str(new_value))
            self.handle_success("Câmbio atualizado com sucesso!")
        except Exception as e:
            self.handle_error(f"Erro ao atualizar o câmbio:\n{str(e)}")
        finally:
            self.stop()
    
    def get_exchange_rate(self):
        moeda_selecionada = self.coin.currentText()
        data = self.data.get("coins")
        print(data)
        for i in data:
            print(i)
            if i["name"] == moeda_selecionada:
                coin = i["acronym"]
                break

        if coin:
            url = f"https://economia.awesomeapi.com.br/json/last/{coin}-BRL"
            cotacao = json.loads(requests.get(url).content)
            self.value = float(cotacao[f"{coin}BRL"]["bid"])
        return str(self.value)