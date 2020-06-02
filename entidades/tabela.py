########################################################################
# MODULO TABELA
#
#  Responsável por manipular as cartelas dos jogadores, armazenando
#  as informações referentes a sua pontuação e a sua participação
#  em cada partida. Implementada com duas relações no banco
#  de dados: Tabela, que armazena a pontuação total, colocação e
#  desistência (booleano) dos jogadores para cada partida, e
#  Tabela_Pontuacao, que armazena a pontuação correspondente a cada
#  categoria dos jogadores nas partidas. Essas duas relações já estão
#  criadas separadamente.
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
#
#---------------------------v0.2.0: 31/05/2020-------------------------
#  Por: Bruno Coutinho
#
#  funções remove e insere_pontuacao implementadas, pequenos erros corrigidos
#  e registra_desistencia completada
#
#---------------------------v1.0.0: 01/06/2020-------------------------
#  Por: Bruno Coutinho
#
#  função obtem_tabelas implementada com sucesso, todas as funções passando
#  nos testes
#
#---------------------------v1.0.1: 02/06/2020-------------------------
#  Por: Bruno Coutinho
#
#  código mais organizado e documentado, modificação de algumas descrições
#  de funções


from entidades import jogador
from entidades import categoria
import funcionalidades.banco_de_dados as bd

__all__ = ['cria_tabela', 'insere_pontuacao', 'registra_desistencia', 'remove',
           'obtem_tabelas']


########################### funções auxiliares ###############################

## função auxiliar à função de acesso insere_pontuacao:

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

## função auxiliar para ver se as informações do jogador na partida
## especificada já estão na relação Tabela do banco de dados

def _tabela_jogador_partida_existe(conexao, jogador, data_horario):
    sqlSearch_tabela = ''' SELECT * FROM Tabela
                           WHERE nome_jogador = %s AND data_horario = %s'''
    conexao['cursor'].execute(sqlSearch_tabela,(jogador, data_horario))
    if (conexao['cursor'].rowcount > 0):
        return True
    return False
    
## função auxiliar para ver se as informações do jogador na partida
## especificada já estão na relação Tabela_Pontuacao do banco de dados

def _tab_pont_jogador_partida_existe(conexao, jogador, data_horario):
    sqlSearch_tab_pont = ''' SELECT * FROM Tabela_Pontuacao
                         WHERE nome_jogador = %s AND data_horario = %s'''
    conexao['cursor'].execute(sqlSearch_tab_pont,(jogador, data_horario))
    if (conexao['cursor'].rowcount > 0):
        return True
    return False

## funções auxiliares à função de acesso obtem_tabelas:

def sql_aux_obtem_data_horario(data_horarios):
    sqlAux = """(SELECT data_horario
                        FROM Tabela
                        WHERE data_horario = '""" + str(data_horarios[0]) + "'"
    
    for data in data_horarios[1:]:
        sqlAux += " OR data_horario = " + "'" + data + "'"
    sqlAux +=")"
    return sqlAux

def sql_aux_obtem_nome(nomes):
    sqlAux = """(SELECT nome_jogador
                           FROM Tabela
                           WHERE nome_jogador = '""" + nomes[0] + "'"
    
    for nome in nomes[1:]:
        sqlAux += " OR nome_jogador = " + "'" + nome + "'"
    sqlAux +=")"
    return sqlAux

def obtem_tab_ambas_vazias(conexao):
    sqlSearch = '''
                SELECT *
                FROM Tabela
                '''
    conexao['cursor'].execute(sqlSearch)
    return conexao['cursor'].fetchall()

def obtem_tab_nomes_vazia(conexao, data_horarios):
    sqlSearch_Tabela = '''
                       SELECT *
                       FROM Tabela
                       WHERE data_horario IN %s
                       '''
    sqlAux = sql_aux_obtem_data_horario(data_horarios)
    
    sqlSearch_Tabela = sqlSearch_Tabela % (sqlAux)
    conexao['cursor'].execute(sqlSearch_Tabela)
    return conexao['cursor'].fetchall()

def obtem_tab_datas_vazia(conexao, nomes):
    sqlSearch_Tabela = '''
                       SELECT *
                       FROM Tabela
                       WHERE nome_jogador IN %s
                       '''
    sqlAux = sql_aux_obtem_nome(nomes)
    
    sqlSearch_Tabela = sqlSearch_Tabela % (sqlAux)
    conexao['cursor'].execute(sqlSearch_Tabela)
    return conexao['cursor'].fetchall()

