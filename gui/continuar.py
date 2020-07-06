from tkinter import *
from tkinter import messagebox, filedialog
from . import menu_principal, partida as partida_gui
from entidades import partida
import os
import importlib

def cria_label_titulo( parent ):
    lb_title = Label(parent, text = "Continuar Partida", fg = "black", font = "none 20 bold")
    lb_title.config(anchor = 'center')
    lb_title.pack(side = 'top', pady = 10)

def escolhe_arquivo( parent):
    diretorio_jogopy = os.getcwd()
    diretorio_saves = os.path.join(diretorio_jogopy, "saves")
    parent.nome_arquivo = filedialog.askopenfilename(initialdir = diretorio_saves,
                                                     title = "Escolha arquivo do save",
                                                     filetypes = (("xml files","*.xml"),))
    if parent.nome_arquivo:
        if partida.obtem_info_partida()!= 1:
            importlib.reload(partida)
            importlib.reload(partida_gui)
        retorno = partida.continua_partida(parent.nome_arquivo)
        if retorno == 1:
            messagebox.showerror("Erro", "Não foi possível ler o arquivo")
        else:
            partida_gui.transicao(parent)

def transicao( window ):
    if window._frame:
        window._frame.destroy()

    fr_continuar = Frame(window)
    fr_continuar.pack(padx=20, pady=20)
    
    cria_label_titulo(fr_continuar)

    bt_voltar = Button(fr_continuar, text = "Voltar ao Menu Principal", command = lambda: menu_principal.transicao(window))
    bt_voltar.pack(side = 'bottom', padx = 20, pady = (15))

    bt_escolher = Button(fr_continuar, text = "Escolher arquivo do save", command = lambda: escolhe_arquivo(window))
    bt_escolher.pack( padx = 20)

    window._frame = fr_continuar
