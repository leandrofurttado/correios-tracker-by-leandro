import sys
from design_correios import Ui_MainWindow
from desgin_janela2 import *
from PyQt5.QtWidgets import QMainWindow, QApplication
from bs4 import BeautifulSoup
import requests

class Janela2(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Janela2()
        self.ui.setupUi(self)
        self.ui.buttonSalvarNome.clicked.connect(self.salvarCodigo)

    def salvarCodigo(self):
        with open('codigos.txt', 'a+') as arq_codigos:
            arq_codigos.write(f'{str(self.ui.inputNomeMercadoria.text())}= {str(self.ui.inputCodigoMercadoria.text())}'
                              f' (APAGUE TUDO QUE NÃO É O CÓDIGO)\n')



class Tracker(QMainWindow, Ui_MainWindow, Ui_Janela2):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        self.janela2 = Janela2()
        self.button_rastreio.clicked.connect(self.rastreiaCodigo)
        self.button_salvar.clicked.connect(self.mudaJanela)
        self.buttonBoxCodigos.clicked.connect(self.opcaoDeCodigo)
        self.clearList.clicked.connect(self.limparlista)
        self.attList.clicked.connect(self.lerCodigos)
        self.lerCodigos()

    #RASTREADOR
    def rastreia(self, codigo):
        code = codigo
        site = requests.get(f'https://www.linkcorreios.com.br/?id={code}')

        soup = BeautifulSoup(site.text, 'html.parser')
        status = soup.findAll("div", {"class": "card-header"})
        convert = (status[0].text).replace('Ãtimo', 'Último').replace('destinatÃ¡rio', 'destinatário.') \
            .replace('DistribuiÃ§Ã£o', 'Distribuição').replace('trÃ¢nsito', 'transito')
        return convert


    def rastreiaCodigo(self):
        try:
            codigo = str(self.inputCodigo.text())
            rastreio = self.rastreia(codigo)
            self.label_dosDados.setText(str(rastreio))
        except IndexError as e:
            self.label_dosDados.setText('MERCADORIA NÃO ENCONTRADA!\nCÓDIGO NÃO EXISTE OU AINDA NÃO FOI POSTADO!')


    def opcaoDeCodigo(self):
        code_save = self.box_codigos.currentText()
        self.inputCodigo.setText(str(code_save))

    def limparlista(self):
        with open('codigos.txt', 'w+') as arq_limpar:
            arq_limpar.write('')

    def lerCodigos(self):
        with open('codigos.txt', 'r') as arq_codigos:
            linhas = arq_codigos.readlines()
            self.box_codigos.addItems(linhas)

    def mudaJanela(self):
        self.janela2.show()




if __name__ == '__main__':
    qt = QApplication(sys.argv)
    app = Tracker()
    app.show()
    qt.exec_()