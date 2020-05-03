import unittest

class Testmock(unittest.TestCase):
##########################
#      TESTES DADO:      
#      Daniel Menezes 
#      24/04/2020
##########################

    def test_AAA_rola_ok_intervalo(self):
        print("Caso de Teste AAA - Valores dos dados dentro do intervalo.")
        correto = False
        for i in range(4):
            correto = dado.rola(6) in range(1,7)
            if not correto:
                break
        self.assertTrue(correto)
    
    def test_AAA_rola_ok_aleatorio(self):
        print("Caso de Teste AAA - Dados gerando valores diferentes.")
        primeiro_valor = dado.rola(6)
        for i in range(10):
            if primeiro_valor != dado.rola(6):
                diferente = True
        self.assertTrue(diferente)

    def test_AAA_rola_nok_faces_invalido(self):
        print("Caso de Teste AAA - Valor invalido de n_faces.")
        self.assertEqual(-1, dado.rola(-1))
        
unittest.main()
