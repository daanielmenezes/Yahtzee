#####################################################################
# MODULO JOGADOR
#
#  Gerencia e provê dados dos jogadores
#
#-------------------------v0.1.0: 20/05/2000-------------------------
#  Por: Daniel Menezes
#  Criadas as funções(funcionando e passando nos testes):
#   -insere
#   -valida_jogador
#####################################################################

from datetime import datetime 
import funcionalidades.banco_de_dados as bd

__all__ = [ 'insere' , 'valida_jogador']


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
    ranking = banco['cursor'].rowcount + 1  #num de jogadores + 1
    pontuacao = recorde = 0

    banco['cursor'].execute(sqlInsert,
                            (nome, data, pontuacao, recorde, ranking))
    bd.fecha_acesso(banco)
    return 0

################################################
# Verifica se um jogador está registrado.
# nome: nome do jogador a buscar.
# Retorna False caso o jogador esteja registrado
# ou retorna True caso não esteja.
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

