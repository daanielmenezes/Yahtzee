import unittest

class Testmock(unittest.TestCase):
##########################
#      TESTES AVALIA:      
#      Daniel Menezes 
#      25/04/2020
##########################

    def test_AAA_avalia_combinacao_ok_1(self):
        print("Caso de Teste AAA - Combinacao avaliada corretamente na categoria '1'")
        retorno = avalia.avalia_combinacao([1,2,1,5,1])
        self.assertIn( {'nome':'1', 'pontuacao':2}, retorno )
    
    def test_AAA_avalia_combinacao_ok_2(self):
        print("Caso de Teste AAA - Combinacao avaliada corretamente na categoria '2'")
        retorno = avalia.avalia_combinacao([1,2,1,2,2])
        self.assertIn( {'nome':'2', 'pontuacao':6}, retorno )
        
    def test_AAA_avalia_combinacao_ok_3(self):
        print("Caso de Teste AAA - Combinacao avaliada corretamente na categoria '3'")
        retorno = avalia.avalia_combinacao([1,3,1,3,3])
        self.assertIn( {'nome':'3', 'pontuacao':9}, retorno )
        
    def test_AAA_avalia_combinacao_ok_4(self):
        print("Caso de Teste AAA - Combinacao avaliada corretamente na categoria '4'")
        retorno = avalia.avalia_combinacao([6,4,1,3,2])
        self.assertIn( {'nome':'4', 'pontuacao':4}, retorno )

    def test_AAA_avalia_combinacao_ok_5(self):
        print("Caso de Teste AAA - Combinacao avaliada corretamente na categoria '5'")
        retorno = avalia.avalia_combinacao([5,4,5,3,2])
        self.assertIn( {'nome':'5', 'pontuacao':10}, retorno )

    def test_AAA_avalia_combinacao_ok_6(self):
        print("Caso de Teste AAA - Combinacao avaliada corretamente na categoria '6'")
        retorno = avalia.avalia_combinacao([6,4,6,6,2])
        self.assertIn( {'nome':'6', 'pontuacao':18}, retorno )
        
    def test_AAA_avalia_combinacao_ok_tripla(self):
        print("Caso de Teste AAA - Combinacao avaliada corretamente na categoria 'tripla'")
        retorno = avalia.avalia_combinacao([3,4,3,3,2])
        self.assertIn( {'nome':'tripla', 'pontuacao':15}, retorno )

    def test_AAA_avalia_combinacao_ok_quadra(self):
        print("Caso de Teste AAA - Combinacao avaliada corretamente na categoria 'quadra'")
        retorno = avalia.avalia_combinacao([6,4,6,6,6])
        self.assertIn( {'nome':'quadra', 'pontuacao':28}, retorno )

    def test_AAA_avalia_combinacao_ok_fullhouse(self):
        print("Caso de Teste AAA - Combinacao avaliada corretamente na categoria 'fullhouse'")
        retorno = avalia.avalia_combinacao([6,4,4,6,6])
        self.assertIn( {'nome':'fullhouse', 'pontuacao':25}, retorno )

    def test_AAA_avalia_combinacao_ok_sequencia4(self):
        print("Caso de Teste AAA - Combinacao avaliada corretamente na categoria 'sequencia4'")
        retorno = avalia.avalia_combinacao([3,2,4,2,5])
        self.assertIn( {'nome':'sequencia4', 'pontuacao':30}, retorno )

    def test_AAA_avalia_combinacao_ok_sequencia5(self):
        print("Caso de Teste AAA - Combinacao avaliada corretamente na categoria 'sequencia5'")
        retorno = avalia.avalia_combinacao([3,2,4,6,5])
        self.assertIn( {'nome':'sequencia5', 'pontuacao':40}, retorno )

    def test_AAA_avalia_combinacao_ok_yahtzee(self):
        print("Caso de Teste AAA - Combinacao avaliada corretamente na categoria 'yahtzee'")
        retorno = avalia.avalia_combinacao([3,3,3,3,3])
        self.assertIn( {'nome':'yahtzee', 'pontuacao':50}, retorno )
        
    def test_AAA_avalia_combinacao_ok_chance(self):
        print("Caso de Teste AAA - Combinacao avaliada corretamente na categoria 'chance'")
        retorno = avalia.avalia_combinacao([3,2,4,6,5])
        self.assertIn( {'nome':'chance', 'pontuacao':20}, retorno )

unittest.main()
