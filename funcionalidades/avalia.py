#####################################################################
# MODULO AVALIA
# Responsável por avaliar a possível pontuação de uma combinação
#de dados em todas as categorias
#
# Regras de pontuação para cada categoria:
#  ‘1’: Soma dos dados que possuem valor 1.
#  ‘2’: Soma dos dados que possuem valor 2.
#  ‘3’: Soma dos dados que possuem valor 3.
#  ‘4’: Soma dos dados que possuem valor 4.
#  ‘5’: Soma dos dados que possuem valor 5.
#  ‘6’: Soma dos dados que possuem valor 6.
#  ‘tripla’: Soma de todos os dados se possuir 3 dados com o mesmo valor.
#            Se não possuir, a pontuação será zero.
#  ‘quadra’: Soma de todos os dados se possuir 4 dados com o mesmo valor.
#            Se não possuir, a pontuação será zero.
#  ‘fullhouse’: 25 pontos se possuir uma tripla e uma dupla de valores diferentes.
#               Se não possuir, a pontuação será zero. 
#  ‘sequencia4’: 30 pontos se possuir 4 dados em sequência.
#              Se não possuir, a pontuação será zero.
#  ‘sequencia5’: 40 pontos se possuir uma 5 dados em sequência.
#              Se não possuir, a pontuação será zero.
#  ‘yahtzee’: 50 pontos se possuir 5 dados com um mesmo valor.
#             Se não possuir, a pontuação será zero.
#  ‘chance’: Soma de todos os dados.
#
#--------------versao 1.0.0: 03/05/20-----------------
#  Por: Bruno Coutinho
#  -avalia_combinacao implementada e passando em todos os testes
#
#--------------versao 1.0.1: 04/05/20-----------------
#  Por: Bruno Coutinho
#  -avalia_combinacao agora utilizando a funcao obtem_nomes do modulo
#categoria para inserir nomes das categorias na lista retornada
#  
#####################################################################

from entidades import categoria

__all__ = ['avalia_combinacao']

##funcoes auxiliares às funcoes de cada categoria:

def avalia_iguais_a_valor(combinacao, valor):
    retorno = 0
    for dado in combinacao:
        if dado == valor:
            retorno = retorno + valor
    return retorno

def calcula_soma_combinacao(combinacao):
    retorno = 0
    for dado in combinacao:
        retorno = retorno + dado
    return retorno

def conta_ocorrencias_dado_em_combinacao(dado_escolhido, combinacao):
    retorno = 0
    for dado in combinacao:
        if dado == dado_escolhido:
            retorno = retorno + 1
    return retorno

def avalia_sequencia_qualquer(dados_sequencia, combinacao):
    for dado in dados_sequencia:
        if not (conta_ocorrencias_dado_em_combinacao(dado, combinacao)):
            return False
    return True

##funcoes que retornam a pontuacao da combinacao em uma categoria especifica:

def avalia1(combinacao):
    return avalia_iguais_a_valor(combinacao, 1)

def avalia2(combinacao):
    return avalia_iguais_a_valor(combinacao, 2)

def avalia3(combinacao):
    return avalia_iguais_a_valor(combinacao, 3)

def avalia4(combinacao):
    return avalia_iguais_a_valor(combinacao, 4)

def avalia5(combinacao):
    return avalia_iguais_a_valor(combinacao, 5)

def avalia6(combinacao):
    return avalia_iguais_a_valor(combinacao, 6)

def avalia_tripla(combinacao):
    for dado in combinacao[:3]:
        if conta_ocorrencias_dado_em_combinacao(dado, combinacao) >= 3:
            return calcula_soma_combinacao(combinacao)
    return 0

def avalia_quadra(combinacao):
    for dado in combinacao[:2]:
        if conta_ocorrencias_dado_em_combinacao(dado, combinacao) >= 4:
            return calcula_soma_combinacao(combinacao)
    return 0

def avalia_fullhouse(combinacao):
    for dado in combinacao:
        if conta_ocorrencias_dado_em_combinacao(dado, combinacao) <2 or\
           conta_ocorrencias_dado_em_combinacao(dado, combinacao) >3:
            return 0
    return 25        

def avalia_seq4(combinacao):
    caso1 = [1,2,3,4]
    caso2 = [2,3,4,5]
    caso3 = [3,4,5,6]
    if avalia_sequencia_qualquer(caso1, combinacao) or\
       avalia_sequencia_qualquer(caso2, combinacao) or\
       avalia_sequencia_qualquer(caso3, combinacao):
        return 30
    return 0

def avalia_seq5(combinacao):
    caso1 = [1,2,3,4,5]
    caso2 = [2,3,4,5,6]
    if avalia_sequencia_qualquer(caso1, combinacao) or\
       avalia_sequencia_qualquer(caso2, combinacao):
        return 40
    return 0

def avalia_yahtzee(combinacao):
    if conta_ocorrencias_dado_em_combinacao(combinacao[0],combinacao) == 5:
        return 50
    return 0

def avalia_chance(combinacao):
    return calcula_soma_combinacao(combinacao)

##funcao auxiliar à funcao de acesso avalia_combinacao:

def insere_retorno(lista_retornada, categoria, pontuacao):
    lista_retornada.append({'nome': categoria, 'pontuacao': pontuacao})


#####################################################################
#Calcula quantos pontos uma combinação de dados vale em todas as categorias
#combinacao: lista com 5 valores de dados (inteiros no intervalo [1,6])
#Retorna uma lista de dicionários com a pontuação da combinação em cada categoria:
#[ {“nome”:<nome_cat1>, “pontuacao”:<pontuacao_cat1>},
#  {“nome”:<nome_cat2>, “pontuacao”:<pontuacao_cat2>},
#   … ]
#####################################################################

def avalia_combinacao(combinacao):

    categorias = categoria.obtem_nomes()
    #funcoes_chamadas: lista de dicionarios indicando o nome das funcoes
    #correspondentes à avaliaçao de cada categoria junto com o nome da categoria
    funcoes_chamadas = [{'nome': avalia1, 'categoria': categorias[0]['nome']},\
                        {'nome': avalia2, 'categoria': categorias[1]['nome']},\
                        {'nome': avalia3, 'categoria': categorias[2]['nome']},\
                        {'nome': avalia4, 'categoria': categorias[3]['nome']},\
                        {'nome': avalia5, 'categoria': categorias[4]['nome']},\
                        {'nome': avalia6, 'categoria': categorias[5]['nome']},\
                        {'nome': avalia_tripla, 'categoria': categorias[6]['nome']},\
                        {'nome': avalia_quadra, 'categoria': categorias[7]['nome']},\
                        {'nome': avalia_fullhouse, 'categoria': categorias[8]['nome']},\
                        {'nome': avalia_seq4, 'categoria': categorias[9]['nome']}, \
                        {'nome': avalia_seq5, 'categoria': categorias[10]['nome']},\
                        {'nome': avalia_yahtzee, 'categoria': categorias[11]['nome']},\
                        {'nome': avalia_chance, 'categoria': categorias[12]['nome']}]
    retorno = []
    for funcao in funcoes_chamadas:
        pontuacao_retornada = funcao['nome'](combinacao)
        insere_retorno(retorno, funcao['categoria'], pontuacao_retornada)
    return retorno
