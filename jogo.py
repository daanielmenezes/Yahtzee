from tkinter import *
from gui.menu_principal import transicao as tr_menuPrincipal

window = Tk()
window.title("Yahtzee")
window._frame=None
tr_menuPrincipal(window)

window.mainloop()
