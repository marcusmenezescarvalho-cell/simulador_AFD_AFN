from src.automato import Automato

class AFN(Automato):

    def __init__(self, dados):
        super().__init__(dados)

    def formatar_estados(self, estados):
        if not estados:
            return "Ø"
        return "{" + ", ".join(sorted(estados)) + "}"

    def simular(self, palavra):

        estados_atuais = {self.estado_inicial}
        caminho = [self.formatar_estados(estados_atuais)]

        for simbolo in palavra:

            if simbolo not in self.alfabeto:
                caminho.append(f"Símbolo inválido: {simbolo}")
                return False, caminho

            novos_estados = set()

            for estado in estados_atuais:

                if estado in self.transicoes:

                    if simbolo in self.transicoes[estado]:

                        destinos = self.transicoes[estado][simbolo]

                        if isinstance(destinos, list):
                            novos_estados.update(destinos)
                        else:
                            novos_estados.add(destinos)

            estados_atuais = novos_estados
            caminho.append(self.formatar_estados(estados_atuais))

            if len(estados_atuais) == 0:
                return False, caminho

        for estado in estados_atuais:
            if estado in self.estados_finais:
                return True, caminho

        return False, caminho