import unittest

class Test(unittest.TestCase):
##########################
#      TESTES BANCO:      
#      Daniel Menezes 
#      19/05/2020
##########################
    def test_AAA_abre_acesso_ok_condicao_retorno(self):
        print("Caso de Teste AAA - Abre acesso Condição de retorno tipos"+
                " corretos.")
        retorno = banco_de_dados.abre_acesso()
        self.assertTrue(
             (type(retorno['conexao']) is\
                     mysql.connector.connection.MySQLConnection)\
                 and
             (type(retorno['cursor']) is\
                     mysql.connector.cursor.MySQLCursorBufferedDict)
        )
        retorno['conexao'].close()
        retorno['cursor'].close()

    # Não há como testar o retorno 1 de abre_acesso em teste de caixa
    # fechada.

    def test_AAA_fecha_acesso_ok_condicao_retorno(self):
        print("Caso de Teste AAA - Fecha acesso Condição de retorno ok.")
        dic = banco_de_dados.abre_acesso()
        retorno = banco_de_dados.fecha_acesso(dic['conexao'], dic['cursor'])
        self.assertEqual(retorno, 0)


    # Não há como testar o retorno 1 de fecha_acesso em teste de caixa
    # fechada.

    def test_AAA_fecha_acesso_nok_condicao_retorno_tipo_invalido(self):
        print("Caso de Teste AAA - Fecha acesso parâmetros inválidos.")
        retorno = banco_de_dados.fecha_acesso(1, 'daniel')
        self.assertEqual(retorno, 2)

unittest.main()
