from src.automato import Automato

class AFD(Automato):

    def __init__(self, dados):
        super().__init__(dados)

    def simular(self, palavra):

        estado_atual = self.estado_inicial
        caminho = [estado_atual]

        for simbolo in palavra:

            if simbolo not in self.alfabeto:
                return False, caminho

            if simbolo not in self.transicoes[estado_atual]:
                return False, caminho

            estado_atual = self.transicoes[estado_atual][simbolo]
            caminho.append(estado_atual)

        if estado_atual in self.estados_finais:
            return True, caminho

        return False, caminho