def obtem_tab_nenhuma_vazia(conexao, nomes, data_horarios):
    sqlSearch_Tabela = '''
                       SELECT *
                       FROM Tabela
                       WHERE data_horario IN %s
                       AND nome_jogador IN %s
                       '''
    
    sqlAux_nome = sql_aux_obtem_nome(nomes)
    sqlAux_data = sql_aux_obtem_data_horario(data_horarios)
    sqlSearch_Tabela = sqlSearch_Tabela % (sqlAux_data, sqlAux_nome)
    conexao['cursor'].execute(sqlSearch_Tabela)
    return conexao['cursor'].fetchall()


####################### funções de acesso ###########################


#####################################################################
# Cria e armazena uma nova tabela(cartela) com pontuação zerada 
# e associada a um jogador e a uma partida. Nessa implementação com
# banco de dados, inserimos nas relações Tabela e Tabela_Pontuacao
# tuplas correspondentes ao jogador e partida informados, com pontuacao
# zerada.
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
# de um jogador para a partida data_horario e marca desistência na informação
# da tabela.
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
# Soma uma quantidade de pontos a uma categoria para um jogador
# e atualiza sua pontuação total e colocação na partida.
# nome_jogador: nome do jogador,
# categoria: nome da categoria  
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

############################################################
# Remove a tabela de um jogador em uma partida
# nome_jogador: nome do jogador a buscar.
# data_horario: partida a buscar.
# retorna 0 em caso de sucesso
# ou retorna 1 se a tabela do jogador na partida não existir
############################################################

def remove(nome_jogador, data_horario):
    sqlDelete_tab_pont = ''' DELETE FROM Tabela_Pontuacao
                         WHERE data_horario = %s AND nome_jogador = %s'''
    sqlDelete_tabela = ''' DELETE FROM Tabela
                         WHERE data_horario = %s AND nome_jogador = %s'''
    
    banco = bd.abre_acesso()
    if not _tabela_jogador_partida_existe(banco, nome_jogador, data_horario)\
       or not _tab_pont_jogador_partida_existe(banco, nome_jogador, data_horario):
        return 1
    
    banco['cursor'].execute(sqlDelete_tab_pont, (data_horario, nome_jogador))
    banco['cursor'].execute(sqlDelete_tabela, (data_horario, nome_jogador))

    bd.fecha_acesso(banco)
    return 0

##############################################################################
# Gera informações sobre todos os jogadores de nomes nas partidas 
# data_horarios
# nomes:lista de nomes dos jogadores a filtrar. Caso vazia, considera-se todos
# os jogadores que possuem uma tabela.
# data_horarios: lista com data_horario de cada partida a ser filtrada. Caso 
# vazia, considera-se todas as partidas que possuem tabela.
# retorna, em caso de sucesso, uma lista de dicionários do tipo:
# {“nome_jogador”, 
#  ”data_horario”, 
#  “pontos_por_categoria”,
#  “pontuacao_total”, 
#  “colocacao”,
#  “desistencia”
# }
#
# “pontos_por_categoria” : lista de dicionários com a pontuação do jogador na
# partida em cada categoria da forma:
# [ { “nome”: <nome_da_categoria1>, “pontuacao”: <pontuacao_na_categoria_1> },
#   { “nome”: <nome_da_categoria2>, “pontuacao”: <pontuacao_na_categoria_2> },
#   { “nome”: <nome_da_categoria3>, “pontuacao”: <pontuacao_na_categoria_3> }
#  ... ]
#  As categorias ainda não pontuadas terão <pontuacao_na_categoria> = None.
#
# ou retorna 1 se nenhum dos nomes ou data_horarios fornecidos foram encontrados
#
################################################################################
    
def obtem_tabelas(nomes, data_horarios):
    banco = bd.abre_acesso()
    
    if nomes == [] and data_horarios == []:
        tuplas_tabela = obtem_tab_ambas_vazias(banco)
    elif nomes == []:
        tuplas_tabela = obtem_tab_nomes_vazia(banco, data_horarios)
        if tuplas_tabela == []:
            return 1
    elif data_horarios == []:
        tuplas_tabela = obtem_tab_datas_vazia(banco, nomes)
        if tuplas_tabela == []:
            return 1
    else:
        tuplas_tabela = obtem_tab_nenhuma_vazia(banco, nomes, data_horarios)
        if tuplas_tabela == []:
            return 1

    sqlSearch_tab_pont = ''' SELECT nome_categoria as nome, pontuacao
                         FROM Tabela_Pontuacao
                         WHERE data_horario = %s
                         AND nome_jogador = %s'''
    
    for elemento in tuplas_tabela:
        banco['cursor'].execute(
            sqlSearch_tab_pont, (elemento['data_horario'],
                                 elemento['nome_jogador']))
        lista_pontos_categoria = banco['cursor'].fetchall()
        elemento['pontos_por_categoria'] = lista_pontos_categoria
                 
    bd.fecha_acesso(banco)
    return tuplas_tabela
