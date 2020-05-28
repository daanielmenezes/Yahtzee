#######################################################################
# MODULO PARTIDA
#
#  Centraliza as ações relacionadas ao andamento de uma partida fazendo
#  a comunicação entre os diversos módulos envolvidos. Cada partida 
#  possui um atributo identificador “data_horario”, trata-se do tipo 
#  datetime do python, indicando a data e horário em que foi criada. 
#   Uma partida pode ter status “andamento”, “pausada” ou “encerrada”.
#  Somente uma partida poderá estar em andamento ao mesmo tempo. As 
#  partidas são armazenadas no banco de dados apenas para registrar um
#  histórico. Portanto, não é possível recuperar uma partida pausada 
#  pelo banco de dados, para isso, é necessário salvar o estado da 
#  partida em um arquivo XML.
#
#---------------------------v0.1.0: 25/05/2020-------------------------
#  Por: Daniel Menezes
#  Criado mocking para tabela.cria_tabela
#  Implementada inicia_partida passando nos testes
#
#---------------------------v0.2.0: 27/05/2020-------------------------
#  Por: Daniel Menezes
#  Modificada inicia_partida. Agora se recusa a iniciar uma partida
#  caso já haja uma partida em andamento. Passando nos novos testes.
#
#---------------------------v0.3.0: 27/05/2020-------------------------
#  Por: Daniel Menezes
#  Implementada faz_lancamento. Passando nos testes.
#
#---------------------------v0.4.0: 28/05/2020-------------------------
#  Por: Daniel Menezes
#  Implementada marca_pontuacao usando mock. Passando nos testes.
#  Mocks criados: 
#    -tabela.insere_pontuacao 
#    -tabela.obtem_tabelas
#---------------------------v0.4.1: 28/05/2020------------------------
#  Por: Daniel Menezes
#  Removido import indevido de jogador.
#######################################################################

from random import shuffle
from datetime import datetime
from entidades import tabela
from funcionalidades import banco_de_dados
from funcionalidades import combinacao

from unittest import mock

__all__ = ['inicia_partida', 'faz_lancamento']


partida_atual = {}

#MOCKS:
tabela = mock.Mock()
tabela.cria_tabela.side_effect = [1, 0, 0, 0]
tabela.insere_pontuacao.side_effect = [2]
tabela.obtem_tabelas.side_effect = [
       [{'nome_jogador':'flavio', 
         'data_horario_partida':None, 
         'pontos_por_categoria': [ 
                {'nome':'chance', 'pontuacao':14},
                {'nome':'yahtzee', 'pontuacao':None}
             ],
         'pontuacao_total':14, 
         'colocacao':1,
         'desistencia':False
       }]
    ]

def _proximo_jogador():
    index = partida_atual['jogadores'].index(partida_atual['jogador_da_vez'])
    index = (index + 1) % len(partida_atual['jogadores'])
    return partida_atual['jogadores'][index]

def _partida_deve_acabar():
    tabelas = tabela.obtem_tabelas([],[partida_atual['data_horario']])

    todos_desistiram = False
    if all(tabela_jogador['desistencia'] for tabela_jogador in tabelas):
        todos_desistiram = True
    else:
        todas_as_tabelas_preenchidas = False
        jogadores_nao_desistentes = [tabela_jogador for tabela_jogador \
                in tabelas if not tabela_jogador['desistencia']]
        pontuacoes = []
        for tabela_jogador in jogadores_nao_desistentes:
            for pontos_por_cat in tabela_jogador['pontos_por_categoria']:
                pontuacoes.append(pontos_por_cat)
        if all(pts['pontuacao'] != None for pts in pontuacoes ):
            todas_as_tabelas_preenchidas = True

    return todos_desistiram or todas_as_tabelas_preenchidas

def _altera_status_bd(status):
    sql = """UPDATE Partida
             SET status = %s
             WHERE data_horario = %s"""
    banco = banco_de_dados.abre_acesso()
    banco['cursor'].execute(sql, (status, partida_atual['data_horario']))
    banco_de_dados.fecha_acesso(banco)
    return

#################################################################
# Cria uma nova partida e associa tabelas para os seus jogadores.
# nomes: lista de nomes dos jogadores participantes.
#
# retorna data_horario da partida criada em caso de sucesso
# ou retorna 1 caso um dos jogadores passados não exista.
# ou retorna 2 caso já haja uma partida em andamento.
#################################################################
def inicia_partida(nomes):
    if (partida_atual):
        return 2
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

    shuffle(nomes)
    partida_atual['data_horario'] = data_horario
    partida_atual['combinacao'] = None
    partida_atual['pts_combinacao'] = None
    partida_atual['turno'] = 1
    partida_atual['tentativas'] = 3
    partida_atual['jogadores'] = nomes
    partida_atual['jogador_da_vez'] = nomes[0]
    partida_atual['status'] = 'andamento'

    return data_horario 

