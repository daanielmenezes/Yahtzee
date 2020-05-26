#####################################################################
# MODULO PARTIDA
#
#  Centraliza as ações relacionadas ao andamento de uma partida
#  fazendo a comunicação entre os diversos módulos envolvidos. Cada 
#  partida possui um atributo identificador “data_horario”, trata-se 
#  do tipo datetime do python, indicando a data e horário em que foi 
#  criada. Uma partida pode ter status “andamento”, “pausada” ou 
#  “encerrada”.
#
#  Responsável por gerar combinações de 5 dados e a sua avaliação
#  em pontos em cada categoria.
#
#--------------v0.1.0: 25/05/0020--------------------
#  Por: Daniel Menezes
#  Criado mocking para tabela.cria_tabela
#  Implementada inicia_partida passando nos testes
#
#####################################################################

from datetime import datetime
from entidades import jogador
from entidades import tabela
from funcionalidades import banco_de_dados
from funcionalidades import combinacao

from unittest import mock

__all__ = ['inicia_partida',]


partida_atual = {}

#MOCKS:
tabela = mock.Mock()
tabela.cria_tabela.side_effect = [0, 0, 0, 1]



#################################################################
# Cria uma nova partida e associa tabelas para os seus jogadores.
# nomes: lista de nomes dos jogadores participantes.
#
# retorna data_horario da partida criada em caso de sucesso
# ou retorna 1 caso um dos jogadores passados não exista.
#################################################################
def inicia_partida(nomes):
    data_horario = datetime.now()

    for jogador in nomes:
        cod_retorno = tabela.cria_tabela(jogador, data_horario) 
        if cod_retorno == 1:
            #jogador nao existe
            for jogador_a_remover in nomes:
                if jogador == jogador_a_remover:
                    break
                tabela.remove(jogador, data_horario)
            return 1

    banco = banco_de_dados.abre_acesso()
    sql_partida = """INSERT Partida VALUES (%s, %s)"""

    banco['cursor'].execute(sql_partida, (data_horario, 'andamento'))

    banco_de_dados.fecha_acesso(banco)

    partida_atual['data_horario'] = data_horario
    partida_atual['combinacao_atual'] = [6,6,6,6,6]
    partida_atual['turno_atual'] = 0
    partida_atual['tentativas'] = 0
    partida_atual['jogadores'] = nomes
    partida_atual['jogador_da_vez'] = nomes[0]
    partida_atual['status'] = 'andamento'

    return data_horario 

##########################################################################
# Gera um novo lançamento para o jogador do turno
# data_horario: identificador da partida
# dados_escolhidos: lista com os índices (inteiros no intervalo [0,4])
#  dos dados a terem seus valores mantidos
#  ou lista vazia para rolar todos os dados
# Retorna 0 em caso de sucesso
#  ou retorna 1 caso a partida informada não exista
#  ou retorna 2 caso a partida esteja pausada
#  ou retorna 3 caso a partida esteja encerrada
#  ou retorna 4 caso um dos índices em dados_escolhidos não seja válido
#  ou retorna 5 caso dados_escolhidos não seja uma lista vazia no primeiro
#  lançamento do turno atual.
##########################################################################
#def faz_lancamento(data_horario, dados_escolhidos):
#    return
#
######################################################################
## Atribui ao jogador do turno os pontos do seu último lançamento (do 
##  mesmo turno) na categoria escolhida e passa para o próximo turno.
## categoria: nome da categoria escolhida
## Retorna 0 em caso de sucesso
##  ou retorna 1 caso a partida informada não exista
##  ou retorna 2 caso a partida esteja pausada
##  ou retorna 3 caso a partida esteja encerrada
##  ou retorna 4 caso nome_categoria seja inválido
##  ou retorna 5 caso o jogador do turno ainda não tenha realizado
##  um lançamento no turno atual.
##  ou retorna 6 caso o jogador já tenha marcado pontos
##  na categoria escolhida nessa partida
######################################################################
#def marca_pontuacao(data_horario, categoria):
#    return
#
## Pausa uma partida em andamento.
## data_horario: identificador da partida.
## retorna 0 em caso de sucesso
## ou retorna 1 caso a partida informada não exista
## ou retorna 2 caso a partida esteja pausada
## ou retorna 3 caso a partida esteja encerrada
#def pausa_partida(data_horario):
#    return
#
## Carrega uma partida que foi pausada anteriormente.
## data_horario: identificador da partida.
## retorna 0 em caso de sucesso
## ou retorna 1 caso a partida informada não exista
## ou retorna 3 caso a partida esteja encerrada
#def continua_partida(data_horario):
#    return
#
## Gera informações gerais sobre as partida de data_horarios com status #“status”. São por essas informações que a interface de usuário deve se guiar # sobre as mudanças que ocorrem na partida.
##
## data_horarios: lista com os atributos “data_horario” das partidas desejadas. #Se for
##uma lista vazia ou None, cosidera-se todas as partidas registradas.
##
## status: status para filtrar das partidas desejadas. Se for None ou string vazia,
##considera-se qualquer status.
##
## Retorna uma lita dicionário do tipo:
## [ {
##   “data_horario”,         #identificador
##   “status”,               #status da partida
##   “combinacao_atual”,     #lista com os valores dos 5 dados
##   “pontuacoes_possiveis”, #lista com dicionários com as pontuações possíveis
##                           # (ver abaixo)
##
##   “turno_atual” ,         #número do turno atual
##   “jogador_da_vez” ,      #nome do jogador da vez
##   “tentativas” ,          #número de tentativas restantes para lançamento
##   “jogadores” ,           #lista com os nomes dos jogadores participantes
##                           #(jogadores desistentes continuam registrados)
## }, … ]
##
## “pontuacoes_possiveis”:
## [ { “nome”: <nome_da_categoria1>, “pontuacao”: <pontuacao_na_categoria_1> },
##   { “nome”: <nome_da_categoria2>, “pontuacao”: <pontuacao_na_categoria_2> },
##   { “nome”: <nome_da_categoria3>, “pontuacao”: <pontuacao_na_categoria_3> }
##  ... ]
##Retorna uma lista vazia caso não seja encontrado nenhuma tabela com as chaves
##escolhidas
#def obtem_info_partida(data_horarios, status):
#    return
#
##Retira um jogador da partida sem afetar o resto da partida.
##Retorna 0 em caso de sucesso.
## ou retorna 1 caso a partida informada não exista
## ou retorna 2 caso a partida esteja pausada
## ou retorna 3 caso a partida esteja encerrada
## ou retorna 4 caso o nome seja inválido
## ou retorna 5 caso o jogador já tenha desistido da partida.
#def desiste(data_horario, nome_jogador):
#    return
#
