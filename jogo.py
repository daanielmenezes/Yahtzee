from tkinter import *
from tkinter import messagebox
import configparser
from os.path import join
import sys
import threading

from gui.menu_principal import transicao as tr_menuPrincipal
from funcionalidades.banco_de_dados import configura

class StdoutRedirector(object):
    def __init__(self,text_widget):
        self.text_space = text_widget

    def write(self,string):
        self.text_space.insert('end', string)
        self.text_space.see('end')

def thread_cria_bd():
    lb_criando = Label(window, text="Criando Banco de Dados...", font=("Helvetica",20))
    lb_criando.grid(column=0, row=0,padx=20, pady=20)
    window.config(cursor="watch")
    text_box = Text(window, wrap='word', height = 11, width=50)
    text_box.grid(column=0, row=1, columnspan = 2, sticky='NSWE', padx=5, pady=5)
    sys.stdout = StdoutRedirector(text_box)
    window.update()

    condret = configura()
    if condret == 0:
        messagebox.showinfo("Info","Banco de dados e tabelas criados com sucesso")
        config['BD']['CriarTabelasAoIniciar'] = 'nao'
        with open(join("config", "config.ini"),"w") as configfile:
            config.write(configfile)
        window.config(cursor="watch")
        lb_criando.destroy()
        text_box.destroy()
        sys.stdout = sys.__stdout__
        window._frame=None
        window.config(cursor="arrow")
        tr_menuPrincipal(window)
    else:
        messagebox.showerror("Erro","Não foi possível criar o banco de dados: "+condret + "Tente rodar a aplicação novamente.")
        sys.exit()

window = Tk()
window.title("Yahtzee")
window.iconbitmap("gui/assets/icon.ico")
window.resizable(width=False, height=False)

config = configparser.ConfigParser()
config.optionxform = str
try:
    config.read(join("config", "config.ini"))
    criarTabelas = config['BD']['CriarTabelasAoIniciar']
except:
    messagebox.showerror("Erro","Erro de leitura do arquivo de configuração.")
    sys.exit()

if criarTabelas == 'sim':
    threading.Thread(target=thread_cria_bd).start()
else:
    window._frame=None
    tr_menuPrincipal(window)

window.mainloop()
