#######################################################################
# MODULO TABELA
#
#  Cria tabelas de pontos com base nas regras de pontuação das categorias
#  Cada tabela armazena quantos pontos cada jogador possui em cada
#  categoria para cada partida.
#
#
#---------------------------v0.1.0: 29/05/2020-------------------------
#  Por: Bruno Coutinho
#  funcao cria_tabela implementada e passando nos testes
#  funcao registra_desistencia implementada p/ condicoes de retorno 1 e 2
#
#---------------------------v0.1.1: 30/05/2020-------------------------
#  Por: Daniel Menezes
#  cria_tabela: verificação de categoria não marcada feita com (== None)
#    já que 0 também é falso em python mas tem significado diferente no
#    contexto.
#
#  mudadas algumas letras dos nomes das relações em maiúsculo para ficar
#    compatível com o nome de criação (deu problemas na execução pra mim)


from entidades import jogador
from entidades import categoria
import funcionalidades.banco_de_dados as bd

__all__ = ['cria_tabela', 'registra_desistencia']

#####################################################################
# Cria e armazena uma nova tabela com pontuação zerada 
# e associada a um jogador e a uma partida.
# nome_jogador: nome do jogador a ser associado à tabela
# data_horario: identificador data_horario da partida a ser associada
# retorna 0 em caso de sucesso
# ou retorna 1 caso não exista um jogador com o nome indicado
# ou retorna 2 caso o jogador já possua uma tabela nessa partida
#####################################################################

def cria_tabela(nome_jogador, data_horario):
    if not jogador.valida_jogador(nome_jogador):
        return 1

    sqlSearch_tab = ''' SELECT * FROM Tabela
    WHERE nome_jogador = %s AND data_horario = %s'''
    sqlSearch_tab_pont = ''' SELECT * FROM Tabela_Pontuacao
    WHERE nome_jogador = %s AND data_horario = %s'''

    sqlInsert_tab = ''' INSERT INTO Tabela VALUES (%s,%s,%s,%s,%s) '''
    sqlInsert_tab_pont = ''' INSERT INTO Tabela_Pontuacao VALUES (%s,%s,%s,%s) '''

    banco = bd.abre_acesso()
    
    banco['cursor'].execute( sqlSearch_tab, (nome_jogador, data_horario) )
    if (banco['cursor'].rowcount > 0): #jogador já registrado
        bd.fecha_acesso(banco)
        return 2
    
    banco['cursor'].execute( sqlSearch_tab_pont, (nome_jogador, data_horario) )
    if (banco['cursor'].rowcount > 0): #jogador já registrado
        bd.fecha_acesso(banco)
        return 2

    pontuacao_total = 0
    colocacao = None
    desistencia = False
    
    banco['cursor'].execute(sqlInsert_tab,
                            (data_horario, nome_jogador, pontuacao_total,
                             colocacao, desistencia))

    categorias = categoria.obtem_nomes()
    for cat in categorias:
        nome_categoria = cat['nome']
        pontuacao = None
        banco['cursor'].execute(sqlInsert_tab_pont,
                            (data_horario, nome_jogador, nome_categoria,
                             pontuacao))
    
    bd.fecha_acesso(banco)
    return 0

############################################################################
# Zera todos os pontos de todas as categorias ainda não pontuadas na tabela
#de um jogador para a partida data_horario e marca desistência na informação
#da tabela.
# nome_jogador: nome do jogador.
# data_horario:  data_horario da partida.
# retorna 0 em caso de sucesso
# ou retorna 1 se a tabela do jogador na partida não existir
# ou retorna 2 se o jogador já pontuou em todas as categorias
############################################################################

def registra_desistencia(nome_jogador, data_horario):
    sqlSearch_tabela = ''' SELECT * FROM Tabela
                           WHERE nome_jogador = %s AND data_horario = %s'''
    sqlSearch_tab_pontuacao = ''' SELECT pontuacao FROM Tabela_Pontuacao
                              WHERE nome_jogador = %s AND data_horario = %s'''
    
    banco = bd.abre_acesso()
    banco['cursor'].execute(sqlSearch_tabela,(nome_jogador, data_horario))
    if (banco['cursor'].rowcount == 0):
        return 1

    banco['cursor'].execute(sqlSearch_tab_pontuacao,(nome_jogador, data_horario))
    tuplas = banco['cursor'].fetchall()
    todas_tuplas_preenchidas = True
    for tupla in tuplas:
        if tupla['pontuacao'] == None:
            todas_tuplas_preenchidas = False
    if todas_tuplas_preenchidas:
        return 2
    #falta zerar as categorias nao pontuadas
    return 0
