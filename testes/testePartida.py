import unittest
from entidades import tabela

class Test(unittest.TestCase):
##########################
#      TESTES PARTIDA:      
#      Daniel Menezes 
#      25/04/2020
##########################

    def test_AAA_inicia_partida_nok_jogador_nao_existente(self):
        print("Caso de Teste AAA - Inicia partida nao aceita jogador"+
            " inexistente.")
        retorno = partida.inicia_partida(["juan"])
        self.assertEqual( retorno , 1 )

    def test_AAA_obtem_info_artida_nok_sem_partida(self):
        print("Caso de Teste AAA - Erro em obtem info sem nenhuma"+
                " partida em andamento.")
        retorno = partida.obtem_info_partida()
        self.assertEqual(retorno, 1)

    def test_AAA_faz_lancamento_nok_partida_sem_partida(self):
        print("Caso de Teste AAA - Erro em fazer lancamento sem nenhuma"+
                " partida em andamento.")
        retorno = partida.faz_lancamento([1,2])
        self.assertEqual( retorno, 1 )
        
    def test_AAA_marca_pontuacao_nok_sem_partida(self):
        print("Caso de Teste AAA - Erro ao marcar pontuacao sem nenhuma"+
                " partida em andamento.")
        retorno = partida.marca_pontuacao('1')
        self.assertEqual( retorno, 1 )

    def test_AAA_para_partida_nok_sem_partida(self):
        print("Caso de Teste AAA - Erro ao encerrar partida sem nenhuma"+
                " partida em andamento.")
        retorno = partida.para_partida()
        self.assertEqual( retorno, 1 )

    def test_AAA_desiste_nok_sem_partida(self):
        print("Caso de Teste AAA - Erro desiste sem partida em andamento.")
        retorno = partida.desiste('flavio')
        self.assertEqual( retorno, 1 )

    def test_AAA_salva_partida_nok_sem_partida(self):
        print("Caso de Teste AAA - Erro salva_partida sem partida em"+
                " andamento.")
        dir_raiz = path.dirname(path.realpath(__file__))
        saves = path.join(dir_raiz, 'saves') 
        retorno = partida.salva_partida(saves)
        self.assertEqual(retorno, 1)

    def test_AAA_inicia_partida_ok_condicao_retorno(self):
        print("Caso de Teste AAA - Inicia partida com sucesso.")
        jogador.insere("flavio")
        jogador.insere("lucas")
        jogador.insere("julia")
        retorno = partida.inicia_partida(["flavio", "lucas", "julia"])
        self.assertIsInstance(retorno, datetime)
   
    def test_AAA_inicia_partida_ok_jogadores_corretos(self):
        print("Caso de Teste AAA - Obtem info com jogadores corretos.")
        jogadores = partida.obtem_info_partida()['jogadores']
        self.assertSetEqual(set(jogadores), set(['flavio', 'lucas', 'julia']))

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
        retorno = partida.marca_pontuacao('chance')
        self.assertEqual( retorno, 0 )

    def test_AAA_marca_pontuacao_ok_passou_o_turno(self):
        print("Caso de Teste AAA - Marca pontuacao passou o turno.")
        turno = partida.obtem_info_partida()['turno']
        self.assertEqual( turno, 2 )

    def test_AAA_marca_pontuacao_ok_restaura_tentativa(self):
        print("Caso de Teste AAA - Marca pontuacao proximo jogador tem 3"+
                " tentativas.")
        info = partida.obtem_info_partida()['tentativas']
        self.assertEqual( info, 3 )

    def test_AAA_desiste_ok_condicao_retorno(self):
        print("Caso de Teste AAA - Desiste com sucesso.")
        retorno = partida.desiste('julia')
        self.assertEqual( retorno, 0 )

    def test_AAA_desiste_ok_retira_jogador(self):
        print("Caso de Teste AAA - Desiste retira jogador da partida.")
        jogadores = partida.obtem_info_partida()['jogadores']
        self.assertNotIn( 'julia', jogadores )

    def test_AAA_desiste_nok_nome_invalido(self):
        print("Caso de Teste AAA - Erro desiste jogador invalido.")
        retorno = partida.desiste('julia')
        self.assertEqual( retorno, 2 )

    def test_AAA_marca_pontuacao_nok_jogador_ja_marcou_na_categoria(self):
        print("Caso de Teste AAA - Erro ao marcar pontuacao ja marcada"+
                " pelo jogador.")
        partida.faz_lancamento([]) 
        partida.marca_pontuacao('chance')
        partida.faz_lancamento([]) 
        partida.marca_pontuacao('chance')
        partida.faz_lancamento([])
        retorno = partida.marca_pontuacao('chance')
        self.assertEqual( retorno, 4 )

    def test_AAA_salva_partida_ok_condicao_retorno(self):
        print("Caso de Teste AAA - Salva partida sucesso.")
        dir_raiz = path.dirname(path.realpath(__file__))
        saves = path.join(dir_raiz, 'saves') 
        retorno = partida.salva_partida(saves)
        self.assertEqual(retorno, 0)

    def test_AAA_salva_partida_nok_path_invalido(self):
        print("Caso de Teste AAA - Erro salva_partida caminho não encontrado")
        dir_raiz = path.dirname(path.realpath(__file__))
        saves = path.join(dir_raiz, 'pasta_nao_existente') 
        retorno = partida.salva_partida(saves)
        self.assertEqual(retorno, 2)

    def test_AAA_para_partida_ok_condicao_retorno(self):
        print("Caso de Teste AAA - Encerra partida com sucesso.")
        retorno = partida.para_partida()
        self.assertEqual( retorno, 0 )

    def test_AAA_continua_partida_ok(self):
        print("Caso de Teste AAA - Continua partida com sucesso.")
        data_horario = partida.obtem_info_partida()['data_horario']
        data_horario = datetime.strftime(data_horario,'%Y%m%d%H%M%S') + '.xml'
        arq = path.join(path.realpath(path.dirname(__file__)),'saves',data_horario)
        retorno = partida.continua_partida(arq)
        self.assertEqual( retorno, 0 )

    def test_AAA_continua_partida_nok_arquivo_inexistente(self):
        print("Caso de Teste AAA - Continua partida Erro ao não encontrar o arquivo")
        retorno = partida.continua_partida('arquivo_nao_existente') 
        self.assertEqual( retorno, 1 )

    def test_AAA_obtem_info_partida_ok_condicao_retorno(self):
        print("Caso de Teste AAA - obtem_info_partida condição de retorno ok.")
        retorno = partida.obtem_info_partida()
        self.assertEqual(set(retorno.keys()), {'data_horario',
                                        'status',
                                        'combinacao',
                                        'pts_combinacao',
                                        'turno',
                                        'jogador_da_vez',
                                        'tentativas',
                                        'jogadores',
                                        'salva'})

    def test_AAA_obtem_partidas_ok_condicao_retorno(self):
        print("Caso de Teste AAA - obtem_partidas condicao de retorno ok")
        retorno = partida.obtem_partidas(status = 'andamento')
        data_horario = partida.obtem_info_partida()['data_horario']
        self.assertIn({'data_horario':data_horario, 'status':'andamento'},
                      retorno)

    def test_AAA_obtem_partidas_ok_condicao_retorno2(self):
        print("Caso de Teste AAA - obtem_partidas condicao de retorno ok"+
                " partida nao encontrada.")
        retorno = partida.obtem_partidas(datetime(2019,1,1,2,1,3))
        self.assertEqual(retorno, [])

    def test_AAA_obtem_partidas_nok_parametro_invalido(self):
        print("Caso de Teste AAA - obtem_partidas erro com parametro invalido")
        retorno = partida.obtem_partidas('parametro_invalido', [1])
        self.assertEqual( retorno, 1 )


unittest.main()
