from tkinter import *
from tkinter import filedialog
from src.leitor_json import LeitorJSON
from src.simulador import Simulador


class Interface(Tk):

    def __init__(self):
        super().__init__()

        self.title("Simulador de AFD e AFN")
        self.geometry("1200x760")
        self.configure(bg="#EAEAEA")
        self.resizable(False, False)

        self.dados = None
        self.ultimo_tipo = "AFD"
        self.criar_interface()

    def criar_interface(self):

        Label(
            self,
            text="SIMULADOR DE AUTÔMATOS FINITOS",
            font=("Arial", 26, "bold"),
            fg="#1E3A8A",
            bg="#EAEAEA"
        ).pack(pady=15)

        principal = Frame(self, bg="white", bd=2, relief=RIDGE)
        principal.pack(fill=BOTH, expand=True, padx=20, pady=10)

        esquerda = Frame(principal, bg="white")
        esquerda.pack(side=LEFT, fill=Y, padx=20, pady=20)

        direita = Frame(principal, bg="#F7F7F7", bd=1, relief=SOLID)
        direita.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)

        Label(
            esquerda,
            text="Tipo de Autômato",
            font=("Arial", 13, "bold"),
            bg="white"
        ).pack(anchor="w")

        self.tipo = StringVar()
        self.tipo.set("AFD")

        Radiobutton(
            esquerda,
            text="AFD",
            variable=self.tipo,
            value="AFD",
            bg="white",
            font=("Arial", 11),
            command=self.atualizar_info_automato
        ).pack(anchor="w")

        Radiobutton(
            esquerda,
            text="AFN",
            variable=self.tipo,
            value="AFN",
            bg="white",
            font=("Arial", 11),
            command=self.atualizar_info_automato
        ).pack(anchor="w")

        Label(
            esquerda,
            text="\nArquivo JSON",
            font=("Arial", 13, "bold"),
            bg="white"
        ).pack(anchor="w")

        self.entryArquivo = Entry(esquerda, width=32, font=("Arial", 10))
        self.entryArquivo.pack()

        Button(
            esquerda,
            text="📂 Abrir Arquivo",
            width=20,
            height=2,
            bg="#E8EAF6",
            activebackground="#C5CAE9",
            font=("Arial", 10, "bold"),
            command=self.abrir_arquivo
        ).pack(pady=8)

        Label(
            esquerda,
            text="\nLista de Palavras",
            font=("Arial", 13, "bold"),
            bg="white"
        ).pack(anchor="w")

        Label(
            esquerda,
            text="Digite uma palavra por linha",
            font=("Arial", 9),
            bg="white",
            fg="gray"
        ).pack(anchor="w")

        self.entryPalavra = Text(
            esquerda,
            width=24,
            height=5,
            font=("Consolas", 11),
            bg="#FFFFFF"
        )
        self.entryPalavra.pack()

        self.btn_simular = Button(
            esquerda,
            text="▶ SIMULAR",
            width=20,
            height=2,
            bg="#1976D2",
            fg="white",
            activebackground="#0D47A1",
            activeforeground="white",
            font=("Arial", 10, "bold"),
            command=self.simular
        )
        self.btn_simular.pack(pady=8)

        self.btn_limpar = Button(
            esquerda,
            text="🗑 LIMPAR",
            width=20,
            height=2,
            bg="#757575",
            fg="white",
            activebackground="#424242",
            activeforeground="white",
            font=("Arial", 10, "bold"),
            command=self.limpar_campos
        )
        self.btn_limpar.pack(pady=5)

        Label(
            esquerda,
            text="\nInformações do Autômato",
            font=("Arial", 13, "bold"),
            bg="white"
        ).pack(anchor="w")

        frame_info = Frame(esquerda, bg="white")
        frame_info.pack(pady=5)

        self.scrollInfo = Scrollbar(frame_info)
        self.scrollInfo.pack(side=RIGHT, fill=Y)

        self.txtInfo = Text(
            frame_info,
            width=34,
            height=12,
            font=("Consolas", 9),
            bg="#FAFAFA",
            yscrollcommand=self.scrollInfo.set
        )
        self.txtInfo.pack(side=LEFT)

        self.scrollInfo.config(command=self.txtInfo.yview)

        self.txtInfo.insert(END, "Nenhum autômato carregado.")
        self.txtInfo.config(state=DISABLED)

        Label(
            direita,
            text="Resultado",
            font=("Arial", 16, "bold"),
            bg="#F7F7F7"
        ).pack()

        self.lblResultado = Label(
            direita,
            text="Aguardando...",
            fg="blue",
            font=("Arial", 18, "bold"),
            bg="#F7F7F7",
            width=36,
            pady=8
        )
        self.lblResultado.pack(pady=10)

        Label(
            direita,
            text="Caminho Percorrido",
            font=("Arial", 14, "bold"),
            bg="#F7F7F7"
        ).pack()

        frame_caminho = Frame(direita, bg="#F7F7F7")
        frame_caminho.pack(pady=8)

        self.scrollCaminho = Scrollbar(frame_caminho)
        self.scrollCaminho.pack(side=RIGHT, fill=Y)

        self.txtCaminho = Text(
            frame_caminho,
            width=72,
            height=11,
            font=("Consolas", 10),
            bg="#FFFFFF",
            yscrollcommand=self.scrollCaminho.set
        )
        self.txtCaminho.pack(side=LEFT)

        self.scrollCaminho.config(command=self.txtCaminho.yview)

        Label(
            direita,
            text="Representação Gráfica do Autômato",
            font=("Arial", 14, "bold"),
            bg="#F7F7F7"
        ).pack()

        self.canvas = Canvas(
            direita,
            width=780,
            height=300,
            bg="#FAFAFA",
            bd=2,
            relief=RIDGE
        )
        self.canvas.pack(pady=10)

        self.status = Label(
            self,
            text="Status: aguardando arquivo JSON.",
            anchor="w",
            font=("Arial", 9),
            bg="#EAEAEA",
            fg="#333333"
        )
        self.status.pack(fill=X, padx=20, pady=(0, 5))

    # ==================================
    # Abrir arquivo JSON
    # ==================================
    def abrir_arquivo(self):

        caminho = filedialog.askopenfilename(
            title="Selecione um arquivo JSON",
            filetypes=[("Arquivos JSON", "*.json")]
        )

        if caminho:
            try:
                leitor = LeitorJSON()
                self.dados = leitor.carregar(caminho)

                self.entryArquivo.delete(0, END)
                self.entryArquivo.insert(0, caminho)

                self.lblResultado.config(
                    text="Arquivo carregado com sucesso.",
                    fg="blue",
                    bg="#F7F7F7"
                )

                self.txtCaminho.delete("1.0", END)
                self.atualizar_info_automato()
                self.desenhar_automato(self.dados)

                self.status.config(
                    text=f"Status: arquivo carregado | Tipo selecionado: {self.tipo.get()}"
                )

            except Exception as erro:
                self.dados = None

                self.lblResultado.config(
                    text="Erro ao carregar JSON",
                    fg="#B71C1C",
                    bg="#FADADA"
                )

                self.txtCaminho.delete("1.0", END)
                self.txtCaminho.insert(END, str(erro))

                self.status.config(text="Status: erro ao carregar JSON.")

    # ==================================
    # Informações formais do autômato
    # ==================================
    def atualizar_info_automato(self):

        self.txtInfo.config(state=NORMAL)
        self.txtInfo.delete("1.0", END)

        if not self.dados:
            self.txtInfo.insert(END, "Nenhum autômato carregado.")
            self.txtInfo.config(state=DISABLED)
            return

        estados = self.dados.get("estados", [])
        alfabeto = self.dados.get("alfabeto", [])
        inicial = self.dados.get("estado_inicial", "")
        finais = self.dados.get("estados_finais", [])
        transicoes = self.dados.get("transicoes", {})

        linhas_transicoes = []
        quantidade = 0
        possui_epsilon = False

        for origem, trans in transicoes.items():
            for simbolo, destino in trans.items():

                if simbolo in ["ε", "epsilon"]:
                    possui_epsilon = True

                if isinstance(destino, list):
                    destino_txt = "{" + ", ".join(destino) + "}"

                    # Conta apenas destinos reais. Lista vazia representa nenhuma transição.
                    quantidade += len(destino)
                else:
                    destino_txt = destino
                    quantidade += 1

                linhas_transicoes.append(
                    f"δ({origem}, {simbolo}) = {destino_txt}"
                )

        texto = ""
        texto += "COMPONENTES DO AUTÔMATO\n"
        texto += "-" * 30 + "\n\n"
        texto += f"Q = {{{', '.join(estados)}}}\n\n"
        texto += f"Σ = {{{', '.join(alfabeto)}}}\n\n"
        texto += f"q₀ = {inicial}\n\n"
        texto += f"F = {{{', '.join(finais)}}}\n\n"
        texto += "δ (Função de Transição)\n"
        texto += "-" * 30 + "\n"

        for linha in linhas_transicoes:
            texto += linha + "\n"

        texto += "\n"
        texto += "-" * 30 + "\n"
        texto += f"Estados: {len(estados)}\n"
        texto += f"Transições reais: {quantidade}\n"

        if self.tipo.get() == "AFD":
            texto += "Tipo: Determinístico\n"
        else:
            texto += "Tipo: Não Determinístico\n"

        if possui_epsilon:
            texto += "Transições ε: Sim\n"
        else:
            texto += "Transições ε: Não\n"

        self.txtInfo.insert(END, texto)
        self.txtInfo.config(state=DISABLED)

    # ==================================
    # Simular lista de palavras
    # ==================================
    def simular(self):

        if not self.dados:
            self.lblResultado.config(
                text="Selecione um arquivo JSON",
                fg="#B71C1C",
                bg="#FADADA"
            )
            return

        conteudo = self.entryPalavra.get("1.0", END).strip()

        if conteudo == "":
            self.lblResultado.config(
                text="Digite ao menos uma palavra",
                fg="#B71C1C",
                bg="#FADADA"
            )
            return

        palavras = conteudo.splitlines()
        tipo_automato = self.tipo.get()
        self.ultimo_tipo = tipo_automato

        self.atualizar_info_automato()
        self.txtCaminho.delete("1.0", END)

        aceitas = 0
        rejeitadas = 0

        ultimos_estados_visitados = set()
        ultimas_transicoes_feitas = []

        self.txtCaminho.insert(END, "RESULTADO DA LISTA DE PALAVRAS\n")
        self.txtCaminho.insert(END, "=" * 55 + "\n\n")

        for palavra in palavras:

            palavra = palavra.strip()

            if palavra == "":
                continue

            try:
                simulador = Simulador(self.dados, tipo_automato)
                aceita, caminho = simulador.executar(palavra)

            except Exception as erro:
                self.lblResultado.config(
                    text="Erro na simulação",
                    fg="#B71C1C",
                    bg="#FADADA"
                )
                self.txtCaminho.insert(
                    END,
                    f"Erro ao simular '{palavra}': {erro}\n"
                )
                return

            if aceita:
                aceitas += 1
                resumo = "ACEITA"
            else:
                rejeitadas += 1
                resumo = "REJEITADA"

            estados_visitados = set()
            transicoes_feitas = []

            self.txtCaminho.insert(END, f"Palavra: {palavra}  ->  {resumo}\n")
            self.txtCaminho.insert(END, "-" * 55 + "\n")

            self.mostrar_caminho(
                palavra,
                caminho,
                aceita,
                tipo_automato,
                estados_visitados,
                transicoes_feitas
            )

            self.txtCaminho.insert(END, "\n" + "=" * 55 + "\n\n")

            ultimos_estados_visitados = estados_visitados
            ultimas_transicoes_feitas = transicoes_feitas

        total = aceitas + rejeitadas

        if total == 1:
            if aceitas == 1:
                self.lblResultado.config(
                    text="✔ PALAVRA ACEITA",
                    fg="#1B5E20",
                    bg="#DFF6DD"
                )
            else:
                self.lblResultado.config(
                    text="❌ PALAVRA REJEITADA",
                    fg="#B71C1C",
                    bg="#FADADA"
                )
        else:
            self.lblResultado.config(
                text=f"{aceitas} ACEITA(S) | {rejeitadas} REJEITADA(S)",
                fg="#1E3A8A",
                bg="#E8EAF6"
            )

        self.desenhar_automato(
            self.dados,
            estados_ativos=ultimos_estados_visitados,
            caminhos_ativos=ultimas_transicoes_feitas
        )

        self.status.config(
            text=f"Status: {tipo_automato} simulado | Total: {total} | Aceitas: {aceitas} | Rejeitadas: {rejeitadas}"
        )

    # ==================================
    # Mostrar caminho
    # ==================================
    def mostrar_caminho(
        self,
        palavra,
        caminho,
        aceita,
        tipo_automato,
        estados_visitados,
        transicoes_feitas
    ):

        if tipo_automato == "AFD":
            self.mostrar_caminho_afd(
                palavra,
                caminho,
                aceita,
                estados_visitados,
                transicoes_feitas
            )
        else:
            self.mostrar_caminho_afn(
                palavra,
                caminho,
                aceita,
                estados_visitados,
                transicoes_feitas
            )

    def mostrar_caminho_afd(
        self,
        palavra,
        caminho,
        aceita,
        estados_visitados,
        transicoes_feitas
    ):

        self.txtCaminho.insert(END, "Execução AFD:\n\n")

        for i, estado in enumerate(caminho):
            estados_visitados.add(estado)

            self.txtCaminho.insert(END, f"Passo {i}: Estado atual = {estado}\n")

            if i < len(caminho) - 1 and i < len(palavra):
                simbolo_lido = palavra[i]
                proximo_estado = caminho[i + 1]

                transicoes_feitas.append(
                    (estado, simbolo_lido, proximo_estado)
                )

                self.txtCaminho.insert(
                    END,
                    f"δ({estado}, {simbolo_lido}) = {proximo_estado}\n"
                )
                self.txtCaminho.insert(END, "↓\n\n")

        if aceita:
            self.txtCaminho.insert(END, "✔ Palavra aceita.\n")
        else:
            self.txtCaminho.insert(END, "❌ Palavra rejeitada.\n")

    def mostrar_caminho_afn(
        self,
        palavra,
        caminho,
        aceita,
        estados_visitados,
        transicoes_feitas
    ):

        self.txtCaminho.insert(END, "Execução AFN:\n\n")

        for i, conjunto_atual in enumerate(caminho):

            self.adicionar_estados_visitados(conjunto_atual, estados_visitados)

            self.txtCaminho.insert(
                END,
                f"Passo {i}: Estados atuais = {conjunto_atual}\n"
            )

            if i < len(caminho) - 1 and i < len(palavra):
                simbolo = palavra[i]
                proximo_conjunto = caminho[i + 1]

                self.txtCaminho.insert(
                    END,
                    f"Lendo '{simbolo}'\n"
                )
                self.txtCaminho.insert(
                    END,
                    f"δ({conjunto_atual}, {simbolo}) = {proximo_conjunto}\n"
                )
                self.txtCaminho.insert(END, "↓\n\n")

        transicoes_feitas.extend(
            self.inferir_transicoes_afn(palavra, caminho)
        )

        if aceita:
            self.txtCaminho.insert(END, "✔ Palavra aceita.\n")
        else:
            self.txtCaminho.insert(END, "❌ Palavra rejeitada.\n")

    # ==================================
    # Limpar
    # ==================================
    def limpar_campos(self):

        self.entryPalavra.delete("1.0", END)

        self.lblResultado.config(
            text="Aguardando...",
            fg="blue",
            bg="#F7F7F7"
        )

        self.txtCaminho.delete("1.0", END)

        if self.dados:
            self.desenhar_automato(self.dados)
        else:
            self.canvas.delete("all")

        self.status.config(text="Status: campos limpos.")

    # ==================================
    # Auxiliares AFN
    # ==================================
    def adicionar_estados_visitados(self, texto, estados_visitados):

        texto = str(texto)

        if texto.startswith("Símbolo inválido"):
            return

        texto = texto.replace("{", "")
        texto = texto.replace("}", "")
        texto = texto.replace("Ø", "")

        for parte in texto.split(","):
            estado = parte.strip()

            if estado:
                estados_visitados.add(estado)

    def texto_para_conjunto(self, texto):

        texto = str(texto)

        if texto == "Ø" or texto.startswith("Símbolo inválido"):
            return set()

        texto = texto.replace("{", "")
        texto = texto.replace("}", "")

        estados = set()

        for parte in texto.split(","):
            estado = parte.strip()

            if estado:
                estados.add(estado)

        return estados

    def inferir_transicoes_afn(self, palavra, caminho):

        transicoes_usadas = []
        transicoes = self.dados["transicoes"]

        for i, simbolo in enumerate(palavra):

            if i >= len(caminho) - 1:
                break

            estados_origem = self.texto_para_conjunto(caminho[i])
            estados_destino = self.texto_para_conjunto(caminho[i + 1])

            for origem in estados_origem:

                if origem not in transicoes:
                    continue

                if simbolo not in transicoes[origem]:
                    continue

                destinos = transicoes[origem][simbolo]

                if isinstance(destinos, str):
                    destinos = [destinos]

                for destino in destinos:

                    if destino in estados_destino:
                        transicoes_usadas.append(
                            (origem, simbolo, destino)
                        )

        return transicoes_usadas

    # ==================================
    # Desenho do autômato
    # ==================================
    def desenhar_automato(
        self,
        dados,
        estados_ativos=None,
        caminhos_ativos=None
    ):

        if estados_ativos is None:
            estados_ativos = set()

        if caminhos_ativos is None:
            caminhos_ativos = []

        self.canvas.delete("all")

        estados = dados["estados"]
        finais = dados["estados_finais"]
        inicial = dados.get("estado_inicial")

        x = 120
        y = 150
        distancia = 190

        posicoes = {}

        for estado in estados:

            posicoes[estado] = (x, y)

            cor_fundo = "#D9FDD3" if estado in estados_ativos else "white"
            cor_linha = "green" if estado in estados_ativos else "black"
            largura_linha = 3 if estado in estados_ativos else 2

            self.canvas.create_oval(
                x - 35,
                y - 35,
                x + 35,
                y + 35,
                width=largura_linha,
                fill=cor_fundo,
                outline=cor_linha
            )

            if estado in finais:
                self.canvas.create_oval(
                    x - 28,
                    y - 28,
                    x + 28,
                    y + 28,
                    width=2,
                    outline=cor_linha
                )

            self.canvas.create_text(
                x,
                y,
                text=estado,
                font=("Arial", 13, "bold"),
                fill="green" if estado in estados_ativos else "black"
            )

            x += distancia

        if inicial and inicial in posicoes:

            x_init, y_init = posicoes[inicial]
            cor_init = "green" if inicial in estados_ativos else "black"

            self.canvas.create_line(
                x_init - 90,
                y_init,
                x_init - 36,
                y_init,
                arrow=LAST,
                width=3,
                fill=cor_init
            )

            self.canvas.create_text(
                x_init - 100,
                y_init - 20,
                text="início",
                fill="green" if inicial in estados_ativos else "gray",
                font=("Arial", 9, "italic")
            )

        for origem in dados["transicoes"]:
            for simbolo in dados["transicoes"][origem]:
                destinos = dados["transicoes"][origem][simbolo]

                if isinstance(destinos, str):
                    destinos = [destinos]

                for destino in destinos:

                    if origem not in posicoes or destino not in posicoes:
                        continue

                    x1, y1 = posicoes[origem]
                    x2, y2 = posicoes[destino]

                    foi_usada = (origem, simbolo, destino) in caminhos_ativos

                    cor_transicao = "green" if foi_usada else "black"
                    espessura_linha = 3 if foi_usada else 1.5

                    if origem == destino:
                        self.desenhar_loop(
                            x1,
                            y1,
                            simbolo,
                            cor_transicao,
                            espessura_linha
                        )
                    else:
                        tem_inversa = self.tem_transicao_inversa(
                            origem,
                            destino,
                            dados["transicoes"]
                        )

                        self.desenhar_seta(
                            x1,
                            y1,
                            x2,
                            y2,
                            simbolo,
                            tem_inversa,
                            cor_transicao,
                            espessura_linha
                        )

    def desenhar_loop(self, x, y, simbolo, cor, espessura):

        self.canvas.create_arc(
            x - 30,
            y - 65,
            x + 30,
            y - 20,
            start=0,
            extent=300,
            style=ARC,
            width=espessura,
            outline=cor
        )

        self.canvas.create_text(
            x,
            y - 78,
            text=simbolo,
            fill="blue" if cor == "black" else cor,
            font=("Arial", 11, "bold")
        )

    def desenhar_seta(
        self,
        x1,
        y1,
        x2,
        y2,
        simbolo,
        tem_inversa,
        cor,
        espessura
    ):

        dx = x2 - x1
        dy = y2 - y1
        margem = 35
        distancia = (dx ** 2 + dy ** 2) ** 0.5

        if distancia <= 0:
            return

        x1_aj = x1 + (dx / distancia) * margem
        y1_aj = y1 + (dy / distancia) * margem
        x2_aj = x2 - (dx / distancia) * margem
        y2_aj = y2 - (dy / distancia) * margem

        if tem_inversa:

            mx = (x1_aj + x2_aj) / 2
            my = (y1_aj + y2_aj) / 2
            desvio = 28 if x1 < x2 else -28

            self.canvas.create_line(
                x1_aj,
                y1_aj,
                mx,
                my + desvio,
                x2_aj,
                y2_aj,
                smooth=True,
                arrow=LAST,
                width=espessura,
                fill=cor
            )

            self.canvas.create_text(
                mx,
                my + desvio - 15,
                text=simbolo,
                fill="blue" if cor == "black" else cor,
                font=("Arial", 11, "bold")
            )

        else:

            self.canvas.create_line(
                x1_aj,
                y1_aj,
                x2_aj,
                y2_aj,
                arrow=LAST,
                width=espessura,
                fill=cor
            )

            self.canvas.create_text(
                (x1_aj + x2_aj) / 2,
                (y1_aj + y2_aj) / 2 - 20,
                text=simbolo,
                fill="blue" if cor == "black" else cor,
                font=("Arial", 11, "bold")
            )

    def tem_transicao_inversa(self, origem, destino, transicoes):

        if destino not in transicoes:
            return False

        for destinos in transicoes[destino].values():

            if isinstance(destinos, str):
                destinos = [destinos]

            if origem in destinos:
                return True

        return False
