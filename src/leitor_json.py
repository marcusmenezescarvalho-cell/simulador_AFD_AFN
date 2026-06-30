import json

class LeitorJSON:

    def carregar(self, caminho):

        with open(caminho, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        return dados