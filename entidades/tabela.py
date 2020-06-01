########################################################################
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

__all__ = ['cria_tabela', 'insere_pontuacao', 'registra_desistencia']

def _atualiza_colocacao(conexao, data_horario):
    sqlUpdate = '''
       WITH aux (data_horario, nome_jogador, coloc) as (
          SELECT data_horario, nome_jogador, rank() OVER(
                                            ORDER BY pontuacao_total DESC )
                                            as coloc
          FROM Tabela
          WHERE data_horario = %s)
       UPDATE Tabela, aux
       SET Tabela.colocacao = aux.coloc
       WHERE Tabela.data_horario = aux.data_horario
       AND Tabela.nome_jogador = aux.nome_jogador '''
    
    conexao['cursor'].execute(sqlUpdate, (data_horario,))
    return

def _tabela_jogador_partida_existe(conexao, jogador, data_horario):
    sqlSearch_tabela = ''' SELECT * FROM Tabela
                           WHERE nome_jogador = %s AND data_horario = %s'''
    conexao['cursor'].execute(sqlSearch_tabela,(jogador, data_horario))
    if (conexao['cursor'].rowcount > 0):
        return True
    return False
    

def _tab_pont_jogador_partida_existe(conexao, jogador, data_horario):
    sqlSearch_tab_pont = ''' SELECT * FROM Tabela_Pontuacao
                         WHERE nome_jogador = %s AND data_horario = %s'''
    conexao['cursor'].execute(sqlSearch_tab_pont,(jogador, data_horario))
    if (conexao['cursor'].rowcount > 0):
        return True
    return False

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

    sqlInsert_tab = ''' INSERT INTO Tabela VALUES (%s,%s,%s,%s,%s) '''
    sqlInsert_tab_pont = ''' INSERT INTO Tabela_Pontuacao VALUES (%s,%s,%s,%s) '''

    banco = bd.abre_acesso()

    if _tabela_jogador_partida_existe(banco, nome_jogador, data_horario):
        bd.fecha_acesso(banco)
        return 2

    if _tab_pont_jogador_partida_existe(banco, nome_jogador, data_horario):
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
    sqlSearch_tab_pontuacao = ''' SELECT pontuacao FROM Tabela_Pontuacao
                              WHERE nome_jogador = %s AND data_horario = %s'''
    sqlUpdate_tabela = ''' UPDATE Tabela SET desistencia = True
                           WHERE data_horario = %s AND nome_jogador = %s'''
    sqlUpdate_tab_pontuacao = ''' UPDATE Tabela_Pontuacao SET pontuacao = 0
                           WHERE data_horario = %s AND nome_jogador = %s'''
    
    banco = bd.abre_acesso()
    if not _tabela_jogador_partida_existe(banco, nome_jogador, data_horario)\
       or not _tab_pont_jogador_partida_existe(banco, nome_jogador, data_horario):
        return 1

    banco['cursor'].execute(sqlSearch_tab_pontuacao,(nome_jogador, data_horario))
    tuplas = banco['cursor'].fetchall()
    todas_tuplas_preenchidas = True
    for tupla in tuplas:
        if tupla['pontuacao'] == None:
            todas_tuplas_preenchidas = False
            break
    if todas_tuplas_preenchidas:
        return 2
    
    banco['cursor'].execute(sqlUpdate_tabela,(data_horario, nome_jogador))
    banco['cursor'].execute(sqlUpdate_tab_pontuacao,(data_horario, nome_jogador))
    
    bd.fecha_acesso(banco)
    return 0

################################################################
# Soma uma quantidade de pontos a uma categoria para um jogador.
# nome_jogador: nome do jogador,
# categoria: nome da categoria e  
# pontuacao: quantidade de pontos (Inteiro maior que 0).
# data_horario: data_horario da partida.
# Retorna 0 em caso de sucesso,
# ou retorna 1 se a tabela do jogador na partida não existir
# ou retorna 2 se a categoria não existir
# ou retorna 3 se a quantidade de pontos for negativa
# ou retorna 4 se o jogador já marcou pontos nessa categoria
################################################################

def insere_pontuacao(nome_jogador, data_horario, categoria, pontuacao):
    sqlSearch_Categoria = ''' SELECT nome_categoria FROM Tabela_Pontuacao
                          WHERE nome_categoria = %s'''
    sqlSearch_Pontos = ''' SELECT pontuacao FROM Tabela_Pontuacao
                       WHERE nome_categoria = %s
                       AND nome_jogador = %s AND data_horario = %s'''
    sqlUpdate_tab_pont = ''' UPDATE Tabela_Pontuacao SET pontuacao = %s
                           WHERE data_horario = %s AND nome_jogador = %s
                           AND nome_categoria = %s'''
    sqlUpdate_tabela = ''' UPDATE Tabela SET pontuacao_total = pontuacao_total + %s
                       WHERE data_horario = %s AND nome_jogador = %s'''
    
    if pontuacao < 0:
        return 3
    
    banco = bd.abre_acesso()
    if not _tab_pont_jogador_partida_existe(banco, nome_jogador, data_horario):
        return 1
    banco['cursor'].execute(sqlSearch_Categoria, (categoria,))
    if banco['cursor'].rowcount == 0:
        return 2
    banco['cursor'].execute(sqlSearch_Pontos, (categoria,nome_jogador,data_horario))
    pontuacao_bd = banco['cursor'].fetchone()
    if pontuacao_bd['pontuacao'] is not None:
        return 4
    banco['cursor'].execute(sqlUpdate_tab_pont, (pontuacao, data_horario,
                                               nome_jogador, categoria))
    banco['cursor'].execute(sqlUpdate_tabela, (pontuacao, data_horario,
                                               nome_jogador))
    _atualiza_colocacao(banco, data_horario)
    
    bd.fecha_acesso(banco)
    return 0










