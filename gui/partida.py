from tkinter import *
import os

from entidades import partida, categoria, tabela
from . import menu_principal


info = None
img_dados =[]
bt_dados = []
bt_pontuacoes = {}
lb_turno = None
lb_lancamentos_rest = None
tk_window = None

def atualiza_info():
    global info
    info = partida.obtem_info_partida()

    # atualiza turno e jogador
    lb_turno.config(text = "Turno {} - {}".format(info['turno'], info['jogador_da_vez']))
    lb_lancamentos_rest.config(text="Lançamentos restantes: {}".format(info['tentativas']))
    # atualiza lancamento
    if info['tentativas'] == 3:
        for botao in bt_dados:
            botao.config(image=img_dados[0], bg='white', relief=FLAT)
    elif info['combinacao']:
        for idx, botao in enumerate(bt_dados):
            botao.config(image=img_dados[info['combinacao'][idx]])
            if info['tentativas'] == 0:
                botao.config(relief=FLAT, bg='slate gray')


    # atualiza as pontuacoes marcadas na cartela
    pts_tabela = tabela.obtem_tabelas([info['jogador_da_vez']], [info['data_horario']])[0]['pontos_por_categoria']
    for categoria_tabela in pts_tabela:
        pts = str(categoria_tabela['pontuacao'])
        if pts == 'None':
            bt_pontuacoes[categoria_tabela['nome']].config(text="", bg="white")
        else:
            bt_pontuacoes[categoria_tabela['nome']].config(text=pts, bg="slate gray", fg="black")
    
    # atualiza pontuacoes possiveis na cartela
    if info['tentativas'] != 3:
        for categoria_combinacao in info['pts_combinacao']:
            if bt_pontuacoes[categoria_combinacao['nome']].cget('bg') == "white":
                pts = str(categoria_combinacao['pontuacao'])
                bt_pontuacoes[categoria_combinacao['nome']].config(text=pts, bg="white", fg="green")


def cria_frame_cartela( parent ):
    def marca_categoria( nome_categoria ):
        codigo_retorno = partida.marca_pontuacao( nome_categoria )

        if codigo_retorno == 1:
            messagebox.showerror("Erro","Não há partida em andamento.")
        elif codigo_retorno == 2:
            messagebox.showerror("Erro","Categoria selecionada é inválida.")
        elif codigo_retorno == 3:
            messagebox.showinfo("Info","Faça um lançamento antes de marcar.")
        elif codigo_retorno == 4:
            messagebox.showinfo("Info","Categoria já marcada.")
        elif codigo_retorno == 0:
            atualiza_info()

    fr_cartela = Frame( parent, bd=1, relief=SOLID )
    fr_cartela.pack(padx=100, pady=10, side="right")

    lb_categoria = Label( fr_cartela, text = "Categoria", bg = 'light grey', bd=1, relief = SOLID)
    lb_categoria.grid(row = 0, column=0, sticky='news', ipady=1)

    lb_pontuacao = Label( fr_cartela, text = "Pontuação", bg = 'light grey', bd=1, relief = SOLID )
    lb_pontuacao.grid( row = 0, column =1, sticky='news',ipady=1)

    for i, dict_categoria in enumerate(categoria.obtem_nomes()):
        Label( fr_cartela, text=dict_categoria['nome'], bd=1, relief=SOLID, height=1).grid(row=i+1, column=0, sticky='news', ipadx=1)
        bt_pontuacoes[dict_categoria['nome']] = Button( fr_cartela, text="", bd=1, relief=SOLID,
                                                      command = lambda nome_cat = dict_categoria['nome']: marca_categoria(nome_cat) )
        bt_pontuacoes[dict_categoria['nome']].grid( row=i+1, column=1, sticky='news', ipady=2 )


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

    fr_lancamento_out= Frame(parent)
    fr_lancamento_out.pack(side = 'left', padx=100, pady=10)
    fr_lancamento = Frame( fr_lancamento_out, bd =1, relief=SOLID )
    fr_lancamento.pack(  )
    
    Label(fr_lancamento, text="Combinacao atual:").pack()
    
    global lb_lancamentos_rest
    lb_lancamentos_rest = Label(fr_lancamento_out)
    lb_lancamentos_rest.pack()


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

def cria_frame_rodape( parent, root ):
    def salva_partida():
        basedir = os.getcwd()
        cond_ret = partida.salva_partida(os.path.join(basedir, 'saves'))
        if cond_ret == 1:
            messagebox.showerror("Erro","Não há partida em andamento.")
        elif cond_ret==2:
            messagebox.showerror("Erro","Pasta 'saves' não foi encontrada.")
        elif cond_ret==3:
            messagebox.showerror("Erro","Erro de escrita.")
        elif cond_ret == 0:
            messagebox.showinfo("Sucesso","Partida salva na pasta Yahtzee/saves/.")
    
    def voltar_menu():
        if not info['salva']:
            answer = messagebox.askyesnocancel("Aviso", "Há alterações não salvas. Deseja salvar?")
            if answer:
                salva_partida()
            elif answer==None:
                return
        partida.para_partida()
        menu_principal.transicao(root)


    fr_rodape = Frame(parent)
    fr_rodape.pack(side="bottom")

    Button(fr_rodape,text='Salvar Partida', command=salva_partida).pack(side='left', padx = 10, pady=10)
    Button(fr_rodape, text='Voltar ao menu', command=voltar_menu).pack(padx=10,pady=10)


def transicao( window ):
    if window._frame:
        window._frame.destroy()

    window.config(cursor = 'arrow')

    fr_partida = Frame(window)
    fr_partida.pack(expand=True)

    global lb_turno
    lb_turno = Label( fr_partida, font = ('Helvetica', 20))
    lb_turno.pack()

    Label( fr_partida, text = "Lance os dados e escolha uma categoria para pontuar", font=('Helvetica', 16)).pack()
    
    cria_frame_rodape( fr_partida, window )

    cria_frame_lancamento(fr_partida)

    cria_frame_cartela( fr_partida )

    global tk_window
    tk_window = window
    window._frame = fr_partida
    atualiza_info()