from tkinter import *
from tkinter import filedialog
import os

from entidades import partida, categoria, tabela
from . import menu_principal

__all__ = ['transicao']


info = None
img_dados =[]
bt_dados = []
bt_pontuacoes = {}
lb_turno = None
lb_lancamentos_rest = None
tk_window = None
save_criado = False

def transicao_tela_final( window ):
    def obtem_pontuacao_categoria(lista_categoria, nome_categoria):
        for categoria in lista_categoria:
            if categoria['nome'] == nome_categoria:
                return categoria['pontuacao']

    if window._frame:
        window._frame.destroy()

    fr_tela_final = Frame( window )
    fr_tela_final.pack()

    window._frame = fr_tela_final

    Label( fr_tela_final, text="PARTIDA ENCERRADA", font=('Helvetica', 20)).pack()

    fr_cartelas = Frame( fr_tela_final )
    fr_cartelas.pack()

    Button( fr_tela_final, text="Voltar ao Menu Principal",
            command = lambda: menu_principal.transicao(window) ).pack( padx=10, pady=10)

    cartelas = tabela.obtem_tabelas( [], [info['data_horario']] )
    
    # ordena as cartelas em relação a colocacao
    cartelas.sort( key = lambda tabela_jogador: tabela_jogador['colocacao'])
    for cartela_jogador in cartelas:
        fr_cartela_container = Frame( fr_cartelas )
        fr_cartela_container.pack( side='left', padx=10, pady=10 )

        Label( fr_cartela_container, text=cartela_jogador['nome_jogador'] ).pack()
        Label( fr_cartela_container, text=str(cartela_jogador['colocacao'])+"º Lugar" ).pack(side='bottom')

        fr_cartela = Frame( fr_cartela_container, bd=1, relief=SOLID )
        fr_cartela.pack( side='left', padx=10, pady=10 )
        Label( fr_cartela, text = "Categoria", bd=1, relief=SOLID, height=1, bg = 'light grey').grid(row=0, column = 0, sticky='news', ipadx=1, ipady=2)
        Label( fr_cartela, text = "Pontuação", bd=1, relief=SOLID, height=1, bg = 'light grey').grid(row=0, column = 1, sticky='news', ipadx=1, ipady=2)

        for i, dict_categoria in enumerate(categoria.obtem_nomes()):
            pts = obtem_pontuacao_categoria( cartela_jogador['pontos_por_categoria'], dict_categoria['nome'])
            Label( fr_cartela, text=dict_categoria['nome'], bd=1, relief=SOLID, height=1).grid(row=i+1, column=0, sticky='news', ipadx=1)
            Label( fr_cartela, text=str(pts), bd=1, relief=SOLID ).grid( row=i+1, column=1, sticky='news', ipady=2 )
        last_row = len(cartela_jogador['pontos_por_categoria'])
        Label( fr_cartela, text="Total", bd=1, relief=SOLID, height=1).grid(row=last_row + 1, column=0, sticky='news', ipadx=1)
        Label( fr_cartela, text=cartela_jogador['pontuacao_total'], bd=1, relief=SOLID ).grid( row=last_row+1, column=1, sticky='news', ipady=2 )
        

def atualiza_info():
    global info

    info = partida.obtem_info_partida()    

    # atualiza turno e jogador
    lb_turno.config(text = "Jogada {} - {}".format(info['turno'], info['jogador_da_vez']))
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

    # detecta fim de jogo
    if info['status'] == 'encerrada':
        transicao_tela_final(tk_window)

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
        bt_pontuacoes[dict_categoria['nome']] = Button( fr_cartela, text="", bd=1, relief=SOLID, cursor="hand2",
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
    
    Label(fr_lancamento, text="Combinação atual:").pack()
    
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
                              command = lambda i=i: seleciona_dado(i), cursor='hand2'))
        bt_dados[i].pack(padx=5, pady=5)

    bt_rolar = Button(fr_lancamento, text="Rolar", command = faz_lancamento)
    bt_rolar.pack(padx = 5, pady=5)

def cria_frame_rodape( parent, root ):
    def salva_partida():
        global save_criado
        if save_criado:
            try:
                arquivo = open(save_criado,"w")
            except:
                messagebox.showerror("Erro","Erro de escrita.")
                return

        else:
            arquivo = filedialog.asksaveasfile(mode="w", defaultextension="xml",
                                                title="Escolha um nome e local para salvar.",
                                                initialdir="saves/", initialfile="Novo Save",
                                                filetypes=(("arquivos xml", "*.xml"),))
            if arquivo == None:
                messagebox.showinfo("Info","Nenhum arquivo selecionado.")
                return
            save_criado = arquivo.name
        cond_ret = partida.salva_partida(arquivo)
        if cond_ret == 1:
            messagebox.showerror("Erro","Não há partida em andamento.")
        elif cond_ret==2:
            messagebox.showerror("Erro","Erro de escrita.")
        elif cond_ret == 0:
            messagebox.showinfo("Sucesso","Partida salva com sucesso!")
    
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
    if info and info['tentativas'] <3:
        Label( fr_partida, text = "Escolha dados a serem mantidos para próximo lançamento", font=('Helvetica', 9)).pack(anchor = 'w',padx = 10, pady = (50,0))
    
    cria_frame_rodape( fr_partida, window )

    cria_frame_lancamento(fr_partida)

    cria_frame_cartela( fr_partida )

    global tk_window
    tk_window = window
    window._frame = fr_partida
    atualiza_info()
