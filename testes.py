import unittest
from entidades import *
from funcionalidades import *

class Test(unittest.TestCase):

##########################
#      TESTES DADO:      
#      Daniel Menezes 
#      24/04/2020
##########################

    def test_001_rola_ok_intervalo(self):
        print("Caso de Teste 001 - Valores dos dados dentro do intervalo.")
        correto = False
        for i in range(4):
            correto = dado.rola(6) in range(1,7)
            if not correto:
                break
        self.assertTrue(correto)
    
    def test_002_rola_ok_aleatorio(self):
        print("Caso de Teste 002 - Dados gerando valores diferentes.")
        primeiro_valor = dado.rola(6)
        for i in range(10):
            if primeiro_valor != dado.rola(6):
                diferente = True
        self.assertTrue(diferente)

    def test_003_rola_nok_faces_invalido(self):
        print("Caso de Teste 003 - Valor invalido de n_faces.")
        self.assertEqual(-1, dado.rola(-1))
        

##########################
#      TESTES CATEGORIA:      
#      Daniel Menezes 
#      24/04/2020
##########################


    def test_004_obtem_nomes_ok_retorna_lista(self):
        print("Caso de Teste 004 - Retorno de obtem nomes é uma lista.")
        self.assertTrue(type(categoria.obtem_nomes()) is list)

    def test_005_obtem_nomes_ok_lista_com_nomes(self):
        print("Caso de Teste 005 - Lista possui dicionario com nome.")
        categorias = categoria.obtem_nomes()
        self.assertTrue(all('nome' in categoria for categoria in categorias))
    
    def test_006_obtem_descricoes_ok_retorna_lista(self):
        print("Caso de Teste 006 - Retorno de obtem_descricoes é uma lista.")
        self.assertTrue(type(categoria.obtem_descricoes()) is list)

    def test_007_obtem_descricoes_ok_lista_com_descricao(self):
        print("Caso de Teste 007 - Lista possui dicionario com nome e descricao.")
        descricoes = categoria.obtem_descricoes()
        iterador = ('nome' and 'descricao' in categoria for categoria in descricoes)
        self.assertTrue(all(iterador))


##########################
#      TESTES AVALIA:      
#      Daniel Menezes 
#      25/04/2020
##########################

    def test_008_avalia_combinacao_ok_1(self):
        print("Caso de Teste 008 - Combinacao avaliada corretamente na categoria '1'")
        retorno = avalia.avalia_combinacao([1,2,1,5,1])
        self.assertIn( {'nome':'1', 'pontuacao':2}, retorno )
    
    def test_009_avalia_combinacao_ok_2(self):
        print("Caso de Teste 009 - Combinacao avaliada corretamente na categoria '2'")
        retorno = avalia.avalia_combinacao([1,2,1,2,2])
        self.assertIn( {'nome':'2', 'pontuacao':6}, retorno )
        
    def test_010_avalia_combinacao_ok_3(self):
        print("Caso de Teste 010 - Combinacao avaliada corretamente na categoria '3'")
        retorno = avalia.avalia_combinacao([1,3,1,3,3])
        self.assertIn( {'nome':'3', 'pontuacao':9}, retorno )
        
    def test_011_avalia_combinacao_ok_4(self):
        print("Caso de Teste 011 - Combinacao avaliada corretamente na categoria '4'")
        retorno = avalia.avalia_combinacao([6,4,1,3,2])
        self.assertIn( {'nome':'4', 'pontuacao':4}, retorno )

    def test_012_avalia_combinacao_ok_5(self):
        print("Caso de Teste 012 - Combinacao avaliada corretamente na categoria '5'")
        retorno = avalia.avalia_combinacao([5,4,5,3,2])
        self.assertIn( {'nome':'5', 'pontuacao':10}, retorno )

    def test_013_avalia_combinacao_ok_6(self):
        print("Caso de Teste 013 - Combinacao avaliada corretamente na categoria '6'")
        retorno = avalia.avalia_combinacao([6,4,6,6,2])
        self.assertIn( {'nome':'6', 'pontuacao':18}, retorno )
        
    def test_014_avalia_combinacao_ok_tripla(self):
        print("Caso de Teste 014 - Combinacao avaliada corretamente na categoria 'tripla'")
        retorno = avalia.avalia_combinacao([3,4,3,3,2])
        self.assertIn( {'nome':'tripla', 'pontuacao':15}, retorno )

    def test_015_avalia_combinacao_ok_quadra(self):
        print("Caso de Teste 015 - Combinacao avaliada corretamente na categoria 'quadra'")
        retorno = avalia.avalia_combinacao([6,4,6,6,6])
        self.assertIn( {'nome':'quadra', 'pontuacao':28}, retorno )

    def test_016_avalia_combinacao_ok_fullhouse(self):
        print("Caso de Teste 016 - Combinacao avaliada corretamente na categoria 'fullhouse'")
        retorno = avalia.avalia_combinacao([6,4,4,6,6])
        self.assertIn( {'nome':'fullhouse', 'pontuacao':25}, retorno )

    def test_017_avalia_combinacao_ok_sequencia4(self):
        print("Caso de Teste 017 - Combinacao avaliada corretamente na categoria 'sequencia4'")
        retorno = avalia.avalia_combinacao([3,2,4,2,5])
        self.assertIn( {'nome':'sequencia4', 'pontuacao':30}, retorno )

    def test_018_avalia_combinacao_ok_sequencia5(self):
        print("Caso de Teste 018 - Combinacao avaliada corretamente na categoria 'sequencia5'")
        retorno = avalia.avalia_combinacao([3,2,4,6,5])
        self.assertIn( {'nome':'sequencia5', 'pontuacao':40}, retorno )

    def test_019_avalia_combinacao_ok_yahtzee(self):
        print("Caso de Teste 019 - Combinacao avaliada corretamente na categoria 'yahtzee'")
        retorno = avalia.avalia_combinacao([3,3,3,3,3])
        self.assertIn( {'nome':'yahtzee', 'pontuacao':50}, retorno )
        
    def test_020_avalia_combinacao_ok_chance(self):
        print("Caso de Teste 020 - Combinacao avaliada corretamente na categoria 'chance'")
        retorno = avalia.avalia_combinacao([3,2,4,6,5])
        self.assertIn( {'nome':'chance', 'pontuacao':20}, retorno )


