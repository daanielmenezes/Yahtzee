#####################################################################
# MODULO DADO
#
#  Responsável por guardar os nomes e a descrição de todas as categorias
#  e disponibilizá-las.
# 
#--------------primeira versao: 02/05/20-----------------
#  -rola() implementada e passando em todos os testes
#  
#####################################################################

import random
__all__ = ['rola']

#####################################################################
# lança um dado.
# n_faces: um número inteiro maior que 0.
# retorna um número inteiro aleatório no intervalo [1, n_faces] ou
# retorna -1 caso n_faces seja um valor inválido.
#
#####################################################################

def rola(n_faces):
    if type(n_faces)!= int or n_faces <= 1:
        return -1
    return random.randint(1, n_faces)

