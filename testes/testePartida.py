import unittest

class Testmock(unittest.TestCase):
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

    def test_AAA_inicia_partida_ok(self):
        print("Caso de Teste AAA - Inicia partida com sucesso.")
        jogador.insere("flavio")
        jogador.insere("lucas")
        jogador.insere("julia")
        retorno = partida.inicia_partida(["flavio", "lucas", "julia"])
        self.assertIs( type(retorno), str )
   
    def test_AAA_inicia_partida_nok_jogador_nao_existente(self):
        print("Caso de Teste AAA - Inicia partida nao aceita jogador"+
            " inexistente.")
        retorno = partida.inicia_partida(["juan"])
        self.assertEqual( retorno , 1 )

    def test_AAA_faz_lancamento_ok(self):
        print("Caso de Teste AAA - Faz lancamento em nova partida sucesso.")
        jogador.insere("eleanor")
        data_horario = partida.inicia_partida(["eleanor"])
        retorno = partida.faz_lancamento(data_horario,[])
        self.assertEqual(retorno,0)

    def test_AAA_faz_lancamento_ok_combinacao_gerada_com_sucesso(self):
        print("Caso de Teste AAA - Faz lancamento combinação gerada.")
        data_horario = tabela.obtem_tabelas(['eleanor'],[])[-1]['data_horario']
        info = partida.obtem_info_partida([data_horario], [])
        combinacao = info['combinacao_atual']
        dados = ([ dadoNum for dadoNum in combinacao if 1 <= dadoNum <= 6])
        #confere que tem 5 numeros [1,6] na lista retornada
        self.assertTrue( len(dados) == 5 )  
        
    def test_AAA_faz_lancamento_nok_partida_inexistente(self):
        print("Caso de Teste AAA - Erro em fazer lancamento em partida"+
                " inexistente.")
        retorno = partida.faz_lancamento("11:01:00:12:23:11",[])
        self.assertEqual( retorno, 1 )

    def test_AAA_pausa_partida_ok(self):
        print("Caso de Teste AAA - Partida pausada com sucesso.")
        data_horario = tabela.obtem_tabelas(['eleanor'],[])[-1]['data_horario']
        retorno = partida.pausa_partida(data_horario) 
        assertEqual( retorno , 0 )

    def test_AAA_pausa_partida_ok_status_pausada(self):
        print("Caso de Teste AAA - Partida pausada com status 'pausada'.")
        data_horario = tabela.obtem_tabelas(['eleanor'],[])[-1]['data_horario']
        status = partida.obtem_info_partida([data_horario], [])['status']
        assertEqual(status, 'pausada') 

    def test_AAA_faz_lancamento_nok_partida_pausada(self):
        print("Caso de Teste AAA - Erro em fazer lancamento em partida"+
                " pausada.")
        data_horario = tabela.obtem_tabelas(['eleanor'],[])[-1]['data_horario']
        retorno = partida.faz_lancamento(data_horario,[])
        self.assertEqual( retorno, 2 )

    def test_AAA_marca_pontuacao_ok_sucesso(self):
        print("Caso de Teste AAA - Marca pontuacao em uma categoria com"+
                " sucesso.")
        data_horario = tabela.obtem_tabelas(['flavio'],[])[-1]['data_horario']
        partida.faz_lancamento(data_horario,[])
        retorno = partida.marca_pontuacao(data_horario, 'chance')
        #marca pontos pro flavio e passa pro lucas
        self.assertEqual( retorno, 0 )

    def test_AAA_marca_pontuacao_ok_pontos_na_tabela(self):
        print("Caso de Teste AAA - Insere pontuacao na tabela com sucesso")
        pts_cat = tabela.obtem_tabelas(['flavio'],[])[-1]['pontos_por_categoria']
        chance = next(cat for cat in pts_cat if cat['nome'] == 'chance')[0] 
        self.assertGreater( chance['pontuacao'], 0 )

    def test_AAA_faz_lancamento_nok_partida_encerrada(self):
        print("Caso de Teste AAA - Erro em fazer lancamento em partida"+
                " encerrada.")
        jogador.insere("hugo")
        data_horario = partida.inicia_partida(["hugo"])
        for categoria in categoria.obtem_nomes():
            #encerra uma partida marcando todas as categorias
            partida.faz_lancamento(data_horario,[])
            partida.marca_pontuacao(data_horario, categoria['nome'])
        retorno = partida.faz_lancamento(data_horario,[])
        self.assertEqual(retorno, 3)

    def test_AAA_faz_lancamento_nok_indice_invalido(self):
        print("Caso de Teste AAA - Erro em fazer lancamento com indices de "+
                "dados invalidos.")
        data_horario = tabela.obtem_tabelas(['flavio'],[])[-1]['data_horario']
        retorno = partida.faz_lancamento(data_horario, [-1,5])
        #turno do lucas
        self.assertEqual(retorno, 4)

    def test_AAA_faz_lancamento_nok_indice_primeiro_lancamento_indice(self):
        print("Caso de Teste AAA - Erro em fazer primeiro lancamento do turno"+
                " com indices de dados escolhidos.")
        data_horario = tabela.obtem_tabelas(['flavio'],[])[-1]['data_horario']
        retorno = partida.faz_lancamento(data_horario, [1,3])
        #turno do lucas
        self.assertEqual(retorno, 5)

    def test_AAA_marca_pontuacao_nok_partida_inexistente(self):
        print("Caso de Teste AAA - Erro ao marcar pontuacao em partida"+
                " inexistente.")
        retorno = partida.marca_pontuacao("11:01:00:10:21:41", 'chance')
        self.assertEqual( retorno, 1 )

    def test_AAA_marca_pontuacao_nok_partida_pausada(self):
        print("Caso de Teste AAA - Erro ao marcar pontuacao em partida "+
                "pausada.")
        data_horario = tabela.obtem_tabelas(['eleanor'],[])[-1]['data_horario']
        retorno = partida.marca_pontuacao(data_horario, 'chance')
        self.assertEqual( retorno, 2 )

    def test_AAA_marca_pontuacao_nok_partida_encerrada(self):
        print("Caso de Teste AAA - Erro ao marcar pontuacao em partida"+
                " encerrada.")
        data_horario = tabela.obtem_tabelas(['hugo'],[])[-1]['data_horario']
        retorno = partida.marca_pontuacao(data_horario, 'chance')
        self.assertEqual( retorno, 3 )

    def test_AAA_marca_pontuacao_nok_categoria_invalida(self):
        print("Caso de Teste AAA - Erro ao marcar pontuacao invalida.")
        data_horario = tabela.obtem_tabelas(['flavio'],[])[-1]['data_horario']
        partida.faz_lancamento(data_horario, [])
        #turno do lucas
        retorno = partida.marca_pontuacao(data_horario, 'abacate')
        self.assertEqual( retorno, 4 )

    def test_AAA_marca_pontuacao_nok_jogador_do_turno_nao_lancou(self):
        print("Caso de Teste AAA - Erro ao marcar pontuacao sem lancar"+
                " dados no turno.")
        data_horario = tabela.obtem_tabelas(['flavio'],[])[-1]['data_horario']
        partida.marca_pontuacao(data_horario, '1') #marca ptos do lucas
                                                   #e passa para a julia
        retorno = partida.marca_pontuacao(data_horario, '2')
        #turno da julia
        self.assertEqual( retorno, 5 )

    def test_AAA_marca_pontuacao_nok_jogador_ja_marcou_na_categoria(self):
        print("Caso de Teste AAA - Erro ao marcar pontuacao ja marcada"+
                " pelo jogador.")
        data_horario = tabela.obtem_tabelas(['flavio'],[])[-1]['data_horario']
        #voltando para o turno do flavio:
        partida.faz_lancamento(data_horario, []) 
        partida.marca_pontuacao(data_horario, 'chance')
        #turno do flavio(ja marcou chance em outro teste):
        partida.faz_lancamento(data_horario, []) 
        retorno = partida.marca_pontuacao(data_horario, 'chance')
        self.assertEqual( retorno, 6 )
        
    def test_AAA_pausa_partida_nok_partida_inexistente(self):
        print("Caso de Teste AAA - Erro ao pausar uma partida inexistente.")
        retorno = partida.pausa_partida("11:01:00:10:21:41")
        self.assertEqual(retorno, 1)

    def test_AAA_pausa_partida_nok_partida_pausada(self):
        print("Caso de Teste AAA - Erro ao pausar uma partida pausada.")
        data_horario = tabela.obtem_tabelas(['eleanor'],[])[-1]['data_horario']
        retorno = partida.pausa_partida( data_horario )
        self.assertEqual( retorno, 2 )

    def test_AAA_pausa_partida_nok_partida_encerrada(self):
        print("Caso de Teste AAA - Erro ao pausar uma partida encerrada.")
        data_horario = tabela.obtem_tabelas(['hugo'],[])[-1]['data_horario']
        retorno = partida.pausa_partida( data_horario )
        self.assertEqual( retorno, 3 )

    def test_AAA_partida_desiste_ok(self):
        print("Caso de Teste AAA - Desistir da partida com sucesso.")
        data_horario = tabela.obtem_tabelas(['flavio'],[])[-1]['data_horario']
        retorno = partida.desiste(data_horario, 'julia')
        self.assertEqual( retorno, 0 )

    def test_AAA_partida_desiste_nok_partida_inexistente(self):
        print("Caso de Teste AAA - Erro ao desistir em uma partida inexistente.")
        retorno = partida.desiste("11:01:00:10:21:41", 'flavio')
        self.assertEqual( retorno, 1 )

    def test_AAA_partida_desiste_nok_partida_pausada(self):
        print("Caso de Teste AAA - Erro ao desistir em uma partida pausada.")
        data_horario = tabela.obtem_tabelas(['eleanor'],[])[-1]['data_horario']
        retorno = partida.desiste(data_horario, 'eleanor')
        self.assertEqual( retorno, 2 )

    def test_AAA_partida_desiste_nok_partida_encerrada(self):
        print("Caso de Teste AAA - Erro ao desistir em uma partida encerrada.")
        data_horario = tabela.obtem_tabelas(['hugo'],[])[-1]['data_horario']
        retorno = partida.desiste( data_horario, 'hugo' )
        self.assertEqual( retorno, 3 )

    def test_AAA_partida_desiste_nok_nome_invalido(self):
        print("Caso de Teste AAA - Erro ao desistir partida de um jogador"+
                " invalido.")
        data_horario = tabela.obtem_tabelas(['lucas'],[])[-1]['data_horario']
        retorno = partida.desiste( data_horario, 'juan' )
        self.assertEqual( retorno, 4 )
        
    def test_AAA_partida_desiste_nok_jogador_ja_desistiu(self):
        print("Caso de Teste AAA - Erro ao desistir partida de um jogador "+
                "ja desistente.")
        data_horario = tabela.obtem_tabelas(['flavio'],[])[-1]['data_horario']
        retorno = partida.desiste( data_horario, 'julia' )
        self.assertEqual( retorno, 5 )

    def test_AAA_continua_partida_ok(self):
        print("Caso de Teste AAA - Continua partida com sucesso.")
        data_horario = tabela.obtem_tabelas(['eleanor'],[])[-1]['data_horario']
        retorno = partida.continua_partida( data_horario )
        self.assertEqual( retorno, 0 )

    def test_AAA_continua_partida_nok_partida_inexistente(self):
        print("Caso de Teste AAA - Erro ao continuar uma partida inexistente.")
        retorno = partida.continua_partida( "11:01:00:10:21:41" )
        self.assertEqual( retorno, 1 )

    def test_AAA_continua_partida_nok_partida_encerrada(self):
        print("Caso de Teste AAA - Erro ao continuar uma partida encerrada.")
        data_horario = tabela.obtem_tabelas(['hugo'],[])[-1]['data_horario']
        retorno = partida.continua_partida( data_horario )
        self.assertEqual( retorno, 3 )

    def test_AAA_obtem_info_partida_ok_data_horario_correto(self):
        print("Caso de Teste AAA - Obtem info com data_horario correto.")
        data_horario = tabela.obtem_tabelas(['flavio'],[])[-1]['data_horario']
        info_partida_flavio = partida.obtem_info_partida([data_horario], [])[0]
        assertEqual(info_partida_flavio['data_horario'], data_horario)

    def test_AAA_obtem_info_partida_ok_status_correto(self):
        print("Caso de Teste AAA - Obtem info com status correto.")
        data_horario = tabela.obtem_tabelas(['flavio'],[])[-1]['data_horario']
        info_partida_flavio = partida.obtem_info_partida([data_horario], [])[0]
        assertEqual(info_partida_flavio['status'], 'andamento')

    def test_AAA_obtem_info_partida_ok_turno_correto(self):
        print("Caso de Teste AAA - Obtem info com turno_atual correto.")
        data_horario = tabela.obtem_tabelas(['flavio'],[])[-1]['data_horario']
        info_partida_flavio = partida.obtem_info_partida([data_horario], [])[0]
        assertEqual(info_partida_flavio['turno_atual'], 4)

    def test_AAA_obtem_info_partida_ok_jogador_da_vez_correto(self):
        print("Caso de Teste AAA - Obtem info com jogador_da_vez correto.")
        data_horario = tabela.obtem_tabelas(['flavio'],[])[-1]['data_horario']
        info_partida_flavio = partida.obtem_info_partida([data_horario], [])[0]
        assertEqual(info_partida_flavio['jogador_da_vez'], 'flavio')

    def test_AAA_obtem_info_partida_ok_tentativas_correto(self):
        print("Caso de Teste AAA - Obtem info com tentativas restantes correto.")
        data_horario = tabela.obtem_tabelas(['flavio'],[])[-1]['data_horario']
        info_partida_flavio = partida.obtem_info_partida([data_horario], [])[0]
        assertEqual(info_partida_flavio['tentativas'], 2)

    def test_AAA_obtem_info_partida_ok_jogadores_correto(self):
        #considerando que jogadores desistentes continuam registrados
        print("Caso de Teste AAA - Obtem info com jogadores corretos.")
        data_horario = tabela.obtem_tabelas(['flavio'],[])[-1]['data_horario']
        info_partida_flavio = partida.obtem_info_partida([data_horario], [])[0]

        jogadores_cadastrados = set( jogadores
                for jogador in ['flavio', 'julia', 'lucas'] )

        jogadores_partida = set(jogadores 
                for jogador in info_partida_flavio['jogadores'] )


        assertEqual(jogadores_partida, jogadores_cadastrados)

    def test_AAA_obtem_info_partida_nok_lista_vazia(self):
        print("Caso de Teste AAA - Obtem info retorna lista vazia se nao achar.")
        info_partida = partida.obtem_info_partida(["11:01:00:10:21:41"], [])[0]
        assertEqual(info_partida, [] )

unittest.main()
