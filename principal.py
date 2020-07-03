from tkinter import *
from tkinter import ttk
import gui.menu_partida as menuPartida

window = Tk()
window.title("Yahtzee")

fr_menuPrincipal = Frame(window)
fr_menuPrincipal.pack(padx = (100, 100), pady = (50,100))
window._frame = fr_menuPrincipal

lb_title = Label(fr_menuPrincipal, text = "Yahtzee", fg = "black", font = "none 30 bold")
lb_title.grid(row = 0, column = 0, pady = (10, 50))

bt_novaPartida = Button(fr_menuPrincipal, text = "Nova Partida", command = lambda: menuPartida.transicao(window))
bt_novaPartida.grid(row = 1, column = 0, pady = (5,5))

bt_novaPartida = Button(fr_menuPrincipal, text = "Continuar")
bt_novaPartida.grid(row = 2, column = 0, pady = (5,5))

bt_novaPartida = Button(fr_menuPrincipal, text = "Ranking")
bt_novaPartida.grid(row = 3, column = 0, pady = (5,5))

window.mainloop()
