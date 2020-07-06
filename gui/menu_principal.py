from tkinter import *
from . import menu_partida, menu_jogadores, continuar

def transicao( window ):
    if window._frame:
        window._frame.destroy()

    fr_menuPrincipal = Frame(window)
    fr_menuPrincipal.pack(padx = (100, 100), pady = (50,100))

    lb_title = Label(fr_menuPrincipal, text = "Yahtzee", fg = "black", font = "none 30 bold")
    lb_title.pack( pady = (10, 50))

    bt_novaPartida = Button(fr_menuPrincipal, text = "Nova Partida", command = lambda: menu_partida.transicao(window))
    bt_novaPartida.pack( pady = (5,5))

    bt_novaPartida = Button(fr_menuPrincipal, text = "Continuar", command = lambda: continuar.transicao(window))
    bt_novaPartida.pack( pady = (5,5))

    bt_novaPartida = Button(fr_menuPrincipal, text = "Jogadores", command = lambda: menu_jogadores.transicao(window))
    bt_novaPartida.pack( pady = (5,5))

    window._frame = fr_menuPrincipal
