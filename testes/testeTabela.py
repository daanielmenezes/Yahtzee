import unittest

class Testmock(unittest.TestCase):
##########################
#      TESTES TABELA:      
#      Bruno Coutinho 
#      25/04/2020
##########################

    def test_AAA_cria_tabela_ok_condicao_retorno(self):
        print("Caso de Teste AAA - Cria tabela com sucesso")
        jogador.insere('eduardo')

        #adiciona partida ao bd para ser usada para testes.
        
        banco = banco_de_dados.abre_acesso()
        data_horario = datetime(2020,2,2,10)
        sql_teste = """INSERT INTO Partida VALUES (%s, %s)"""
        banco['cursor'].execute(sql_teste, (data_horario, 'encerrada'))
        banco_de_dados.fecha_acesso(banco)

        retorno_esperado = tabela.cria_tabela('eduardo', data_horario) 
        self.assertEqual(retorno_esperado, 0)

    def test_AAA_cria_tabela_ok_criada_com_sucesso(self):
        print("Caso de Teste AAA - Verifica criacao de tabela")
        temp = tabela.obtem_tabelas(['eduardo'], [datetime(2020,2,2,10)])
        self.assertEqual((temp[0]['nome_jogador'],
                          temp[0]['data_horario'],
                          temp[0]['pontuacao_total']),
                         ('eduardo',datetime(2020,2,2,10),0))

    def test_AAA_cria_tabela_nok_nome_inexistente(self):
        print("Caso de Teste AAA - Impede criacao de tabela caso" +
              " nao exista jogador com nome fornecido")
        retorno_esperado = tabela.cria_tabela('norma', datetime(2020,2,2,10))
        self.assertEqual(retorno_esperado, 1)

    def test_AAA_cria_tabela_nok_tabela_ja_existente(self):
        print("Caso de Teste AAA - Impede criacao de tabela caso" + 
              " jogador já possua tabela na partida")
        retorno_esperado = tabela.cria_tabela('eduardo',datetime(2020,2,2,10))
        self.assertEqual(retorno_esperado, 2)

    def test_AAA_insere_pontuacao_ok_condicao_retorno(self):
        print("Caso de Teste AAA - Insere pontuacao com sucesso")
        categ = categoria.obtem_nomes() 
        categ = categ[0]['nome'] #pega o nome da primeira categoria
        retorno_esperado = tabela.insere_pontuacao('eduardo',datetime(2020,2,2,10),
                                                   categ,30)
        self.assertEqual(retorno_esperado, 0)

    def test_AAA_insere_pontuacao_ok_insere_com_sucesso(self):
        print("Caso de Teste AAA - Verifica insercao")
        categ = categoria.obtem_nomes() 
        categ = categ[0]['nome'] #pega o nome da primeira categoria
        temp = tabela.obtem_tabelas(['eduardo'], [datetime(2020,2,2,10)])
        temp = temp[0]['pontos_por_categoria'] #pontos por categoria do eduardo
        pontos_categ = next(pontos for pontos in temp if pontos['nome']==categ)
        self.assertEqual(pontos_categ['pontuacao'], 30)

    def test_AAA_insere_pontuacao_nok_tabela_nao_existe(self):
        print("Caso de Teste AAA - Nao insere se a tabela informada nao existir")
        categ = categoria.obtem_nomes() 
        categ = categ[0]['nome'] #pega o nome da primeira categoria
        retorno_esperado = tabela.insere_pontuacao('karla',datetime(2020,2,2,10),
                                                   categ, 30)
        self.assertEqual(retorno_esperado, 1)

    def test_AAA_insere_pontuacao_nok_categoria_nao_existe(self):
        print("Caso de Teste AAA - Nao insere se a" +
              " categoria informada nao existir")
        retorno_esperado = tabela.insere_pontuacao('eduardo',
                                                   datetime(2020,2,2,10),
                                                   'categ_falsa', 30)
        self.assertEqual(retorno_esperado, 2)

    def test_AAA_insere_pontuacao_nok_pontos_negativos(self):
        print("Caso de Teste AAA - Nao insere se a quantidade de"+
              " pontos for negativa")
        categ = categoria.obtem_nomes() 
        categ = categ[0]['nome'] #pega o nome da primeira categoria
        retorno_esperado = tabela.insere_pontuacao('eduardo',datetime(2020,2,2,10),
                                                   categ, -30)
        self.assertEqual(retorno_esperado, 3)

    def test_AAA_insere_pontuacao_nok_categoria_ja_pontuada(self):
        print("Caso de Teste AAA - Nao insere se" +
              " o jogador ja marcou pontos na categoria informada")
        categ = categoria.obtem_nomes() 
        categ = categ[0]['nome'] #pega o nome da primeira categoria
        retorno_esperado = tabela.insere_pontuacao('eduardo',datetime(2020,2,2,10),
                                                   categ, 30)
        self.assertEqual(retorno_esperado, 4)

    def test_AAA_registra_desistencia_ok_condicao_retorno(self):
        print("Caso de Teste AAA - registra desistencia com sucesso")
        jogador.insere('jorge')
        tabela.cria_tabela('jorge',datetime(2020,2,2,10))
        retorno_esperado = tabela.registra_desistencia('jorge',
                                                       datetime(2020,2,2,10))
        self.assertEqual(retorno_esperado, 0)

    def test_AAA_registra_desistencia_ok_zera_nao_pontuadas(self):
        print("Caso de Teste AAA - Verifica se categorias nao pontuadas" +
              " foram zeradas ao desistir")
        zeradas = True
        temp = tabela.obtem_tabelas(['jorge'],[datetime(2020,2,2,10)])
        pontos_categ = temp[0]['pontos_por_categoria']
        for categ in pontos_categ:
            if categ['pontuacao']!=0:
                zeradas = False
        self.assertTrue(zeradas)

    def test_AAA_registra_desistencia_ok_desiste_com_sucesso(self):
        print("Caso de Teste AAA - Verifica desistencia")
        temp = tabela.obtem_tabelas(['jorge'], [datetime(2020,2,2,10)])
        confere_desistiu = temp[0]['desistencia']
        self.assertTrue(confere_desistiu)

    def test_AAA_registra_desistencia_nok_tabela_nao_existe(self):
        print("Caso de Teste AAA - impede desistencia caso tabela" +
              " do jogador na partida nao exista")
        retorno_esperado = tabela.registra_desistencia('karla',
                                                       datetime(2020,2,2,10))
        self.assertEqual(retorno_esperado, 1)

    def test_AAA_registra_desistencia_nok_todas_categorias_pontuadas(self):
        print("Caso de Teste AAA - impede desistencia caso jogador" +
              " ja tenha pontuado em todas as categorias")
        categorias = categoria.obtem_nomes()
        for categ in categorias[1:]:  
            nome_cat = categ['nome']
            tabela.insere_pontuacao('eduardo',datetime(2020,2,2,10),
                                                   nome_cat,30)
        retorno_esperado = tabela.registra_desistencia('eduardo',
                                                       datetime(2020,2,2,10))
        self.assertEqual(retorno_esperado, 2)

    def test_AAA_obtem_tabelas_ok(self):
        print("Caso de Teste AAA - Obter tabelas de jogadores nas partidas")
        temp = tabela.obtem_tabelas(['eduardo'],[datetime(2020,2,2,10)])
        n_categorias = len(categoria.obtem_nomes())
        self.assertEqual((temp[0]['nome_jogador'],
                          temp[0]['data_horario'],
                          temp[0]['pontuacao_total'],
                          temp[0]['desistencia']),
                         ('eduardo',datetime(2020,2,2,10),30 * n_categorias,True))

    def test_AAA_obtem_tabelas_ok_colocacoes_corretas(self):
        print("Caso de Teste AAA - Tabelas calculam colocacoes corretamente")
        tab_ed = tabela.obtem_tabelas(['eduardo'],[datetime(2020,2,2,10)])
        tab_jorge = tabela.obtem_tabelas(['jorge'],[datetime(2020,2,2,10)])
        self.assertEqual((tab_ed[0]['colocacao'], tab_jorge[0]['colocacao']),
                         (1,2))
        
    def test_AAA_obtem_tabelas_nok_nome_invalido(self):
        print("Caso de Teste AAA - obtem_info retorna 1"
              + " se a lista de nomes possuir um nome invalido")
        retorno_esperado = tabela.obtem_tabelas(['pedro'],[datetime(2020,2,2,10)])
        self.assertEqual(retorno_esperado, 1)

    def test_AAA_obtem_tabelas_nok_data_horario_invalido(self):
        print("Caso de Teste AAA - obtem_info retorna 2"
              + " se a lista de data_horario possuir um data_horario invalido")
        retorno_esperado = tabela.obtem_tabelas(['eduardo'],[datetime(2019,4,25,17)])
        self.assertEqual(retorno_esperado, 2)
        
    def test_AAA_remove_ok_condicao_retorno(self):
        print("Caso de Teste AAA - remove tabela de um jogador" +
              " em uma partida com sucesso")
        retorno_esperado = tabela.remove('eduardo',datetime(2020,2,2,10))
        self.assertEqual(retorno_esperado, 0)

    def test_AAA_remove_ok_retira_com_sucesso(self):
        print("Caso de Teste AAA - Verifica remocao")
        retorno_esperado = tabela.obtem_tabelas(['eduardo'],
                                                [datetime(2020,2,2,10)])
        self.assertEqual(retorno_esperado, 1)

    def test_AAA_remove_nok_tabela_nao_existe(self):
        print("Caso de Teste AAA - impede remocao caso tabela" +
              "do jogador na partida nao exista")
        retorno_esperado = tabela.remove('eduardo',datetime(2020,2,2,10))
        self.assertEqual(retorno_esperado, 1)


unittest.main()
