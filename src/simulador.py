from src.afd import AFD
from src.afn import AFN


class Simulador:

    def __init__(self, dados, tipo):

        self.tipo = tipo

        if tipo == "AFD":
            self.automato = AFD(dados)
        else:
            self.automato = AFN(dados)

    def executar(self, palavra):

        return self.automato.simular(palavra)