#from entidades.combinacao import *

    
##########################
#      TESTES COMBINACAO:      
#      Bruno Coutinho 
#      24/04/2020
##########################

    def test_021_gera_combinacao_ok_mantem_dados_escolhidos(self):
        print("Caso de Teste 021 - Combinacao gerada manteve dados escolhidos")
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

    def test_022_gera_combinacao_ok_altera_dados_descartados(self):
        print("Caso de Teste 022 - Combinacao gerada alterou dados descartados")
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
                descartaos_alterados = True
        self.assertTrue(descartados_alterados)

    def test_023_gera_combinacao_nok_indice_invalido(self):
        print("Caso de Teste 023 - Nao gera combinacao caso indice invalido")
        retorno_esperado = combinacao.gera_combinacao([2,7,-1])
        self.assertEqual(retorno_esperado, 1)


#from entidades.jogador import *

##########################
#      TESTES JOGADOR:      
#      Bruno Coutinho 
#      25/04/2020
##########################

    def test_024_insere_jogador_ok_condicao_retorno(self):
        print("Caso de Teste 024 - Insere jogador com sucesso")
        retorno_esperado = jogador.insere('maria')
        self.assertEqual(retorno_esperado, 0)

    def test_025_insere_jogador_ok_inserido_com_sucesso(self):
        print("Caso de Teste 025 - Verifica insercao")
        self.assertTrue(jogador.valida_jogador('maria'))

    def test_026_insere_jogador_nok_nome_nulo(self):
        print("Caso de Teste 026 - Impede insercao caso nome seja nulo")
        retorno_esperado = jogador.insere('')
        self.assertEqual(retorno_esperado, 1)

    def test_027_insere_jogador_nok_nome_existente(self):
        print("Caso de Teste 027 - Impede insercao caso nome ja exista")
        retorno_esperado = jogador.insere('maria')
        self.assertEqual(retorno_esperado, 2)

    def test_028_remove_jogador_ok_condicao_retorno(self):
        print("Caso de Teste 028 - Remove jogador com sucesso")
        retorno_esperado = jogador.remove('maria')
        self.assertEqual(retorno_esperado, 0)

    def test_029_remove_jogador_ok_removido_com_sucesso(self):
        print("Caso de Teste 029 - Verifica remocao")
        self.assertFalse(jogador.valida_jogador('maria'))

    def test_030_remove_jogador_nok_nome_invalido(self):
        print("Caso de Teste 030 - Impede remocao caso nome invalido")
        retorno_esperado = jogador.remove('carlos')
        self.assertEqual(retorno_esperado, 1)

    def test_031_obtem_info_ok(self):
        print("Caso de Teste 031 - Obter info de jogadores")
        jogador.insere('joao')
        info_joao = jogador.obtem_info(['joao'])[0]
        self.assertEqual((info_joao['nome'],
                          info_joao['pontuacao_total'],
                          info_joao['recorde']),
                         ('joao',0,0))

    def test_032_obtem_info_nok_jogador_nao_encontrado(self):
        print("Caso de Teste 032 - obtem_info retorna lista"
              + "vazia se nomes nao encontrados")
        retorno_esperado = jogador.obtem_info(['julia'])
        self.assertEqual(retorno_esperado, [])

    def test_033_atualiza_info_ok_condicao_retorno(self):
        print("Caso de Teste 033 - Atualiza pontuacao total,"+
              " ranking e recorde de jogador com sucesso")
        retorno_esperado = jogador.atualiza_info('joao', 100)
        self.assertEqual(retorno_esperado, 0)

    def test_034_atualiza_info_ok_atualiza_com_sucesso(self):
        print("Caso de Teste 034 - Verifica atualizacao")
        info_joao = jogador.obtem_info('joao')[0]
        self.assertEqual((info_joao['pontuacao_total'],
                          info_joao['recorde']),(100,100))

    def test_035_atualiza_info_nok_nome_invalido(self):
        print("Caso de Teste 035 - Impede atualizacao caso nome invalido")
        retorno_esperado = jogador.atualiza_info('carlos', 80)
        self.assertEqual(retorno_esperado, 1)

    def test_036_atualiza_info_pontos_negativos(self):
        print("Caso de Teste 036 - Impede atualizacao caso pontuacao negativa")
        retorno_esperado = jogador.atualiza_info('joao', -80)
        self.assertEqual(retorno_esperado, 2)

    def test_037_valida_jogador_nome_registrado(self):
        print("Caso de Teste 037 - valida jogador existente")
        retorno_esperado = jogador.valida_jogador('joao')
        self.assertTrue(retorno_esperado)

    def test_038_valida_jogador_nome_nao_registrado(self):
        print("Caso de Teste 038 - nao valida jogador nao registrado")
        retorno_esperado = jogador.valida_jogador('paula')
        self.assertFalse(retorno_esperado)