############################################################################
#  Gera um novo lançamento para o jogador do turno na partida em andamento.
#  
#  dados_escolhidos: lista com os índices (inteiros no intervalo [0,4])
#   dos dados a terem seus valores mantidos
#   ou lista vazia para rolar todos os dados
#
#  Retorna 0 em caso de sucesso
#   ou retorna 1 caso não haja partida em andamento
#   ou retorna 2 caso um dos índices em dados_escolhidos não seja válido
#   ou retorna 3 caso dados_escolhidos não seja uma lista vazia no primeiro
#    lançamento do turno atual.
#   ou retorna 4 caso o jogador do turno atual já tenha esgotado o número 
#    de tentativas.
#
############################################################################
def faz_lancamento(dados_escolhidos):
    if not partida_atual:
        return 1
    if any(d not in range(1,7) for d in dados_escolhidos):
        return 2
    if partida_atual['tentativas'] == 3 and dados_escolhidos:
        return 3
    if partida_atual['tentativas'] == 0:
        return 4

    comb = combinacao.gera_combinacao(dados_escolhidos)
    partida_atual['combinacao'] = comb['combinacao'] 
    partida_atual['pts_combinacao'] = comb['pontos']
    partida_atual['tentativas'] -= 1

    return 0

########################################################################
#
#  Atribui ao jogador do turno da partida atual os pontos do seu último
#   lançamento (do mesmo turno) na categoria escolhida e passa para o
#   próximo turno.
#
#  categoria: nome da categoria escolhida
#
#  Retorna 0 em caso de sucesso
#   ou retorna 1 caso não haja partida em andamento
#   ou retorna 2 caso a categoria seja inválida
#   ou retorna 3 caso o jogador do turno ainda não tenha realizado
#     um lançamento no turno atual.
#   ou retorna 4 caso o jogador já tenha marcado pontos
#     na categoria escolhida nessa partida
#
########################################################################
def marca_pontuacao(categoria):
    if not partida_atual:
        return 1
    if partida_atual['tentativas'] == 3:
        return 3

    for categ in partida_atual['pts_combinacao']:
        if categ['nome'] == categoria:
            pontos = categ['pontuacao']
            break
    else:
        return 2

    args = [partida_atual['jogador_da_vez'],
            partida_atual['data_horario'],
            categoria,
            pontos]
    ret_insere = tabela.insere_pontuacao(*args)

    if ret_insere == 4:
        return 4

    if _partida_deve_acabar():
        partida_atual['status'] = 'encerrada'  
        _altera_status_bd('encerrada') 
    else:
        partida_atual['jogador_da_vez'] = _proximo_jogador()
        partida_atual['turno'] += 1
        partida_atual['tentativas'] = 3

    return 0

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



##############################################################################
#
# Gera informações gerais sobre a partida atual.
# São por essas informações que a interface de usuário deve se guiar
# sobre as mudanças que ocorrem na partida.
#
# Retorna um dicionário do tipo:
#   {
#   “data_horario”,         #identificador
#   “status”,               #status da partida
#   “combinacao_atual”,     #lista com os valores dos 5 dados
#   “pts_combinacoes”,      #lista com dicionários com as pontuações possíveis
#                           # (ver abaixo)
#
#   “turno_atual” ,         #número do turno atual
#   “jogador_da_vez” ,      #nome do jogador da vez
#   “tentativas” ,          #número de tentativas restantes para lançamento
#   “jogadores” ,           #lista com os nomes dos jogadores participantes
#                           #(jogadores desistentes continuam registrados)
# }
#
# “pts_combinacoes”:
# [ { “nome”: <nome_da_categoria1>, “pontuacao”: <pontuacao_na_categoria_1> },
#   { “nome”: <nome_da_categoria2>, “pontuacao”: <pontuacao_na_categoria_2> },
#   { “nome”: <nome_da_categoria3>, “pontuacao”: <pontuacao_na_categoria_3> }
#  ... ]
#
#  Retorna 1 caso não haja uma partida em andamento.
#
##############################################################################
def obtem_info_partida():
    return partida_atual

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
