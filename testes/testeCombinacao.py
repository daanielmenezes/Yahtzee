import unittest

#from entidades.combinacao import *

class Testmock(unittest.TestCase):
    
##########################
#      TESTES COMBINACAO:      
#      Bruno Coutinho 
#      24/04/2020
##########################

    def test_AAA_gera_combinacao_ok_mantem_dados_escolhidos(self):
        print("Caso de Teste AAA - Combinacao gerada manteve dados escolhidos")
        primeira_combinacao = combinacao.gera_combinacao([])
        primeira_combinacao = primeira_combinacao['combinacao']
        primeira_indice2 = primeira_combinacao[2]
        primeira_indice3 = primeira_combinacao[3]
        nova_combinacao = combinacao.gera_combinacao([2,3])
        nova_combinacao = nova_combinacao['combinacao']
        nova_indice2 = nova_combinacao[2]
        nova_indice3 = nova_combinacao[3]
        self.assertEqual((primeira_indice2,primeira_indice3),
                         (nova_indice2, nova_indice3))

    def test_AAA_gera_combinacao_ok_altera_dados_descartados(self):
        print("Caso de Teste AAA - Combinacao gerada alterou dados descartados")
        primeira_combinacao = combinacao.gera_combinacao([])
        primeira_combinacao = primeira_combinacao['combinacao']
        primeira_indice0 = primeira_combinacao[0]
        primeira_indice1 = primeira_combinacao[1]
        primeira_indice4 = primeira_combinacao[4]
        descartados_alterados = False
        for i in range(10):
            nova_combinacao = combinacao.gera_combinacao([2,3])
            nova_combinacao = nova_combinacao['combinacao']
            if nova_combinacao[0] != primeira_indice0 or\
               nova_combinacao[1] != primeira_indice1 or\
               nova_combinacao[4] != primeira_indice4:
                descartados_alterados = True
        self.assertTrue(descartados_alterados)

    def test_AAA_gera_combinacao_nok_indice_invalido(self):
        print("Caso de Teste AAA - Nao gera combinacao caso indice invalido")
        retorno_esperado = combinacao.gera_combinacao([2,7,-1])
        self.assertEqual(retorno_esperado, 1)

    def test_AAA_inicializa_combinacao_ok_condicao_retorno(self):
        print("Caso de Teste AAA - Inicializa combinacao com sucesso")
        retorno_esperado = combinacao.inicializa_combinacao([2,3,2,5,5])
        self.assertEqual(retorno_esperado, 0)

    def test_AAA_inicializa_combinacao_nok_tamanho_invalido(self):
        print("Caso de Teste AAA - Nao inicializa combinacao caso tamanho" +
              " da lista seja invalido")
        retorno_esperado = combinacao.inicializa_combinacao([2,3,2,5,5,7])
        self.assertEqual(retorno_esperado, 1)

    def test_AAA_inicializa_combinacao_ok_condicao_retorno(self):
        print("Caso de Teste AAA - Nao inicializa combinacao caso algum dado" +
              " tenha valor invalido")
        retorno_esperado = combinacao.inicializa_combinacao([8,3,2,-1,5])
        self.assertEqual(retorno_esperado, 2)

unittest.main()
