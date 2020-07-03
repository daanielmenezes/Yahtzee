#####################################################################
# MODULO CATEGORIA
#
#  Responsável por guardar os nomes e a descrição de todas as categorias
#  e disponibilizá-las.
# 
#--------------v1.0.0: 28/04/20-----------------
#  Por: Daniel Menezes
#  -13 categorias implementadas: 
#        1,2,3,4,5,6,tripla,quadra, sequencia4, sequencia5, fullhouse
#        yahtzee e chance
#  -obtem_nomes implementada e passando em todos os testes
#  -obtem_descricoes implementada e passando em todos os testes
#####################################################################

__all__ = ['obtem_nomes', 'obtem_descricoes']

categorias = [ 
        {
        'nome':'1',
        'descricao':'Dados com o valor 1.'
        },
        {
        'nome':'2',
        'descricao':'Dados com o valor 2.' 
        },
        {
        'nome':'3',
        'descricao':'Dados com o valor 3.'
        },
        {
        'nome':'4',
        'descricao':'Dados com o valor 4.'
        },
        {
        'nome':'5',
        'descricao':'Dados com o valor 5.'
        },
        {
        'nome':'6',
        'descricao':'Dados com o valor 6.'
        },
        {
        'nome':'tripla',
        'descricao':'Tres dados com o mesmo valor.'
        },
        {
        'nome':'quadra',
        'descricao':'Quatro dados com o mesmo valor.'
        },
        {
        'nome':'fullhouse',
        'descricao':'Uma dupla e uma tripla de valores diferentes.'
        },
        {
        'nome':'sequencia4',
        'descricao':'Quatro dados em sequencia.'
        },
        {
        'nome':'sequencia5',
        'descricao':'Cinco dados em sequencia.'
        },
        {
        'nome':'yahtzee',
        'descricao':'Cinco dados com o mesmo valor.'
        },
        {
        'nome':'chance',
        'descricao':'Sem condicoes, pode ser marcado a qualquer momento'
        }

    ]

#########################################################
# Retorna uma lista de dicionários com os nomes de todas 
# as categorias implementadas: 
# [ {“nome”:<nome_da_cat1>}, 
#   {“nome”:<nome_da_cat2>},
#    … ]
#########################################################
def obtem_nomes():
    return [ {'nome':categoria['nome']} for categoria in categorias ]




#########################################################
#Obtem todas as categorias e suas descrições.
#Retorna uma lista de dicionários:
#########################################################

def obtem_descricoes():
    return categorias