##########################
#      TESTES TABELA:      
#      Bruno Coutinho 
#      25/04/2020
##########################

    def test_039_cria_tabela_ok_condicao_retorno(self):
        print("Caso de Teste 039 - Cria tabela com sucesso")
        jogador.insere('eduardo')
        retorno_esperado = tabela.cria_tabela('eduardo','25:04:20:17:00:00')
        self.assertEqual(retorno_esperado, 0)

    def test_040_cria_tabela_ok_criada_com_sucesso(self):
        print("Caso de Teste 040 - Verifica criacao de tabela")
        temp = tabela.obtem_tabelas(['eduardo'], ['25:04:20:17:00:00'])
        self.assertEqual((temp[0]['nome_jogador'],
                          temp[0]['data_horario_partida'],
                          temp[0]['pontuacao_total']),
                         ('eduardo','25:04:20:17:00:00',0))

    def test_041_cria_tabela_nok_nome_inexistente(self):
        print("Caso de Teste 041 - Impede criacao de tabela caso" +
              " nao exista jogador com nome fornecido")
        retorno_esperado = tabela.cria_tabela('norma', '25:04:20:17:00:00')
        self.assertEqual(retorno_esperado, 1)

    def test_042_cria_tabela_nok_tabela_ja_existente(self):
        print("Caso de Teste 042 - Impede criacao de tabela caso" + 
              " jogador já possua tabela na partida")
        retorno_esperado = tabela.cria_tabela('eduardo','25:04:20:17:00:00')
        self.assertEqual(retorno_esperado, 2)

    def test_043_insere_pontuacao_ok_condicao_retorno(self):
        print("Caso de Teste 043 - Insere pontuacao com sucesso")
        categ = categoria.obtem_nomes() 
        categ = categ[0]['nome'] #pega o nome da primeira categoria
        retorno_esperado = tabela.insere_pontuacao('eduardo','25:04:20:17:00:00',
                                                   categ,30)
        self.assertEqual(retorno_esperado, 0)

    def test_044_insere_pontuacao_ok_insere_com_sucesso(self):
        print("Caso de Teste 044 - Verifica insercao")
        categ = categoria.obtem_nomes() 
        categ = categ[0]['nome'] #pega o nome da primeira categoria
        temp = tabela.obtem_tabelas(['eduardo'], ['25:04:20:17:00:00'])
        temp = temp[0]['pontos_por_categoria'] #pontos por categoria do eduardo
        pontos_categ = next(pontos for pontos in temp if pontos['nome']==categ)
        self.assertEqual(pontos_categ['pontuacao'], 30)

    def test_045_insere_pontuacao_nok_tabela_nao_existe(self):
        print("Caso de Teste 045 - Nao insere se a tabela informada nao existir")
        categ = categoria.obtem_nomes() 
        categ = categ[0]['nome'] #pega o nome da primeira categoria
        retorno_esperado = tabela.insere_pontuacao('karla','25:04:20:17:00:00',
                                                   categ, 30)
        self.assertEqual(retorno_esperado, 1)

    def test_046_insere_pontuacao_nok_categoria_nao_existe(self):
        print("Caso de Teste 046 - Nao insere se a" +
              " categoria informada nao existir")
        retorno_esperado = tabela.insere_pontuacao('eduardo',
                                                   '25:04:20:17:00:00',
                                                   'categ_falsa', 30)
        self.assertEqual(retorno_esperado, 2)

    def test_047_insere_pontuacao_nok_pontos_negativos(self):
        print("Caso de Teste 047 - Nao insere se a quantidade de"+
              " pontos for negativa")
        categ = categoria.obtem_nomes() 
        categ = categ[0]['nome'] #pega o nome da primeira categoria
        retorno_esperado = tabela.insere_pontuacao('eduardo','25:04:20:17:00:00',
                                                   categ, -30)
        self.assertEqual(retorno_esperado, 3)

    def test_048_insere_pontuacao_nok_categoria_ja_pontuada(self):
        print("Caso de Teste 048 - Nao insere se" +
              " o jogador ja marcou pontos na categoria informada")
        categ = categoria.obtem_nomes() 
        categ = categ[0]['nome'] #pega o nome da primeira categoria
        retorno_esperado = tabela.insere_pontuacao('eduardo','25:04:20:17:00:00',
                                                   categ, 30)
        self.assertEqual(retorno_esperado, 4)

    def test_049_registra_desistencia_ok_condicao_retorno(self):
        print("Caso de Teste 049 - registra desistencia com sucesso")
        jogador.insere('jorge')
        tabela.cria_tabela('jorge','25:04:20:17:00:00')
        retorno_esperado = tabela.registra_desistencia('jorge',
                                                       '25:04:20:17:00:00')
        self.assertEqual(retorno_esperado, 0)

    def test_050_registra_desistencia_ok_zera_nao_pontuadas(self):
        print("Caso de Teste 050 - Verifica se categorias nao pontuadas" +
              " foram zeradas ao desistir")
        zeradas = True
        temp = tabela.obtem_tabelas(['jorge'],['25:04:20:17:00:00'])
        pontos_categ = temp[0]['pontos_por_categoria']
        for categ in pontos_categ:
            if categ['pontuacao']!=0:
                zeradas = False
        assertTrue(zeradas)

    def test_051_registra_desistencia_ok_desiste_com_sucesso(self):
        print("Caso de Teste 051 - Verifica desistencia")
        temp = tabela.obtem_tabelas(['jorge'], ['25:04:20:17:00:00'])
        confere_desistiu = temp[0]['desistencia']
        self.assertTrue(confere_desistiu)

    def test_052_registra_desistencia_nok_tabela_nao_existe(self):
        print("Caso de Teste 052 - impede desistencia caso tabela" +
              " do jogador na partida nao exista")
        retorno_esperado = tabela.registra_desistencia('karla',
                                                       '25:04:20:17:00:00')
        self.assertEqual(retorno_esperado, 1)

    def test_053_registra_desistencia_nok_todas_categorias_pontuadas(self):
        print("Caso de Teste 053 - impede desistencia caso jogador" +
              " ja tenha pontuado em todas as categorias")
        categorias = categoria.obtem_nomes()
        for categ in categorias[1:]:  
            nome_cat = categ['nome']
            tabela.insere_pontuacao('eduardo','25:04:20:17:00:00',
                                                   nome_cat,30)
        retorno_esperado = tabela.registra_desistencia('eduardo',
                                                       '25:04:20:17:00:00')
        self.assertEqual(retorno_esperado, 2)

    def test_054_obtem_tabelas_ok(self):
        print("Caso de Teste 054 - Obter tabelas de jogadores nas partidas")
        temp = tabela.obtem_tabelas(['eduardo'],['25:04:20:17:00:00'])
        n_categorias = len(categorias.obtem_nomes())
        self.assertEqual((temp[0]['nome_jogador'],
                          temp[0]['data_horario_partida'],
                          temp[0]['pontuacao_total'],
                          temp[0]['desistencia']),
                         ('eduardo','25:04:20:17:00:00',30 * n_categorias,True))

    def test_055_obtem_tabelas_ok_colocacoes_corretas(self):
        print("Caso de Teste 055 - Tabelas calculam colocacoes corretamente")
        tab_ed = tabela.obtem_tabelas(['eduardo'],['25:04:20:17:00:00'])
        tab_jorge = tabela.obtem_tabelas(['jorge'],['25:04:20:17:00:00'])
        self.assertEqual((tab_ed[0]['colocacao'], tab_jorge[0]['colocacao']),
                         (1,2))
        
    def test_056_obtem_tabelas_nok_nome_invalido(self):
        print("Caso de Teste 056 - obtem_info retorna 1"
              + " se a lista de nomes possuir um nome invalido")
        retorno_esperado = tabela.obtem_tabelas(['pedro'],['25:04:20:17:00:00'])
        self.assertEqual(retorno_esperado, 1)

    def test_057_obtem_tabelas_nok_data_horario_invalido(self):
        print("Caso de Teste 057 - obtem_info retorna 2"
              + " se a lista de data_horario possuir um data_horario invalido")
        retorno_esperado = tabela.obtem_tabelas(['eduardo'],['25:04:19:17:00:00'])
        self.assertEqual(retorno_esperado, 2)
        
    def test_058_remove_ok_condicao_retorno(self):
        print("Caso de Teste 058 - remove tabela de um jogador" +
              " em uma partida com sucesso")
        retorno_esperado = tabela.remove('eduardo','25:04:20:17:00:00')
        self.assertEqual(retorno_esperado, 0)

    def test_059_remove_ok_retira_com_sucesso(self):
        print("Caso de Teste 059 - Verifica remocao")
        retorno_esperado = tabela.obtem_tabelas(['eduardo'],
                                                ['25:04:20:17:00:00'])
        self.assertEqual(retorno_esperado, [])

    def test_060_remove_nok_tabela_nao_existe(self):
        print("Caso de Teste 060 - impede remocao caso tabela" +
              "do jogador na partida nao exista")
        retorno_esperado = tabela.remove('eduardo','25:04:20:17:00:00')
        self.assertEqual(retorno_esperado, 1)



