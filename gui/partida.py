from entidades import partida
from tkinter import *

info = None
img_dados =[]
bt_dados = []

def atualiza_info():
    global info
    info = partida.obtem_info_partida()

    # quando a partica começa combinacao é None
    if info['combinacao']:
        for idx, botao in enumerate(bt_dados):
            botao.config(image=img_dados[info['combinacao'][idx]])


def cria_frame_lancamento( parent ):
    def seleciona_dado(idx):
        if info['tentativas'] in range(1,3):
            if bt_dados[idx].cget('relief') == 'flat':
                bt_dados[idx].config(relief=SUNKEN, background='lime')
            else:
                bt_dados[idx].config(relief=FLAT, background='white')
        elif info['tentativas'] == 3:
            messagebox.showinfo("Info","Não é possível selecionar dados antes de fazer um lançamento na sua rodada.")
        elif info['tentativas'] == 0:
            messagebox.showinfo("Info","Acabaram as suas tentativas. Marque uma pontuação.")

    def faz_lancamento():
        dados_a_manter = [idx for idx, botao in enumerate(bt_dados)\
                         if botao.cget('relief') == 'sunken']
        codigo_retorno = partida.faz_lancamento(dados_a_manter)
        if codigo_retorno == 1:
            messagebox.showerror("Erro","Não há partida em andamento.")
        elif codigo_retorno == 2:
            messagebox.showerror("Erro","Dado inválido escolhido.")
        elif codigo_retorno == 3:
            messagebox.showerror("Erro","Dado selecionado no primeiro lançamento.")
        elif codigo_retorno == 4:
            messagebox.showinfo("Info","Acabaram as suas tentativas. Marque uma pontuação.")
        elif codigo_retorno == 0:
            atualiza_info()

    fr_lancamento = Frame( parent, bd =1, relief=SOLID )
    fr_lancamento.pack( side = 'left', padx=10, pady=10 )
    
    img_dados.append(PhotoImage(file = "gui/assets/diceZero.gif"))
    img_dados.append(PhotoImage(file = "gui/assets/diceOne.gif"))
    img_dados.append(PhotoImage(file = "gui/assets/diceTwo.gif"))
    img_dados.append(PhotoImage(file = "gui/assets/diceThree.gif"))
    img_dados.append(PhotoImage(file = "gui/assets/diceFour.gif"))
    img_dados.append(PhotoImage(file = "gui/assets/diceFive.gif"))
    img_dados.append(PhotoImage(file = "gui/assets/diceSix.gif"))

    for i in range(5):
        bt_dados.append(Button(fr_lancamento, image = img_dados[0], relief=FLAT,
                              command = lambda i=i: seleciona_dado(i)))
        bt_dados[i].pack(padx=5, pady=5)

    bt_rolar = Button(fr_lancamento, text="Rolar", command = faz_lancamento)
    bt_rolar.pack(padx = 5, pady=5)

def transicao( window ):
    if window._frame:
        window._frame.destroy()

    window.config(cursor = 'arrow')

    fr_partida = Frame(window)
    fr_partida.pack(expand=True)

    cria_frame_lancamento(fr_partida)

    jogadores = partida.obtem_info_partida()['jogadores']
    for jogador in jogadores:
        Label(fr_partida, text = jogador).pack( side = 'left')

    atualiza_info()