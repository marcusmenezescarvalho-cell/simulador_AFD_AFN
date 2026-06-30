class Automato:

    def __init__(self, dados):

        self.estados = dados["estados"]
        self.alfabeto = dados["alfabeto"]
        self.estado_inicial = dados["estado_inicial"]
        self.estados_finais = dados["estados_finais"]
        self.transicoes = dados["transicoes"]

    def get_estados(self):
        return self.estados

    def get_alfabeto(self):
        return self.alfabeto

    def get_estado_inicial(self):
        return self.estado_inicial

    def get_estados_finais(self):
        return self.estados_finais

    def get_transicoes(self):
        return self.transicoes