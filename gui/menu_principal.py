from tkinter import *
from . import menu_partida, menu_jogadores, continuar

__all__ = ['transicao']


def transicao( window ):
    if window._frame:
        window._frame.destroy()

    fr_menuPrincipal = Frame(window)
    fr_menuPrincipal.pack(padx = (100, 100), pady = (50,100))

    lb_title = Label(fr_menuPrincipal, text = "Yahtzee", fg = "black", font = "none 30 bold")
    lb_title.pack( pady = (10, 50))

    fr_botoes = Frame( fr_menuPrincipal )
    fr_botoes.pack()

    bt_novaPartida = Button(fr_botoes, text = "Nova Partida", command = lambda: menu_partida.transicao(window))
    bt_novaPartida.pack( pady = (5,5), fill = X )

    bt_novaPartida = Button(fr_botoes, text = "Continuar", command = lambda: continuar.transicao(window))
    bt_novaPartida.pack( pady = (5,5), fill = X)

    bt_novaPartida = Button(fr_botoes, text = "Jogadores", command = lambda: menu_jogadores.transicao(window))
    bt_novaPartida.pack( pady = (5,5), fill = X)

    bt_sairDoJogo = Button( fr_botoes, text = "Sair do Jogo", command = lambda: window.destroy() )
    bt_sairDoJogo.pack( pady = (5,5), fill = X)


    window._frame = fr_menuPrincipal
