from tkinter import *
from tkinter import messagebox
from entidades import jogador

jogadores_escolhidos = []

def atualiza_lista_jogadores( fr_lista ):
    nomes_jogadores = [ dados_jogador['nome'] for dados_jogador in jogador.obtem_info([]) ]
    for filho in fr_lista.winfo_children():
        filho.destroy()
    for nome in nomes_jogadores:
        Button(fr_lista, text=nome).pack(padx=(0,0), fill='x')

def cria_label_titulo( parent ):
    lb_title = Label(parent, text = "Escolha os jogadores:", fg = "black", font = "none 20 bold")
    lb_title.config(anchor = 'center')
    lb_title.pack(side = 'top', pady = 10)

def cria_frame_novoJogador(parent, fr_lista):
    def insere( fr_lista ):
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
            elif retorno == 0:
                messagebox.showinfo("Info", "Jogador Criado. Agora ele pode ser escholido para jogar.")
                parent.focus()
                atualiza_lista_jogadores( fr_lista )
            et_nome.delete(0,END)
    
    fr_novoJogador = Frame( parent, bd = 1, relief = SOLID)
    fr_novoJogador.pack( side = 'left', padx = 10, pady=50 )

    lb_novoJogador = Label( fr_novoJogador, text = "Criar novo jogador:" )
    lb_novoJogador.pack(pady = (5,10), padx = (10,10))

    lb_nome = Label( fr_novoJogador, text = "Nome" , anchor = W) 
    lb_nome.pack( anchor = W, padx = 5 )
    et_nome = Entry( fr_novoJogador )
    et_nome.pack(padx = 5, pady = (0,5))

    bt_novoJogador = Button(fr_novoJogador, text = "Criar", command = lambda:insere(fr_lista))
    bt_novoJogador.pack(fill = X, padx = 5, pady = 5)


def cria_frame_lista_de_jogadores(parent):
    # para fazer a rolagem é preciso ter um frame dentro um canvas

    # container externo com borda
    fr_containerLista = Frame( parent, bd=1, relief=SOLID)
    fr_containerLista.pack(side='left', pady=50, padx=(10,10) )

    # canvas
    cv_lista = Canvas( fr_containerLista , width=116)

    #barra de rolagem
    scroll_y = Scrollbar( fr_containerLista, orient = 'vertical', command = cv_lista.yview) 

    scroll_x = Scrollbar( fr_containerLista, orient = 'horizontal', command = cv_lista.xview) 

    # frame interno
    fr_lista = Frame( cv_lista )
    fr_lista.bind( "<Configure>",
                lambda e: cv_lista.configure(scrollregion=cv_lista.bbox("all")) 
    )
    cv_lista.create_window((0,0), window=fr_lista, anchor='nw', width=116)
    cv_lista.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    scroll_y.pack( side = 'right', fill = 'y')
    scroll_x.pack( side='bottom', fill = 'x')
    cv_lista.pack( fill = 'x', expand = True)
    return fr_lista


def transicao( window ):
    window._frame.destroy()
    fr_menuPartida = Frame(window)
    fr_menuPartida.pack()

    cria_label_titulo( fr_menuPartida )

    fr_lista = cria_frame_lista_de_jogadores( fr_menuPartida )
    atualiza_lista_jogadores(fr_lista)
    
    cria_frame_novoJogador( fr_menuPartida, fr_lista )


    window._frame = fr_menuPartida
