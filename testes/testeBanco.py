import unittest


class Test(unittest.TestCase):
##########################
#      TESTES BANCO:      
#      Daniel Menezes 
#      19/05/2020
##########################
    def test_AAA_configura_banco_ok_condicao_retorno(self):
        print("Caso de Teste AAA - Configura banco ok condição de retorno")
        retorno = banco_de_dados.configura()
        self.assertEqual(retorno, 0)

    #Não é possível testar o erro de conexão em teste de caixa fechada

    def test_AAA_abre_acesso_ok_condicao_retorno(self):
        print("Caso de Teste AAA - Abre acesso tipos corretos.")
        retorno = banco_de_dados.abre_acesso()
        self.assertTrue( isinstance(retorno['conexao'],
                         mysql.connector.connection.MySQLConnection)
                     and
                         isinstance(retorno['cursor'],
                         mysql.connector.cursor.MySQLCursor))
        retorno['conexao'].close()
        retorno['cursor'].close()

    # Não há como testar o retorno 1 de abre_acesso em teste de caixa
    # fechada.

    def test_AAA_fecha_acesso_ok_condicao_retorno(self):
        print("Caso de Teste AAA - Fecha acesso Condição de retorno ok.")
        dic = banco_de_dados.abre_acesso()
        retorno = banco_de_dados.fecha_acesso(dic)
        self.assertEqual(retorno, 0)


    # Não há como testar o retorno 1 de fecha_acesso em teste de caixa
    # fechada.

    def test_AAA_fecha_acesso_nok_condicao_retorno_tipo_invalido(self):
        print("Caso de Teste AAA - Fecha acesso parâmetros inválidos.")
        retorno = banco_de_dados.fecha_acesso(
                    {'conexao':1, 'cursor':'daniel'}
                )
        self.assertEqual(retorno, 2)

unittest.main()
