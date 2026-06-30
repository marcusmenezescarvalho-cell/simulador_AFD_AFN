# Simulador de Autômatos Finitos (AFD e AFN)

## Descrição

Este projeto consiste na implementação de um **Simulador de Autômatos Finitos Determinísticos (AFD)** e **Autômatos Finitos Não Determinísticos (AFN)**, desenvolvido em **Python** utilizando a biblioteca **Tkinter** para a interface gráfica.

O simulador permite carregar um autômato definido em um arquivo **JSON**, realizar a simulação de uma ou mais palavras e informar se elas são aceitas ou rejeitadas pelo autômato, além de exibir o caminho percorrido durante a execução e representar graficamente o autômato.

O projeto foi desenvolvido como trabalho da disciplina **Linguagens Formais e Autômatos**.

---

# Funcionalidades

✔ Simulação de AFD

✔ Simulação de AFN

✔ Leitura automática de arquivos JSON

✔ Interface gráfica desenvolvida em Tkinter

✔ Simulação de uma ou várias palavras

✔ Exibição do resultado (Aceita/Rejeitada)

✔ Exibição detalhada do caminho percorrido

✔ Representação gráfica do autômato

✔ Destaque visual dos estados e transições percorridas

✔ Exibição dos componentes formais do autômato (Q, Σ, δ, q₀ e F)

✔ Informações do autômato carregado

---

# Tecnologias Utilizadas

- Python 3
- Tkinter
- JSON
- Programação Orientada a Objetos (POO)

---

# Estrutura do Projeto

```text
Simulador_AFD_AFN/

│
├── main.py
├── README.md
├── requirements.txt
├── environment.yml
│
├── src/
│   ├── interface.py
│   ├── automato.py
│   ├── afd.py
│   ├── afn.py
│   ├── simulador.py
│   └── leitor_json.py
│
├── exemplos/
│   ├── afd.json
│   └── afn.json
│
└── imagens/
```

---

# Arquitetura do Sistema

O projeto foi desenvolvido utilizando Programação Orientada a Objetos.

Cada classe possui uma responsabilidade específica.

```text
            Interface
                │
                ▼
           Simulador
          ┌──────────┐
          ▼          ▼
        AFD         AFN
          │
          ▼
      Automato
```

### Interface

Responsável pela interação com o usuário.

Realiza:

- abertura do arquivo JSON;
- leitura das palavras;
- exibição do resultado;
- desenho do autômato.

---

### Simulador

Responsável por identificar o tipo de autômato selecionado (AFD ou AFN) e executar o algoritmo correspondente.

---

### Automato

Classe base contendo todas as informações comuns aos autômatos.

- estados
- alfabeto
- estado inicial
- estados finais
- transições

---

### AFD

Implementa o algoritmo de simulação de Autômatos Determinísticos.

---

### AFN

Implementa o algoritmo de simulação de Autômatos Não Determinísticos utilizando conjuntos de estados.

---

### LeitorJSON

Responsável pela leitura e carregamento do arquivo JSON contendo a definição do autômato.

---

# Formato do Arquivo JSON

 Exemplo de Arquivo JSON (AFD)

```json
{
  "tipo": "AFD",
  "estados": ["q0", "q1"],
  "alfabeto": ["a", "b"],
  "estado_inicial": "q0",
  "estados_finais": ["q1"],
  "transicoes": {
    "q0": {
      "a": "q1",
      "b": "q0"
    },
    "q1": {
      "a": "q1",
      "b": "q0"
    }
  }
}
```

Exemplo de um AFN:

```json
{
    "estados": ["q0", "q1", "q2"],

    "alfabeto": ["a", "b"],

    "estado_inicial": "q0",

    "estados_finais": ["q2"],

    "transicoes": {

        "q0": {

            "a": ["q0","q1"],

            "b": []

        },

        "q1": {

            "a": [],

            "b": ["q2"]

        },

        "q2": {

            "a": [],

            "b": []

        }

    }

}
```

## Arquivos de Exemplo

O projeto já contém arquivos JSON prontos para teste:

- `teste_afd.json` – exemplo de Autômato Finito Determinístico (AFD).
- `teste_afn.json` – exemplo de Autômato Finito Não Determinístico (AFN).

Basta abrir um desses arquivos no simulador para realizar os testes.

---
## Requisitos

- Python 3.11
- Conda (Miniconda ou Anaconda)

# Como Executar

1. Clone o repositório.

```bash
git clone https://github.com/marcusmenezescarvalho-cell/simulador_AFD_AFN.git
```

2. Entre na pasta.

```bash
cd simulador_AFD_AFN
```

3. Crie o ambiente Conda.

```bash
conda env create -f environment.yml
```

4. Ative o ambiente.

```bash
conda activate simulador-afd-afn
```

5. Execute o programa.

```bash
python main.py
```

# Como Utilizar

1. Execute o programa.

2. Escolha o tipo do autômato (AFD ou AFN).

3. Clique em **Abrir Arquivo**.

4. Selecione um arquivo JSON.

5. Digite uma ou mais palavras.

6. Clique em **SIMULAR**.

O programa exibirá:

- resultado da simulação;
- caminho percorrido;
- representação gráfica;
- informações do autômato.

---

# Exemplo de Simulação

Entrada:

```text
ab
aa
aab
abb
```

Saída:

```text
ab   -> ACEITA

aa   -> REJEITADA

aab  -> ACEITA

abb  -> REJEITADA
```

---

# Interface do Sistema

A interface gráfica apresenta:

- seleção do tipo do autômato;

- abertura de arquivos JSON;

- entrada de palavras;

- informações do autômato;

- resultado da simulação;

- caminho percorrido;

- desenho do autômato.

*(Recomenda-se inserir uma captura de tela da interface nesta seção.)*

---

# Componentes Formais do Autômato

O simulador apresenta automaticamente:

- Q (Conjunto de Estados)

- Σ (Alfabeto)

- δ (Função de Transição)

- q₀ (Estado Inicial)

- F (Estados Finais)

---

# Limitações

A implementação do AFN não contempla transições ε (epsilon), trabalhando apenas com autômatos não determinísticos sem ε-transições.

---

# Possíveis Melhorias Futuras

- Suporte a transições ε.

- Posicionamento automático dos estados.

- Exportação do resultado para arquivo.

- Animação da execução da palavra.

- Geração automática do desenho em formato SVG.

---


Projeto desenvolvido para a disciplina **Linguagens Formais e Autômatos**.

---

# Licença

Este projeto foi desenvolvido exclusivamente para fins acadêmicos.