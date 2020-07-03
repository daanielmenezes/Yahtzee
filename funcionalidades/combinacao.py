#####################################################################
# MODULO COMBINACAO
#
#  Responsável por gerar combinações de 5 dados e a sua avaliação
#  em pontos em cada categoria.
#
#--------------v0.1.0: 03/05/2020--------------------
#  Por: Daniel Menezes
#  -usando mocking do modulo avalia
#  -gera_combinacao implementada e passando nos testes
#--------------v1.0.0: 03/05/2020--------------------
#  Por: Daniel Menezes
#  - mocking de avalia removido
#
#--------------v1.0.1: 02/06/2020--------------------
#  Por: Bruno Coutinho
#  -função inicializa_combinacao implementada
#####################################################################

from . import dado

from .avalia import avalia_combinacao as avalia

__all__ = ["gera_combinacao", "inicializa_combinacao"]

combinacao = [None, None, None, None, None]
#pode ser inicializada com valores salvos ao continuar uma partida. Isso é
#feito com a função de acesso inicializa_combinacao

###############################################################################
#
#  sorteia uma nova combinação mantendo os valores dos dados escolhidos
#  dados_escolhidos: índices (inteiros no intervalo [0,4]) dos dados a terem
#  seus valores mantidos ou
#  lista vazia para modificar todos os dados
#  retorna um dicionário do tipo:
#  {“pontos”, “combinacao”}
#  “pontos” : dicionário com a pontuação da combinação em cada categoria
#  na forma
#  [ { “nome”: <nome_da_categoria1>, “pontuacao”: <pontuacao_na_categoria_1> },
#    { “nome”: <nome_da_categoria2>, “pontuacao”: <pontuacao_na_categoria_2> },
#    { “nome”: <nome_da_categoria3>, “pontuacao”: <pontuacao_na_categoria_3> }
#   ... ]
#  combinacao: lista com 5 valores de dados (inteiros no intervalo [1,6])
#  retorna 1 caso um dos índices em dados_escolhidos não seja válido
#
###############################################################################
def gera_combinacao(dados_escolhidos = []):
    if any([i not in range(5) for i in dados_escolhidos]):
        #um dos índices em dados_escolhidos não é válido
        return 1
    for i in range(5):
        if i not in dados_escolhidos:
            combinacao[i] = dado.rola(6)
    pontos = avalia(combinacao)
    return {'pontos':pontos, 'combinacao':combinacao}


###############################################################################
# 
# Inicializa a combinação encapsulada com a lista da última combinação
# ao continuar uma partida
# combinacao_fornecida: lista com 5 valores entre 1 e 6 representando os valores
# dos dados da última combinação
# retorna 1 caso o tamanho da lista combinacao_fornecida seja inválido
# retorna 2 caso algum dos dados tenha valor inválido 
#
###############################################################################


def inicializa_combinacao(combinacao_fornecida):
    if len(combinacao_fornecida) != 5:
        return 1
    
    for dado in combinacao_fornecida:
        if dado not in range(1,7):
            return 2

    combinacao = combinacao_fornecida
    return 0

    




