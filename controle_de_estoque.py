import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime


# VARIÁVEIS GLOBAIS

ARQUIVO_PRODUTOS = "produtos.json"
ARQUIVO_MOVIMENTOS = "movimentacoes.json"

produtos = []        # lista de dicionários com os produtos
movimentacoes = []   # lista de dicionários com entradas e saídas

# Cores usadas no título
COR_ESCURA = "#37474F"   # cinza escuro
COR_CIANO = "#00ACC1"    # ciano



# FUNÇÕES DE ARQUIVO (leitura e gravação em JSON)

def carregar_arquivo(nome_arquivo):
    """Lê um arquivo JSON e devolve uma lista. Se der erro, devolve lista vazia."""
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        # Arquivo ainda não existe (primeira vez que o sistema roda)
        return []
    except json.JSONDecodeError:
        messagebox.showwarning("Aviso", "O arquivo " + nome_arquivo + " está com dados inválidos.")
        return []
    except Exception as erro:
        messagebox.showerror("Erro", "Erro ao ler " + nome_arquivo + ": " + str(erro))
        return []


def salvar_arquivo(nome_arquivo, dados):
    """Grava uma lista em um arquivo JSON."""
    try:
        with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)
    except Exception as erro:
        messagebox.showerror("Erro", "Não foi possível salvar " + nome_arquivo + ": " + str(erro))



# FUNÇÕES AUXILIARES

def buscar_produto(codigo):
    """Procura um produto pelo código. Devolve o produto ou None."""
    for produto in produtos:
        if produto["codigo"] == codigo:
            return produto
    return None


def limpar_tabela(tabela):
    """Apaga todas as linhas de uma tabela (Treeview)."""
    for linha in tabela.get_children():
        tabela.delete(linha)



# JANELA PRINCIPAL

janela = tk.Tk()
janela.title("Controle de Estoque")
janela.geometry("760x580")

# Título no topo: faixa cinza escuro com uma linha ciano embaixo
tk.Label(janela, text="CONTROLE DE ESTOQUE", bg=COR_ESCURA, fg="white",
         font=("Segoe UI", 16, "bold"), pady=12).pack(fill="x")
tk.Frame(janela, bg=COR_CIANO, height=4).pack(fill="x")

# Agora que a janela existe, podemos carregar os dados
produtos = carregar_arquivo(ARQUIVO_PRODUTOS)
movimentacoes = carregar_arquivo(ARQUIVO_MOVIMENTOS)

# Abas do sistema
abas = ttk.Notebook(janela)
aba_produtos = ttk.Frame(abas)
aba_entrada = ttk.Frame(abas)
aba_saida = ttk.Frame(abas)
aba_consulta = ttk.Frame(abas)
aba_baixo = ttk.Frame(abas)
aba_historico = ttk.Frame(abas)

abas.add(aba_produtos, text="Produtos")
abas.add(aba_entrada, text="Entrada")
abas.add(aba_saida, text="Saída")
abas.add(aba_consulta, text="Consultar Estoque")
abas.add(aba_baixo, text="Estoque Baixo")
abas.add(aba_historico, text="Movimentações")
abas.pack(fill="both", expand=True, padx=5, pady=5)



# ABA 1 - CADASTRO DE PRODUTOS

