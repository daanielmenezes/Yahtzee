import unittest

#from entidades.jogador import *

class Testmock(unittest.TestCase):
##########################
#      TESTES JOGADOR:      
#      Bruno Coutinho 
#      25/04/2020
##########################

    def test_AAA_insere_jogador_ok_condicao_retorno(self):
        print("Caso de Teste AAA - Insere jogador com sucesso")
        retorno_esperado = jogador.insere('maria')
        self.assertEqual(retorno_esperado, 0)

    def test_AAA_insere_jogador_ok_inserido_com_sucesso(self):
        print("Caso de Teste AAA - Verifica insercao")
        self.assertTrue(jogador.valida_jogador('maria'))

    def test_AAA_insere_jogador_nok_nome_nulo(self):
        print("Caso de Teste AAA - Impede insercao caso nome seja nulo")
        retorno_esperado = jogador.insere('')
        self.assertEqual(retorno_esperado, 1)

    def test_AAA_insere_jogador_nok_nome_existente(self):
        print("Caso de Teste AAA - Impede insercao caso nome ja exista")
        retorno_esperado = jogador.insere('maria')
        self.assertEqual(retorno_esperado, 2)

    def test_AAA_remove_jogador_ok_condicao_retorno(self):
        print("Caso de Teste AAA - Remove jogador com sucesso")
        retorno_esperado = jogador.remove('maria')
        self.assertEqual(retorno_esperado, 0)

    def test_AAA_remove_jogador_ok_removido_com_sucesso(self):
        print("Caso de Teste AAA - Verifica remocao")
        self.assertFalse(jogador.valida_jogador('maria'))

    def test_AAA_remove_jogador_nok_nome_invalido(self):
        print("Caso de Teste AAA - Impede remocao caso nome invalido")
        retorno_esperado = jogador.remove('carlos')
        self.assertEqual(retorno_esperado, 1)

    def test_AAA_obtem_info_ok(self):
        print("Caso de Teste AAA - Obter info de jogadores")
        jogador.insere('joao')
        info_joao = jogador.obtem_info(['joao'])[0]
        self.assertEqual((info_joao['nome'],
                          info_joao['pontuacao_total'],
                          info_joao['recorde']),
                         ('joao',0,0))

    def test_AAA_obtem_info_nok_jogador_nao_encontrado(self):
        print("Caso de Teste AAA - obtem_info retorna lista"
              + "vazia se nomes nao encontrados")
        retorno_esperado = jogador.obtem_info(['julia'])
        self.assertEqual(retorno_esperado, [])

    def test_AAA_atualiza_info_ok_condicao_retorno(self):
        print("Caso de Teste AAA - Atualiza pontuacao total,"+
              " ranking e recorde de jogador com sucesso")
        retorno_esperado = jogador.atualiza_info('joao', 100)
        self.assertEqual(retorno_esperado, 0)

    def test_AAA_atualiza_info_ok_atualiza_com_sucesso(self):
        print("Caso de Teste AAA - Verifica atualizacao")
        info_joao = jogador.obtem_info('joao')[0]
        self.assertEqual((info_joao['pontuacao_total'],
                          info_joao['recorde']),(100,100))

    def test_AAA_atualiza_info_nok_nome_invalido(self):
        print("Caso de Teste AAA - Impede atualizacao caso nome invalido")
        retorno_esperado = jogador.atualiza_info('carlos', 80)
        self.assertEqual(retorno_esperado, 1)

    def test_AAA_atualiza_info_pontos_negativos(self):
        print("Caso de Teste AAA - Impede atualizacao caso pontuacao negativa")
        retorno_esperado = jogador.atualiza_info('joao', -80)
        self.assertEqual(retorno_esperado, 2)

    def test_AAA_valida_jogador_nome_registrado(self):
        print("Caso de Teste AAA - valida jogador existente")
        retorno_esperado = jogador.valida_jogador('joao')
        self.assertTrue(retorno_esperado)

    def test_AAA_valida_jogador_nome_nao_registrado(self):
        print("Caso de Teste AAA - nao valida jogador nao registrado")
        retorno_esperado = jogador.valida_jogador('paula')
        self.assertFalse(retorno_esperado)


unittest.main()