##########################
#      TESTES PARTIDA:      
#      Daniel Menezes 
#      25/04/2020
##########################

#As vezes a ordem parece estranha mas faz sentido com o 
#desenvolvimento incremental das funcoes do modulo
# ja que algumas condicoes de retorno de algumas funcoes 
# so conseguem ser atingidas por uma condicao especifica de 
# outra funcao
# Por exemplo:
#  pausa_partida tem um retorno especifico caso a partida ja tenha 
#se encerrado e uma partida so consegue ser encerrada com todas as 
#categorias sendo marcadas, entao eh necessario que marca_pontuacao
#esteja implementada. Mas marca_pontuacao tem um retorno especifico 
#caso a partida esteja pausada, exigindo que pausa_partida esteja 
#implementada. Isso se resolve implementando o retorno de sucesso 
# e de partida encerrada de marca_pontuacao, depois o retorno de 
#sucesso e de partida encerrada de pausa_partida e depois o retorno
#de partida encerrada de marca_pontuacao.

#Guia:
#A partida do juan nao existe
#A partida do flavio, lucas e julia ficara em andamento
#A partida do eleanor sera pausada
#A partida do hugo sera encerrada

    def test_061_inicia_partida_ok(self):
        print("Caso de Teste 061 - Inicia partida com sucesso.")
        jogador.insere("flavio")
        jogador.insere("lucas")
        jogador.insere("julia")
        retorno = partida.inicia_partida(["flavio", "lucas", "julia"])
        self.assertIs( type(retorno), str )
   
    def test_062_inicia_partida_nok_jogador_nao_existente(self):
        print("Caso de Teste 062 - Inicia partida nao aceita jogador"+
            " inexistente.")
        retorno = partida.inicia_partida(["juan"])
        self.assertEqual( retorno , 1 )

    def test_063_faz_lancamento_ok(self):
        print("Caso de Teste 063 - Faz lancamento em nova partida sucesso.")
        jogador.insere("eleanor")
        data_horario = partida.inicia_partida(["eleanor"])
        retorno = partida.faz_lancamento(data_horario,[])
        self.assertEqual(retorno,0)

    def test_064_faz_lancamento_nok_partida_inexistente(self):
        print("Caso de Teste 064 - Erro em fazer lancamento em partida"+
                " inexistente.")
        retorno = partida.faz_lancamento("11:01:00:12:23:11",[])
        self.assertEqual( retorno, 1 )

    def test_065_pausa_partida_ok(self):
        print("Caso de Teste 065 - Partida pausada com sucesso.")
        data_horario = tabela.obtem_tabelas(['eleanor'],[])[-1]['data_horario']
        retorno = partida.pausa_partida(data_horario) 
        assertEqual( retorno , 0 )

    def test_066_faz_lancamento_nok_partida_pausada(self):
        print("Caso de Teste 066 - Erro em fazer lancamento em partida"+
                " pausada.")
        data_horario = tabela.obtem_tabelas(['eleanor'],[])[-1]['data_horario']
        retorno = partida.faz_lancamento(data_horario,[])
        self.assertEqual( retorno, 2 )

    def test_067_marca_pontuacao_ok_sucesso(self):
        print("Caso de Teste 067 - Marca pontuacao em uma categoria com"+
                " sucesso.")
        data_horario = tabela.obtem_tabelas(['flavio'],[])[-1]['data_horario']
        partida.faz_lancamento(data_horario,[])
        retorno = partida.marca_pontuacao(data_horario, 'chance')
        self.assertEqual( retorno, 0 )

    def test_068_marca_pontuacao_ok_pontos_na_tabela(self):
        print("Caso de Teste 068 - Insere pontuacao na tabela com sucesso"+
                " sucesso.")
        pts_cat = tabela.obtem_tabelas(['flavio'],[])[-1]['pontos_por_categoria']
        chance = next(cat for cat in pts_cat if cat['nome'] == 'chance')[0] 
        self.assertNotEqual( chance['pontuacao'], 0 )

    def test_069_faz_lancamento_nok_partida_encerrada(self):
        print("Caso de Teste 069 - Erro em fazer lancamento em partida"+
                " encerrada.")
        jogador.insere("hugo")
        data_horario = partida.inicia_partida(["hugo"])
        for categoria in categoria.obtem_nomes():
            #encerrando uma partida marcando todas as categorias
            partida.faz_lancamento(data_horario,[])
            partida.marca_pontuacao(categoria['nome'])
        retorno = partida.faz_lancamento(data_horario,[])
        self.assertEqual(retorno, 3)

    def test_070_faz_lancamento_nok_indice_invalido(self):
        print("Caso de Teste 070 - Erro em fazer lancamento com indices de dados"+
                " invalidos.")
        data_horario = tabela.obtem_tabelas(['flavio'],[])[-1]['data_horario']
        retorno = partida.faz_lancamento(data_horario, [-1,5])
        self.assertEqual(retorno, 4)

    def test_071_faz_lancamento_nok_indice_primeiro_lancamento_indice(self):
        print("Caso de Teste 071 - Erro em fazer primeiro lancamento do turno"+
                " com indices de dados escolhidos.")
        data_horario = tabela.obtem_tabelas(['flavio'],[])[-1]['data_horario']
        retorno = partida.faz_lancamento(data_horario, [1,3])
        self.assertEqual(retorno, 5)

    def test_072_marca_pontuacao_nok_partida_inexistente(self):
        print("Caso de Teste 072 - Erro ao marcar pontuacao em partida"+
                " inexistente.")
        retorno = partida.marca_pontuacao("11:01:00:10:21:41", 'chance')
        self.assertEqual( retorno, 1 )

    def test_073_marca_pontuacao_nok_partida_pausada(self):
        print("Caso de Teste 073 - Erro ao marcar pontuacao em partida "+
                "pausada.")
        data_horario = tabela.obtem_tabelas(['eleanor'],[])[-1]['data_horario']
        retorno = partida.marca_pontuacao(data_horario, 'chance')
        self.assertEqual( retorno, 2 )

    def test_074_marca_pontuacao_nok_partida_encerrada(self):
        print("Caso de Teste 074 - Erro ao marcar pontuacao em partida"+
                " encerrada.")
        data_horario = tabela.obtem_tabelas(['hugo'],[])[-1]['data_horario']
        retorno = partida.marca_pontuacao(data_horario, 'chance')
        self.assertEqual( retorno, 3 )

    def test_075_marca_pontuacao_nok_categoria_invalida(self):
        print("Caso de Teste 075 - Erro ao marcar pontuacao invalida.")
        data_horario = tabela.obtem_tabelas(['flavio'],[])[-1]['data_horario']
        partida.faz_lancamento(data_horario, [])
        retorno = partida.marca_pontuacao(data_horario, 'abacate')
        self.assertEqual( retorno, 4 )

    def test_076_marca_pontuacao_nok_jogador_do_turno_nao_lancou(self):
        print("Caso de Teste 076 - Erro ao marcar pontuacao sem lancar"+
                " dados no turno.")
        data_horario = tabela.obtem_tabelas(['flavio'],[])[-1]['data_horario']
        partida.marca_pontuacao(data_horario, '1') #marca ptos do ultimo lancamento
                                              #e passa para o prox jogador
        retorno = partida.marca_pontuacao(data_horario, '2')
        self.assertEqual( retorno, 5 )

    def test_077_marca_pontuacao_nok_jogador_ja_marcou_na_categoria(self):
        print("Caso de Teste 077 - Erro ao marcar pontuacao ja marcada"+
                " pelo jogador.")
        data_horario = tabela.obtem_tabelas(['flavio'],[])[-1]['data_horario']
        #voltando para o turno do flavio:
        partida.faz_lancamento(data_horario, []) 
        partida.marca_pontuacao(data_horario, 'abacate')
        #turno do flavio(ja marcou chance em outro teste):
        partida.faz_lancamento(data_horario, []) 
        retorno = partida.marca_pontuacao(data_horario, 'chance')
        self.assertEqual( retorno, 6 )
        
    def test_078_pausa_partida_nok_partida_pausada(self):
        print("Caso de Teste 078 - Erro ao pausar uma partida pausada.")
        data_horario = tabela.obtem_tabelas(['eleanor'],[])[-1]['data_horario']
        retorno = partida.pausa_partida( data_horario )
        self.assertEqual( retorno, 2 )

    def test_079_pausa_partida_nok_partida_encerrada(self):
        print("Caso de Teste 079 - Erro ao pausar uma partida encerrada.")
        data_horario = tabela.obtem_tabelas(['hugo'],[])[-1]['data_horario']
        retorno = partida.pausa_partida( data_horario )
        self.assertEqual( retorno, 3 )

    def test_080_partida_desiste_ok(self):
        print("Caso de Teste 080 - Desistir da partida com sucesso.")
        data_horario = tabela.obtem_tabelas(['flavio'],[])[-1]['data_horario']
        retorno = partida.desiste(data_horario, 'julia')
        self.assertEqual( retorno, 0 )

    def test_081_partida_desiste_nok_partida_inexistente(self):
        print("Caso de Teste 081 - Erro ao pausar uma partida inexistente.")
        retorno = partida.desiste("11:01:00:10:21:41", 'flavio')
        self.assertEqual( retorno, 1 )

    def test_082_partida_desiste_ok_partida_pausada(self):
        print("Caso de Teste 082 - Erro ao pausar uma partida pausada.")
        data_horario = tabela.obtem_tabelas(['eleanor'],[])[-1]['data_horario']
        retorno = partida.desiste(data_horario, 'eleanor')
        self.assertEqual( retorno, 2 )

    def test_083_partida_desiste_nok_partida_encerrada(self):
        print("Caso de Teste 083 - Erro ao pausar uma partida encerrada.")
        data_horario = tabela.obtem_tabelas(['hugo'],[])[-1]['data_horario']
        retorno = partida.desiste( data_horario, 'hugo' )
        self.assertEqual( retorno, 3 )

        
    def test_084_continua_partida_ok(self):
        print("Caso de Teste 084 - Continua partida com sucesso.")
        data_horario = tabela.obtem_tabelas(['eleanor'],[])[-1]['data_horario']
        retorno = partida.continua_partida( data_horario )
        self.assertEqual( retorno, 0 )

    def test_085_continua_partida_nok_partida_inexistente(self):
        print("Caso de Teste 085 - Erro ao continuar uma partida inexistente.")
        retorno = partida.continua_partida( "11:01:00:10:21:41" )
        self.assertEqual( retorno, 1 )

    def test_086_continua_partida_nok_partida_encerrada(self):
        print("Caso de Teste 086 - Erro ao continuar uma partida encerrada.")
        data_horario = tabela.obtem_tabelas(['hugo'],[])[-1]['data_horario']
        retorno = partida.continua_partida( data_horario )
        self.assertEqual( retorno, 3 )

    def test_087_obtem_info_ok_data_horario_correto(self):
        print("Caso de Teste 087 - Obtem info com data_horario correto.")
        data_horario = tabela.obtem_tabelas(['flavio'],[])[-1]['data_horario']
        info_partida_flavio = partida.obtem_info_partida([data_horario], [])[0]
        assertEqual(info_partida_flavio['data_horario'], data_horario)

    def test_088_obtem_info_ok_status_correto(self):
        print("Caso de Teste 088 - Obtem info com status correto.")
        data_horario = tabela.obtem_tabelas(['flavio'],[])[-1]['data_horario']
        info_partida_flavio = partida.obtem_info_partida([data_horario], [])[0]
        assertEqual(info_partida_flavio['status'], 'andamento')

    def test_089_obtem_info_ok_turno_correto(self):
        print("Caso de Teste 089 - Obtem info com turno_atual correto.")
        data_horario = tabela.obtem_tabelas(['flavio'],[])[-1]['data_horario']
        info_partida_flavio = partida.obtem_info_partida([data_horario], [])[0]
        assertEqual(info_partida_flavio['turno_atual'], 4)

    def test_090_obtem_info_ok_jogador_da_vez_correto(self):
        print("Caso de Teste 090 - Obtem info com jogador_da_vez correto.")
        data_horario = tabela.obtem_tabelas(['flavio'],[])[-1]['data_horario']
        info_partida_flavio = partida.obtem_info_partida([data_horario], [])[0]
        assertEqual(info_partida_flavio['jogador_da_vez'], 'flavio')

    def test_091_obtem_info_ok_tentativas_correto(self):
        print("Caso de Teste 091 - Obtem info com tentativas restantes correto.")
        data_horario = tabela.obtem_tabelas(['flavio'],[])[-1]['data_horario']
        info_partida_flavio = partida.obtem_info_partida([data_horario], [])[0]
        assertEqual(info_partida_flavio['tentativas'], 2)

    def test_092_obtem_info_ok_jogadores_correto(self):
        #considerando que jogadores desistentes continuam registrados
        print("Caso de Teste 092 - Obtem info com jogadores corretos.")
        data_horario = tabela.obtem_tabelas(['flavio'],[])[-1]['data_horario']
        info_partida_flavio = partida.obtem_info_partida([data_horario], [])[0]

        jogadores_cadastrados = set( jogadores
                for jogador in ['flavio', 'julia', 'lucas'] )

        jogadores_partida = set(jogadores 
                for jogador in info_partida_flavio['jogadores'] )


        assertEqual(jogadores_partida, jogadores_cadastrados)

unittest.main()
