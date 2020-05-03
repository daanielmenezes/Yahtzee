import unittest

class Testmock(unittest.TestCase):
##########################
#      TESTES CATEGORIA:      
#      Daniel Menezes 
#      24/04/2020
##########################


    def test_AAA_obtem_nomes_ok_retorna_lista(self):
        print("Caso de Teste AAA - Retorno de obtem nomes é uma lista.")
        self.assertTrue(type(categoria.obtem_nomes()) is list)

    def test_AAA_obtem_nomes_ok_lista_com_nomes(self):
        print("Caso de Teste AAA - Lista possui dicionario com nome.")
        categorias = categoria.obtem_nomes()
        self.assertTrue(all('nome' in categoria for categoria in categorias))
    
    def test_AAA_obtem_descricoes_ok_retorna_lista(self):
        print("Caso de Teste AAA - Retorno de obtem_descricoes é uma lista.")
        self.assertTrue(type(categoria.obtem_descricoes()) is list)

    def test_AAA_obtem_descricoes_ok_lista_com_descricao(self):
        print("Caso de Teste AAA - Lista possui dicionario com nome e descricao.")
        descricoes = categoria.obtem_descricoes()
        iterador = ('nome' and 'descricao' in categoria for categoria in descricoes)
        self.assertTrue(all(iterador))

unittest.main()
