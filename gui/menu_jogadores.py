from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview, Scrollbar
from . import menu_principal
from entidades import jogador

def atualiza_lista_jogadores( tree ):
    jogadores = jogador.obtem_info([])
    tree.delete(*tree.get_children())
    #para ordenar pelo ranking:
    jogadores.sort(key = lambda x: float('inf') if x.get('ranking') is None else x.get('ranking'))
    
    for i, cada_jogador in enumerate(jogadores):
        tree.insert('',i,values = (cada_jogador['nome'],
                                     cada_jogador['recorde'],
                                     cada_jogador['pontuacao_total'],
                                     cada_jogador['ranking']))

def cria_frame_novoJogador(parent, tree):
    def insere( tree ):
        nome = et_nome.get().strip()
        if len(nome) > 11:
            messagebox.showerror("Erro","Tamanho máximo do nome: 11 caracteres.")
            et_nome.delete(0,END)
        else:
            retorno = jogador.insere(nome)
            if retorno == 1:
                messagebox.showerror("Erro","O nome não pode ser vazio")
            elif retorno == 2:
                messagebox.showerror("Erro","Já existe um jogador com o nome escolhido")
            else:
                messagebox.showinfo("Info", "Jogador Criado")
                atualiza_lista_jogadores( tree )
            et_nome.delete(0,END)
    
    fr_novoJogador = Frame( parent, bd = 1, relief = SOLID)
    fr_novoJogador.pack( side = 'top', padx = 10, pady=(45, 10) )

    lb_novoJogador = Label( fr_novoJogador, text = "Criar novo jogador:" )
    lb_novoJogador.pack(pady = (5,10), padx = (10,10))

    lb_nome = Label( fr_novoJogador, text = "Nome" , anchor = W) 
    lb_nome.pack( anchor = W, padx = 5 )
    et_nome = Entry( fr_novoJogador )
    et_nome.pack(padx = 5, pady = (0,5))

    bt_novoJogador = Button(fr_novoJogador, text = "Criar", command = lambda:insere(tree))
    bt_novoJogador.pack(fill = X, padx = 5, pady = 5)

def cria_label_titulo( parent ):
    lb_title = Label(parent, text = "Ranking dos Jogadores", fg = "black", font = "none 20 bold")
    lb_title.config(anchor = 'center')
    lb_title.pack(side = 'top', pady = 10)

def remove_jogador(parent, tabela):
    if tabela.selection():
        confirmacao = messagebox.askyesno('Remover',
                                          'Deseja remover permanentemente este jogador?')
        if not confirmacao:
            return
        for item in tabela.selection():
            removido = tabela.item(item, "values")[0]
            tabela.delete(item)
        if jogador.remove(removido) == 0:
            messagebox.showinfo("Info", "Jogador Removido")
    else:
        messagebox.showerror("Erro","É preciso selecionar pelo menos um jogador.")

def mostra_ranking(parent):
    columns = ("zero","um","dois","tres")
    tabela = Treeview(parent, selectmode='browse', show="headings", columns=columns)
    
    tabela.column("zero", width=200)
    tabela.column("um", width=70)
    tabela.column("dois", width=100)
    tabela.column("tres", width=70)

    tabela.heading("zero",text="Jogador",anchor='center')
    tabela.heading("um", text="Recorde",anchor='center')
    tabela.heading("dois", text="Pontuação Total",anchor='center')
    tabela.heading("tres", text="Posição",anchor='center')

    tabela.pack(side='left', fill=BOTH, pady = 10, padx = 10)
    vsb = Scrollbar(parent, orient="vertical",command=tabela.yview)
    vsb.pack(side='left', fill='y')
    tabela.configure(yscrollcommand=vsb.set)

    atualiza_lista_jogadores(tabela)

    return tabela

def transicao( window ):
    if window._frame:
        window._frame.destroy()

    fr_ranking = Frame(window)
    fr_ranking.pack()
    
    cria_label_titulo(fr_ranking)

    tabela = mostra_ranking(fr_ranking)

    cria_frame_novoJogador(fr_ranking, tabela)

    bt_voltar = Button(fr_ranking, text = "Voltar", command = lambda: menu_principal.transicao(window))
    bt_voltar.pack( pady = (75,5))

    bt_remover = Button(fr_ranking, text = "Remover Jogador", command = lambda: remove_jogador(window, tabela))
    bt_remover.pack( pady = (5,5))

    window._frame = fr_ranking
