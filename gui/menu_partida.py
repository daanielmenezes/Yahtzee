from tkinter import *
from tkinter import messagebox
from entidades import jogador, partida
from . import menu_principal, partida as partida_gui
import time
import threading

def atualiza_lista_jogadores( listbox ):
    nomes_jogadores = [ dados_jogador['nome'] for dados_jogador in jogador.obtem_info([]) ]
    listbox.delete(0, END)
    for nome in nomes_jogadores:
        listbox.insert(END, nome) 

def cria_label_titulo( parent ):
    lb_title = Label(parent, text = "Escolha os jogadores:", fg = "black", font = "none 20 bold")
    lb_title.config(anchor = 'center')
    lb_title.pack(side = 'top', pady = 10)

def cria_frame_novoJogador(parent, listbox):
    def insere( listbox ):
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
                messagebox.showinfo("Info", "Jogador Criado. Agora ele pode ser escholido para jogar.")
                atualiza_lista_jogadores( listbox )
            et_nome.delete(0,END)
    
    fr_novoJogador = Frame( parent, bd = 1, relief = SOLID)
    fr_novoJogador.pack( side = 'top', padx = 10, pady=(45, 10) )

    lb_novoJogador = Label( fr_novoJogador, text = "Criar novo jogador:" )
    lb_novoJogador.pack(pady = (5,10), padx = (10,10))

    lb_nome = Label( fr_novoJogador, text = "Nome" , anchor = W) 
    lb_nome.pack( anchor = W, padx = 5 )
    et_nome = Entry( fr_novoJogador )
    et_nome.pack(padx = 5, pady = (0,5))

    bt_novoJogador = Button(fr_novoJogador, text = "Criar", command = lambda:insere(listbox))
    bt_novoJogador.pack(fill = X, padx = 5, pady = 5)


def cria_frame_lista_de_jogadores(parent):
    # para fazer a rolagem é preciso ter um frame dentro um canvas

    # container externo com borda
    fr_containerLista = Frame( parent, bd=1, relief=SOLID)
    fr_containerLista.pack(side='left', pady=45, padx=(10,10) )

    listbox_nomes = Listbox( fr_containerLista , height=11, width=20,
                           selectmode=MULTIPLE, relief=FLAT, activestyle = 'none')

    #barra de rolagem
    scroll_y = Scrollbar( fr_containerLista, orient = 'vertical', command = listbox_nomes.yview) 
    scroll_x = Scrollbar( fr_containerLista, orient = 'horizontal', command = listbox_nomes.xview) 

    # frame interno
    listbox_nomes.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    scroll_y.pack( side = 'right', fill = 'y')
    scroll_x.pack( side='bottom', fill = 'x')
    listbox_nomes.pack( fill = 'x', expand = True)
    return listbox_nomes

def inicia_partida( window, listbox ):
    # macete com threding para não travar a aplicação enquanto acessa o bd
    def thread_inicia_partida():
        retorno = partida.inicia_partida(nomes)

        if retorno == 1:
            messagebox.showerror("Erro","Jogador inválido escolhido.")
            window.config(cursor="arrow")

        elif retorno == 2:
            messagebox.showerror("Erro","Há uma outra partida em andamento.")
            window.config(cursor="arrow")
        else:
            partida_gui.transicao( window )

    # nomes selecionados na listbox
    nomes = [listbox.get(idx) for idx in listbox.curselection()]
    if nomes:
        #cursor de loading pq inicia_partida demora um pouco
        window.config(cursor="watch")
        window.update()

        #executa a função de cima um uma nova thread
        threading.Thread(target=thread_inicia_partida).start()
    else:
        messagebox.showerror("Erro","É preciso selecionar pelo menos um jogador.")

def transicao( window ):
    if window._frame:
        window._frame.destroy()

    fr_menuPartida = Frame(window)
    fr_menuPartida.pack()

    cria_label_titulo( fr_menuPartida )

    listbox = cria_frame_lista_de_jogadores( fr_menuPartida )
    atualiza_lista_jogadores(listbox)
    
    cria_frame_novoJogador( fr_menuPartida, listbox )

    bt_voltar = Button(fr_menuPartida, text="Voltar ao Menu Principal", command=lambda: menu_principal.transicao(window))
    bt_inicia = Button(fr_menuPartida, text="Iniciar Partida", command=lambda: inicia_partida(window, listbox))
    bt_inicia.pack(fill='x', padx=5, pady=5)
    bt_voltar.pack(fill='x', padx=5, pady=5)

    window._frame = fr_menuPartida