tk.Label(aba_produtos, text="Código:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_codigo = tk.Entry(aba_produtos, width=10)
entry_codigo.grid(row=0, column=1, padx=5, pady=5, sticky="w")

tk.Label(aba_produtos, text="Nome:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
entry_nome = tk.Entry(aba_produtos, width=30)
entry_nome.grid(row=0, column=3, padx=5, pady=5, sticky="w")

tk.Label(aba_produtos, text="Quantidade:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_quantidade = tk.Entry(aba_produtos, width=10)
entry_quantidade.grid(row=1, column=1, padx=5, pady=5, sticky="w")

tk.Label(aba_produtos, text="Estoque mínimo:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
entry_minimo = tk.Entry(aba_produtos, width=10)
entry_minimo.grid(row=1, column=3, padx=5, pady=5, sticky="w")

tk.Label(aba_produtos, text="Preço (R$):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
entry_preco = tk.Entry(aba_produtos, width=10)
entry_preco.grid(row=2, column=1, padx=5, pady=5, sticky="w")

# Tabela que lista os produtos
tabela_produtos = ttk.Treeview(
    aba_produtos,
    columns=("codigo", "nome", "quantidade", "minimo", "preco"),
    show="headings",
    height=12,
)
tabela_produtos.heading("codigo", text="Código")
tabela_produtos.heading("nome", text="Nome")
tabela_produtos.heading("quantidade", text="Quantidade")
tabela_produtos.heading("minimo", text="Mínimo")
tabela_produtos.heading("preco", text="Preço (R$)")
tabela_produtos.column("codigo", width=70, anchor="center")
tabela_produtos.column("nome", width=250)
tabela_produtos.column("quantidade", width=90, anchor="center")
tabela_produtos.column("minimo", width=90, anchor="center")
tabela_produtos.column("preco", width=100, anchor="center")
tabela_produtos.grid(row=4, column=0, columnspan=4, padx=5, pady=10)


def limpar_campos_produto():
    """Limpa os campos de texto do cadastro."""
    entry_codigo.config(state="normal")
    entry_codigo.delete(0, tk.END)
    entry_nome.delete(0, tk.END)
    entry_quantidade.delete(0, tk.END)
    entry_minimo.delete(0, tk.END)
    entry_preco.delete(0, tk.END)


def ler_campos_produto(verificar_codigo_duplicado):
    """
    Lê e valida os campos do formulário.
    Devolve um dicionário com o produto, ou None se algo estiver errado.
    """
    try:
        codigo = int(entry_codigo.get())
    except ValueError:
        messagebox.showwarning("Atenção", "O código deve ser um número inteiro.")
        return None

    nome = entry_nome.get().strip()
    if nome == "":
        messagebox.showwarning("Atenção", "O nome é obrigatório.")
        return None

    try:
        quantidade = int(entry_quantidade.get())
        minimo = int(entry_minimo.get())
    except ValueError:
        messagebox.showwarning("Atenção", "Quantidade e estoque mínimo devem ser números inteiros.")
        return None

    if quantidade < 0 or minimo < 0:
        messagebox.showwarning("Atenção", "Quantidade e estoque mínimo não podem ser negativos.")
        return None

    try:
        # troca vírgula por ponto, para aceitar "79,90"
        preco = float(entry_preco.get().replace(",", "."))
    except ValueError:
        messagebox.showwarning("Atenção", "O preço deve ser um número.")
        return None

    if preco <= 0:
        messagebox.showwarning("Atenção", "O preço deve ser maior que zero.")
        return None

    # Código único (só verifica ao incluir)
    if verificar_codigo_duplicado and buscar_produto(codigo) is not None:
        messagebox.showwarning("Atenção", "Já existe um produto com esse código.")
        return None

    return {
        "codigo": codigo,
        "descricao": nome,
        "quantidade": quantidade,
        "estoque_minimo": minimo,
        "preco": preco,
    }


def incluir_produto():
    novo = ler_campos_produto(True)
    if novo is None:
        return
    produtos.append(novo)
    salvar_arquivo(ARQUIVO_PRODUTOS, produtos)
    limpar_campos_produto()
    atualizar_tudo()
    messagebox.showinfo("Sucesso", "Produto cadastrado!")


def alterar_produto():
    novo = ler_campos_produto(False)
    if novo is None:
        return
    produto = buscar_produto(novo["codigo"])
    if produto is None:
        messagebox.showwarning("Atenção", "Produto não encontrado. Selecione um da lista.")
        return
    # Atualiza os dados do produto existente
    produto["descricao"] = novo["descricao"]
    produto["quantidade"] = novo["quantidade"]
    produto["estoque_minimo"] = novo["estoque_minimo"]
    produto["preco"] = novo["preco"]
    salvar_arquivo(ARQUIVO_PRODUTOS, produtos)
    limpar_campos_produto()
    atualizar_tudo()
    messagebox.showinfo("Sucesso", "Produto alterado!")


def excluir_produto():
    try:
        codigo = int(entry_codigo.get())
    except ValueError:
        messagebox.showwarning("Atenção", "Selecione um produto na lista para excluir.")
        return
    produto = buscar_produto(codigo)
    if produto is None:
        messagebox.showwarning("Atenção", "Produto não encontrado.")
        return
    if messagebox.askyesno("Confirmar", "Deseja excluir " + produto["descricao"] + "?"):
        produtos.remove(produto)
        salvar_arquivo(ARQUIVO_PRODUTOS, produtos)
        limpar_campos_produto()
        atualizar_tudo()


def selecionar_produto(evento):
    """Quando o usuário clica numa linha da tabela, preenche os campos."""
    selecionado = tabela_produtos.selection()
    if not selecionado:
        return
    valores = tabela_produtos.item(selecionado[0])["values"]
    codigo = int(valores[0])
    produto = buscar_produto(codigo)
    if produto is None:
        return
    limpar_campos_produto()
    entry_codigo.insert(0, produto["codigo"])
    entry_nome.insert(0, produto["descricao"])
    entry_quantidade.insert(0, produto["quantidade"])
    entry_minimo.insert(0, produto["estoque_minimo"])
    entry_preco.insert(0, produto["preco"])


tabela_produtos.bind("<<TreeviewSelect>>", selecionar_produto)

frame_botoes = tk.Frame(aba_produtos)
frame_botoes.grid(row=3, column=0, columnspan=4, pady=5)
tk.Button(frame_botoes, text="Incluir", width=12, command=incluir_produto).pack(side="left", padx=5)
tk.Button(frame_botoes, text="Alterar", width=12, command=alterar_produto).pack(side="left", padx=5)
tk.Button(frame_botoes, text="Excluir", width=12, command=excluir_produto).pack(side="left", padx=5)
tk.Button(frame_botoes, text="Limpar", width=12, command=limpar_campos_produto).pack(side="left", padx=5)


# ABAS 2 e 3 - ENTRADA E SAÍDA DE MERCADORIAS

def criar_tela_movimento(aba, tipo):
    """
    Monta a tela de entrada ou saída (a tela é igual, só muda o tipo).
    tipo = "Entrada" ou "Saída". Devolve o combobox para ser atualizado depois.
    """
    tk.Label(aba, text="Produto:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    combo = ttk.Combobox(aba, width=40, state="readonly")
    combo.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(aba, text="Quantidade:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    entry_qtd = tk.Entry(aba, width=15)
    entry_qtd.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    tk.Label(aba, text="Data (dd/mm/aaaa):").grid(row=2, column=0, padx=10, pady=10, sticky="e")
    entry_data = tk.Entry(aba, width=15)
    entry_data.grid(row=2, column=1, padx=10, pady=10, sticky="w")
    entry_data.insert(0, datetime.now().strftime("%d/%m/%Y"))  # data de hoje

    def registrar():
        registrar_movimento(tipo, combo, entry_qtd, entry_data)

    tk.Button(aba, text="Registrar " + tipo, width=20, command=registrar).grid(
        row=3, column=1, padx=10, pady=15, sticky="w"
    )
    return combo


def registrar_movimento(tipo, combo, entry_qtd, entry_data):
    """Registra uma entrada ou saída de mercadoria."""
    # 1) Produto escolhido
    texto = combo.get()
    if texto == "":
        messagebox.showwarning("Atenção", "Escolha um produto.")
        return
    codigo = int(texto.split(" - ")[0])
    produto = buscar_produto(codigo)

    # 2) Quantidade
    try:
        quantidade = int(entry_qtd.get())
    except ValueError:
        messagebox.showwarning("Atenção", "A quantidade deve ser um número inteiro.")
        return
    if quantidade <= 0:
        messagebox.showwarning("Atenção", "A quantidade deve ser maior que zero.")
        return

    # 3) Data
    data = entry_data.get().strip()
    try:
        datetime.strptime(data, "%d/%m/%Y")
    except ValueError:
        messagebox.showwarning("Atenção", "Data inválida. Use o formato dd/mm/aaaa.")
        return

    # 4) Atualiza o estoque
    if tipo == "Entrada":
        produto["quantidade"] = produto["quantidade"] + quantidade
    else:
        if quantidade > produto["quantidade"]:
            messagebox.showwarning(
                "Atenção",
                "Estoque insuficiente! Disponível: " + str(produto["quantidade"]),
            )
            return
        produto["quantidade"] = produto["quantidade"] - quantidade

    # 5) Guarda no histórico
    movimentacoes.append({
        "tipo": tipo,
        "codigo": codigo,
        "produto": produto["descricao"],
        "quantidade": quantidade,
        "data": data,
    })

    salvar_arquivo(ARQUIVO_PRODUTOS, produtos)
    salvar_arquivo(ARQUIVO_MOVIMENTOS, movimentacoes)
    entry_qtd.delete(0, tk.END)
    atualizar_tudo()
    messagebox.showinfo("Sucesso", tipo + " registrada com sucesso!")


combo_entrada = criar_tela_movimento(aba_entrada, "Entrada")
combo_saida = criar_tela_movimento(aba_saida, "Saída")


# ABA 4 - CONSULTA DE ESTOQUE

tipo_busca = tk.StringVar(value="codigo")  # guarda a opção escolhida

tk.Label(aba_consulta, text="Buscar por:").grid(row=0, column=0, padx=5, pady=10)
tk.Radiobutton(aba_consulta, text="Código", variable=tipo_busca, value="codigo").grid(row=0, column=1)
tk.Radiobutton(aba_consulta, text="Nome", variable=tipo_busca, value="nome").grid(row=0, column=2)
entry_busca = tk.Entry(aba_consulta, width=25)
entry_busca.grid(row=0, column=3, padx=5)

tabela_consulta = ttk.Treeview(
    aba_consulta, columns=("codigo", "nome", "quantidade"), show="headings", height=14
)
tabela_consulta.heading("codigo", text="Código")
tabela_consulta.heading("nome", text="Produto")
tabela_consulta.heading("quantidade", text="Quantidade")
tabela_consulta.column("codigo", width=80, anchor="center")
tabela_consulta.column("nome", width=350)
tabela_consulta.column("quantidade", width=100, anchor="center")
tabela_consulta.grid(row=2, column=0, columnspan=5, padx=10, pady=10)


def mostrar_consulta(lista):
    """Mostra uma lista de produtos na tabela de consulta."""
    limpar_tabela(tabela_consulta)
    for p in lista:
        tabela_consulta.insert("", tk.END, values=(
            str(p["codigo"]).zfill(3), p["descricao"], p["quantidade"]
        ))


def consultar():
    texto = entry_busca.get().strip()
    if texto == "":
        mostrar_consulta(produtos)  # sem texto: mostra todos
        return
    resultado = []
    if tipo_busca.get() == "codigo":
        try:
            codigo = int(texto)
        except ValueError:
            messagebox.showwarning("Atenção", "Digite um código numérico.")
            return
        for p in produtos:
            if p["codigo"] == codigo:
                resultado.append(p)
    else:
        for p in produtos:
            if texto.lower() in p["descricao"].lower():
                resultado.append(p)
    mostrar_consulta(resultado)
    if len(resultado) == 0:
        messagebox.showinfo("Consulta", "Nenhum produto encontrado.")


def mostrar_todos():
    entry_busca.delete(0, tk.END)
    mostrar_consulta(produtos)


tk.Button(aba_consulta, text="Consultar", command=consultar).grid(row=0, column=4, padx=5)
tk.Button(aba_consulta, text="Mostrar todos", command=mostrar_todos).grid(row=1, column=4, padx=5)


# ABA 5 - ESTOQUE BAIXO

tabela_baixo = ttk.Treeview(
    aba_baixo, columns=("produto", "quantidade", "minimo"), show="headings", height=16
)
tabela_baixo.heading("produto", text="Produto")
tabela_baixo.heading("quantidade", text="Quantidade")
tabela_baixo.heading("minimo", text="Mínimo")
tabela_baixo.column("produto", width=350)
tabela_baixo.column("quantidade", width=100, anchor="center")
tabela_baixo.column("minimo", width=100, anchor="center")
tabela_baixo.pack(padx=10, pady=10)


def atualizar_baixo():
    """Mostra os produtos com quantidade <= estoque mínimo."""
    limpar_tabela(tabela_baixo)
    for p in produtos:
        if p["quantidade"] <= p["estoque_minimo"]:
            tabela_baixo.insert("", tk.END, values=(
                p["descricao"], p["quantidade"], p["estoque_minimo"]
            ))



# ABA 6 - HISTÓRICO DE MOVIMENTAÇÕES (relatório simples)

tabela_historico = ttk.Treeview(
    aba_historico,
    columns=("data", "tipo", "produto", "quantidade"),
    show="headings",
    height=16,
)
tabela_historico.heading("data", text="Data")
tabela_historico.heading("tipo", text="Tipo")
tabela_historico.heading("produto", text="Produto")
tabela_historico.heading("quantidade", text="Quantidade")
tabela_historico.column("data", width=100, anchor="center")
tabela_historico.column("tipo", width=90, anchor="center")
tabela_historico.column("produto", width=300)
tabela_historico.column("quantidade", width=100, anchor="center")
tabela_historico.pack(padx=10, pady=10)


def atualizar_historico():
    limpar_tabela(tabela_historico)
    for m in movimentacoes:
        tabela_historico.insert("", tk.END, values=(
            m["data"], m["tipo"], m["produto"], m["quantidade"]
        ))



# ATUALIZAÇÃO GERAL DAS TELAS

def atualizar_tudo():
    """Atualiza todas as tabelas e listas depois de qualquer mudança."""
    # Tabela de produtos
    limpar_tabela(tabela_produtos)
    for p in produtos:
        tabela_produtos.insert("", tk.END, values=(
            p["codigo"], p["descricao"], p["quantidade"],
            p["estoque_minimo"], "%.2f" % p["preco"]
        ))

    # Listas de escolha de produto (entrada e saída)
    lista_nomes = []
    for p in produtos:
        lista_nomes.append(str(p["codigo"]) + " - " + p["descricao"])
    combo_entrada["values"] = lista_nomes
    combo_saida["values"] = lista_nomes
    combo_entrada.set("")
    combo_saida.set("")

    mostrar_consulta(produtos)
    atualizar_baixo()
    atualizar_historico()


# ---------------------------------------------------------------
# INÍCIO DO PROGRAMA
# ---------------------------------------------------------------
atualizar_tudo()
janela.mainloop()