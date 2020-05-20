#####################################################################
# MODULO JOGADOR
#
#  Gerencia e provê dados dos jogadores
#
#-------------------------v0.1.0: 20/05/2020-------------------------
#  Por: Daniel Menezes
#  Criadas as funções(funcionando e passando nos testes):
#   -insere
#   -valida_jogador
#
#-------------------------v1.0.0: 20/05/2020-------------------------
#  Por: Daniel Menezes
#  Criadas as funções(funcionando e passando nos testes):
#   -remove
#   -obtem_info
#   -atualiza_info
#   -valida_jogador
#  
#####################################################################

from datetime import datetime 
import funcionalidades.banco_de_dados as bd

__all__ = [ 'insere' , 'valida_jogador', 'remove', 'obtem_info',
            'atualiza_info', 'valida_jogador' ]


def _atualiza_rank(conexao):
    sqlAtualizaRank = """
        with aux (nome, ordem) as (
            select nome, rank() over (
                        order by pontuacao_total desc, recorde desc )
                        as ordem from Jogador
            )
        update Jogador, aux 
        set Jogador.ranking = aux.ordem
        where Jogador.nome = aux.nome
    """
    conexao['cursor'].execute(sqlAtualizaRank)
    return


######################################
#  Cria um novo jogador.
#  Recebe o nome do novo jogador.
#  Retorna 0 em caso de sucesso
#   ou retorna 1 se o nome for nulo
#   ou retorna 2 se o nome já existir.
######################################
def insere(nome):
    if not nome: #nome nulo
        return 1 

    sqlSearch = " SELECT nome FROM Jogador WHERE nome = %s"
    sqlInsert = "INSERT INTO Jogador VALUES (%s, %s, %s, %s, %s)"

    banco = bd.abre_acesso()

    banco['cursor'].execute( sqlSearch, (nome,) ) 
    if (banco['cursor'].rowcount > 0):      #nome já registrado
        bd.fecha_acesso(banco)
        return 2

    banco['cursor'].execute("select nome from Jogador")
    data = datetime.now().date()            #data de hoje
    ranking = None
    pontuacao = recorde = 0

    banco['cursor'].execute(sqlInsert,
                            (nome, data, pontuacao, recorde, ranking))
    bd.fecha_acesso(banco)
    return 0


################################################
#  Verifica se um jogador está registrado.
#  nome: nome do jogador a buscar.
#  Retorna False caso o jogador esteja registrado
#  ou retorna True caso não esteja.
################################################
def valida_jogador(nome):
    sqlBusca = """ SELECT nome 
                   FROM Jogador
                   WHERE nome = %s """
    banco = bd.abre_acesso()
    banco['cursor'].execute(sqlBusca, (nome,))
    encontrado = banco['cursor'].rowcount == 1
    bd.fecha_acesso(banco)
    return encontrado


########################################
#  Remove um jogador sem afetar os outros.
#  Recebe o nome do jogador.
#  Retorna 0 em caso de sucesso
#   ou retorna 1 caso o nome seja inválido
########################################
def remove(nome):
    sqlRemove = """ DELETE
                    FROM Jogador
                    WHERE nome = %s """

    banco = bd.abre_acesso()
    banco['cursor'].execute(sqlRemove, (nome,))

    retorno = 1 if banco['cursor'].rowcount == 0 else 0 

    _atualiza_rank(banco)
    bd.fecha_acesso(banco)
    return retorno


########################################################################
#  Gera uma lista de dicionários contendo informações básicas sobre cada
#  jogador
#  Recebe uma lista de nomes para filtrar jogadores desejados ou
#  Recebe uma lista vazia para retornar todos os jogadores registrados.
#  Retorna, em caso de sucesso, uma lista de dicionários do tipo:
#  { 
#    “nome”,
#    “pontuacao_total” ,
#    “data_criacao” ,
#    “recorde”,
#    “posicao_ranking”
#  }  
#  ou retorna uma lista vazia se nenhum nome recebido for encontrado
########################################################################
def obtem_info(nomes):
    if not nomes:
        retorno = []
    else:
        sqlBusca = """ SELECT *
                       FROM Jogador
                       WHERE nome = %s """

        for i in range(len(nomes) - 1):
            sqlBusca += "OR nome = %s"

        banco = bd.abre_acesso()
        banco['cursor'].execute(sqlBusca, tuple(nomes))
        retorno = [dictJogador for dictJogador in banco['cursor']]
        bd.fecha_acesso(banco)

    return retorno


######################################################################
#  Atualiza a pontuação total, ranking e recorde do jogador após obter
#  “ultima_pontuacao” novos pontos.
#
#  nome: nome do jogador.
#  ultima_pontuacao: número de pontos novos obtidos.
#
#  retorna 0 em caso de sucesso
#  ou retorna 1 caso não haja um jogador de nome “nome” registrado.
#  ou retorna 2 caso “ultima_pontuacao” seja negativa
######################################################################
def atualiza_info(nome, ultima_pontuacao):
    if ultima_pontuacao < 0:
        retorno = 2
    else:
        sqlAtualizaPts = """
            UPDATE Jogador
            SET pontuacao_total = pontuacao_total + %s
            WHERE nome = %s
        """

        sqlAtualizaRecorde = """
            UPDATE Jogador
            SET recorde = %s
            WHERE nome = %s
            AND recorde < %s
        """

        banco = bd.abre_acesso()
        banco['cursor'].execute( sqlAtualizaPts, (ultima_pontuacao, nome) )
        if banco['cursor'].rowcount == 1 :
            banco['cursor'].execute( sqlAtualizaRecorde,
                                        (ultima_pontuacao,
                                        nome,
                                        ultima_pontuacao ) )
            _atualiza_rank(banco)
            retorno = 0
        else:
            retorno = 1

        bd.fecha_acesso(banco)

    return retorno
