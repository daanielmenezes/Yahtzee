import unittest
from entidades import tabela

class Test(unittest.TestCase):
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

    def test_AAA_inicia_partida_nok_jogador_nao_existente(self):
        print("Caso de Teste AAA - Inicia partida nao aceita jogador"+
            " inexistente.")
        retorno = partida.inicia_partida(["juan"])
        self.assertEqual( retorno , 1 )

    def test_AAA_faz_lancamento_nok_partida_inexistente(self):
        print("Caso de Teste AAA - Erro em fazer lancamento em partida"+
                " inexistente.")
        retorno = partida.faz_lancamento([1,2])
        self.assertEqual( retorno, 1 )
        
    def test_AAA_marca_pontuacao_nok_sem_partida(self):
        print("Caso de Teste AAA - Erro ao marcar pontuacao sem nenhuma"+
                " partida em andamento.")
        retorno = partida.marca_pontuacao('1')
        self.assertEqual( retorno, 1 )

    def test_AAA_inicia_partida_ok(self):
        print("Caso de Teste AAA - Inicia partida com sucesso.")
        jogador.insere("flavio")
        jogador.insere("lucas")
        jogador.insere("julia")
        retorno = partida.inicia_partida(["flavio", "lucas", "julia"])
        self.assertIsInstance(retorno, datetime)
        self.partidaFlavio = retorno
   
    def test_AAA_inicia_partida_nok_partida_em_andamento(self):
        print("Caso de Teste AAA - Inicia partida recusa iniciar partida"+
                " com outra partida em andamento.")
        retorno = partida.inicia_partida(["lucas"])
        self.assertEqual( retorno , 2 )

    def test_AAA_faz_lancamento_nok_indice_invalido(self):
        print("Caso de Teste AAA - Erro em fazer lancamento com indices de "+
                "dados invalidos.")
        retorno = partida.faz_lancamento([-1,5])
        self.assertEqual(retorno, 2)

    def test_AAA_faz_lancamento_nok_indice_primeiro_lancamento_indice(self):
        print("Caso de Teste AAA - Erro em fazer primeiro lancamento do turno"+
                " com indices de dados escolhidos.")
        retorno = partida.faz_lancamento([1,3])
        self.assertEqual(retorno, 3)

    def test_AAA_marca_pontuacao_nok_jogador_do_turno_nao_lancou(self):
        print("Caso de Teste AAA - Erro ao marcar pontuacao sem lancar"+
                " dados no turno.")
        retorno = partida.marca_pontuacao('2')
        self.assertEqual( retorno, 3 )

    def test_AAA_faz_lancamento_ok(self):
        print("Caso de Teste AAA - Faz lancamento em partida com sucesso.")
        retorno = partida.faz_lancamento([])
        self.assertEqual(retorno, 0)

    def test_AAA_faz_lancamento_ok_reduziu_tentativas(self):
        print("Caso de Teste AAA - Faz lancamento reduz o numero de"+
                " tentativas.")
        info = partida.obtem_info_partida()
        self.assertEqual( info['tentativas'], 2 )

    def test_AAA_faz_lancamento_nok_tentativas_esgotadas(self):
        print("Caso de Teste AAA - Faz lancamento erro quando o jogador já"+
                " esgotou suas tentativas.")
        partida.faz_lancamento([])
        partida.faz_lancamento([])
        retorno = partida.faz_lancamento([])
        self.assertEqual(retorno, 4)

    def test_AAA_faz_lancamento_ok_combinacao_gerada_com_sucesso(self):
        print("Caso de Teste AAA - Faz lancamento combinação gerada.")
        info = partida.obtem_info_partida()
        combinacao = info['combinacao']
        dados = ([ dadoNum for dadoNum in combinacao if dadoNum in range(1,7)])
        #confere que tem 5 numeros [1,6] na lista retornada
        self.assertEqual( len(dados), 5 )  
       
    def test_AAA_marca_pontuacao_nok_categoria_invalida(self):
        print("Caso de Teste AAA - Erro ao marcar pontuacao invalida.")
        partida.faz_lancamento([])
        retorno = partida.marca_pontuacao('abacate')
        self.assertEqual( retorno, 2 )

    def test_AAA_marca_pontuacao_ok_sucesso(self):
        print("Caso de Teste AAA - Marca pontuacao em uma categoria com"+
                " sucesso.")
        self.jogadorAnterior = partida.obtem_info_partida()['jogador_da_vez']
        retorno = partida.marca_pontuacao('chance')
        self.assertEqual( retorno, 0 )

    def test_AAA_marca_pontuacao_ok_passou_o_turno(self):
        print("Caso de Teste AAA - Marca pontuacao passou o turno.")
        retorno = partida.obtem_info_partida()['turno']
        self.assertEqual( retorno, 2 )

    def test_AAA_marca_pontuacao_ok_restaura_tentativa(self):
        print("Caso de Teste AAA - Marca pontuacao proximo jogador tem 3"+
                " tentativas.")
        info = partida.obtem_info_partida()['tentativas']
        self.assertEqual( info, 3 )

    def test_AAA_marca_pontuacao_nok_jogador_ja_marcou_na_categoria(self):
        print("Caso de Teste AAA - Erro ao marcar pontuacao ja marcada"+
                " pelo jogador.")
        partida.faz_lancamento([]) 
        retorno = partida.marca_pontuacao('chance')
        self.assertEqual( retorno, 4 )
        
#################

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

    def test_AAA_marca_pontuacao_ok_pontos_na_tabela(self):
        print("Caso de Teste AAA - Marca Pontuacao Insere pontuacao na"+
                " tabela com sucesso")
        pts_cat = tabela.obtem_tabelas(['flavio'],[])[-1]['pontos_por_categoria']
        chance = next(cat for cat in pts_cat if cat['nome'] == 'chance')[0] 
        self.assertGreater( chance['pontuacao'], 0 )



    def test_AAA_pausa_partida_nok_partida_inexistente(self):
        print("Caso de Teste AAA - Erro ao pausar uma partida inexistente.")
        retorno = partida.pausa_partida(datetime(2000, 1, 11, 12, 21, 41, 0))
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
        retorno = partida.desiste(datetime(2000, 1, 11, 12, 21, 11, 0), 'flavio')
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
        info_partida = partida.obtem_info_partida([datetime(2000, 1, 11, 12, 21, 11, 0)], [])[0]
        assertEqual(info_partida, [] )

unittest.main()
