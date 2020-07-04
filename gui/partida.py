
from entidades import partida
from tkinter import *

def transicao( window ):
    if window._frame:
        window._frame.destroy()

    window.config(cursor = 'arrow')

    fr_partida = Frame(window)
    fr_partida.pack()

    jogadores = partida.obtem_info_partida()['jogadores']
    for jogador in jogadores:
        Label(fr_partida, text = jogador).pack()

