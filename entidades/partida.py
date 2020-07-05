#######################################################################
# MODULO PARTIDA
#
#  Centraliza as ações relacionadas ao andamento de uma partida fazendo
#  a comunicação entre os diversos módulos envolvidos. Cada partida 
#  possui um atributo identificador “data_horario”, trata-se do tipo 
#  datetime do python, indicando a data e horário em que foi criada. 
#   Uma partida pode ter status “andamento”, “pausada” ou “encerrada”.
#  Somente uma partida poderá estar em andamento ao mesmo tempo. As 
#  partidas são armazenadas no banco de dados apenas para registrar um
#  histórico. Portanto, não é possível recuperar uma partida pausada 
#  pelo banco de dados, para isso, é necessário salvar o estado da 
#  partida em um arquivo XML.
#---------------------------v0.1.0: 25/05/2020-------------------------
#  Por: Daniel Menezes
#  Criado mocking para tabela.cria_tabela
#---------------------------v0.2.0: 27/05/2020-------------------------
#  Por: Daniel Menezes
#  Modificada inicia_partida. Agora se recusa a iniciar uma partida
#  caso já haja uma partida em andamento. Passando nos novos testes.
#---------------------------v0.3.0: 27/05/2020-------------------------
#  Por: Daniel Menezes
#  Implementada faz_lancamento. Passando nos testes.
#---------------------------v0.4.0: 28/05/2020-------------------------
#  Por: Daniel Menezes
#  Implementada marca_pontuacao usando mock. Passando nos testes.
#  Mocks criados: 
#    -tabela.insere_pontuacao 
#    -tabela.obtem_tabelas
#---------------------------v0.4.1: 28/05/2020------------------------
#  Por: Daniel Menezes
#  Removido import indevido de jogador.
#---------------------------v0.4.2: 28/05/2020------------------------
#  Por: Daniel Menezes
#  Adicionado marca_pontuacao em __all__.
#---------------------------v0.5.0: 28/05/2020------------------------
#  Por: Daniel Menezes
#  Criado mock de tabela.registra_desistencia
#  Implementada desiste. Passando nos testes.
#---------------------------v0.5.1: 29/05/2020------------------------
#  Por: Daniel Menezes
#  Consertado bug em que desiste removia o jogador da partida antes de
#  passar o turno. Agora ela passa o turno e depois remove o jogador.
#  O bug ocorria porque achar o proximo jogador depende do jogador do
#  turno atual.
#---------------------------v0.6.0: 29/05/2020------------------------
#  Por: Daniel Menezes
#  Implementada parcialmente salva_partida passando nos testes.
#  A função salva os dados da partida mas não salva as tabelas ainda.
#  Passando nos testes.
#---------------------------v0.6.1: 01/06/2020------------------------
#  Por: Daniel Menezes
#  Implementada parcialmente continua_partida. A função carrega os
#   dados do módulo partida mas ainda não carrega os dados do módulo
#   tabela e nem do combincação
#---------------------------v0.7.0: 02/06/2020------------------------
#  Por: Daniel Menezes
#  Implementada para_partida.
#---------------------------v0.7.1: 02/06/2020------------------------
#  Por: Daniel Menezes
#  Removidos todos os mocks.
#  salva_partida e continua_partida salvam e inicializam as tabelas
#######################################################################

from datetime import datetime
from random import shuffle
from os.path import isdir, join
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, Comment
from xml.dom import minidom

from entidades import tabela
from entidades.jogador import valida_jogador, insere as insere_jogador, atualiza_info as atualiza_jogador
from funcionalidades import banco_de_dados
from funcionalidades import combinacao


__all__ = ['inicia_partida', 'faz_lancamento', 'marca_pontuacao', 'desiste',
        'obtem_partidas', 'salva_partida', 'continua_partida', 'para_partida',
           'obtem_info_partida']


partida_atual = {}


def _proximo_jogador():
    index = partida_atual['jogadores'].index(partida_atual['jogador_da_vez'])
    index = (index + 1) % len(partida_atual['jogadores'])
    return partida_atual['jogadores'][index]

def _partida_deve_acabar():
    tabelas = tabela.obtem_tabelas([],[partida_atual['data_horario']])

    todos_desistiram = False
    if all(tabela_jogador['desistencia'] for tabela_jogador in tabelas):
        todos_desistiram = True
    else:
        todas_as_tabelas_preenchidas = False
        jogadores_nao_desistentes = [tabela_jogador for tabela_jogador \
                in tabelas if not tabela_jogador['desistencia']]
        pontuacoes = []
        for tabela_jogador in jogadores_nao_desistentes:
            for pontos_por_cat in tabela_jogador['pontos_por_categoria']:
                pontuacoes.append(pontos_por_cat)
        if all(pts['pontuacao'] != None for pts in pontuacoes ):
            todas_as_tabelas_preenchidas = True

    return todos_desistiram or todas_as_tabelas_preenchidas

def _altera_status_bd(status):
    sql = """UPDATE Partida
             SET status = %s
             WHERE data_horario = %s"""
    banco = banco_de_dados.abre_acesso()
    banco['cursor'].execute(sql, (status, partida_atual['data_horario']))
    banco_de_dados.fecha_acesso(banco)
    return

def _ha_partida_em_andamento():
    return (partida_atual and partida_atual['status'] == 'andamento')

def _passa_turno():
    partida_atual['jogador_da_vez'] = _proximo_jogador()
    partida_atual['turno'] += 1
    partida_atual['tentativas'] = 3
    return

def _preenche_element_tree_partida_atual(elem_partida):
    for key, value in partida_atual.items():
        if key in ('salva', 'status'):
            continue

        sub_elem = SubElement(elem_partida, key)
        if key == 'jogadores':
            for nome_jogador in value:
                elem_nome = SubElement(sub_elem, 'nome')
                elem_nome.text = nome_jogador
        elif key == 'combinacao':
            if value:
                for dado in value:
                    elem_dado = SubElement(sub_elem, 'dado')
                    elem_dado.text = str(dado)
        elif key == 'pts_combinacao':
            if value:
                for categoria in value:
                    elem_categoria = SubElement(sub_elem, 'categoria')
                    elem_categoria_nome = SubElement(elem_categoria, 'nome')
                    elem_categoria_pontuacao = SubElement(elem_categoria,
                            'pontuacao')
                    elem_categoria_nome.text = categoria['nome']
                    elem_categoria_pontuacao.text = str(categoria['pontuacao'])
        else:
            sub_elem.text = str(value)
    return

def _preenche_element_tree_tabelas(elem_partida):
    tabelas = tabela.obtem_tabelas([], [partida_atual['data_horario']])
    elem_tabelas = SubElement(elem_partida, 'tabelas')
    for dict_tabela in tabelas:
        elem_tabela = SubElement(elem_tabelas, 'tabela')
        for k, v in dict_tabela.items():
            if k in ('data_horario', 'colocacao', 'pontuacao_total'):
                continue
            elem_atributo = SubElement(elem_tabela, k)
            if k == 'pontos_por_categoria':
                for categoria in v:
                    elem_categoria = SubElement(elem_atributo, 'categoria')
                    nome = SubElement(elem_categoria, 'nome') 
                    nome.text = categoria['nome']
                    pontuacao = SubElement(elem_categoria, 'pontuacao')
                    pontuacao.text = str(categoria['pontuacao'])
            else:
                elem_atributo.text = str(v)
                

def _carrega_dados_partida_atual(root):
    partida_atual.clear()
    data_horario_string = root.find('data_horario').text
    partida_atual['data_horario'] = datetime.strptime(data_horario_string,
            "%Y-%m-%d %H:%M:%S") 

    partida_atual['combinacao'] = list()
    for dado in root.find('combinacao').findall('dado'):
        partida_atual['combinacao'].append(int(dado.text))
    if partida_atual['combinacao']:
        combinacao.inicializa_combinacao(partida_atual['combinacao'])

    pts = partida_atual['pts_combinacao'] = list()
    for categoria in root.find('pts_combinacao').findall('categoria'):
        pts.append( {'nome': categoria.find('nome').text,
                     'pontuacao': int(categoria.find('pontuacao').text) })
   
    jogs = partida_atual['jogadores'] = list()
    for jogador in root.find('jogadores').findall('nome'):
        jogs.append(jogador.text)

    partida_atual['turno'] = int(root.find('turno').text)
    partida_atual['tentativas'] = int(root.find('tentativas').text)
    partida_atual['jogador_da_vez'] = root.find('jogador_da_vez').text
    partida_atual['status'] = 'andamento'
    partida_atual['salva'] = True
    return

def _carrega_dados_tabelas(root):
    for tabela_jogador in root.find('tabelas').findall('tabela'):
        nome_jogador = tabela_jogador.find('nome_jogador').text
        insere_jogador(nome_jogador)
        tabela.remove(nome_jogador, partida_atual['data_horario'])
        tabela.cria_tabela(nome_jogador, partida_atual['data_horario'])

        categorias = tabela_jogador.find('pontos_por_categoria')
        for categoria in categorias.findall('categoria'):
            categ_pontuacao = categoria.find('pontuacao').text
            if categ_pontuacao != 'None':
                categ_pontuacao = int(categ_pontuacao)
                categ_nome = categoria.find('nome').text
                tabela.insere_pontuacao(nome_jogador,
                                        partida_atual['data_horario'],
                                        categ_nome,
                                        categ_pontuacao)
    return



#################################################################
# Cria uma nova partida e associa tabelas para os seus jogadores.
#
# nomes: lista de nomes dos jogadores participantes.
#
# retorna data_horario da partida criada em caso de sucesso
# ou retorna 1 caso um dos jogadores passados não exista.
# ou retorna 2 caso já haja uma partida em andamento.
#################################################################
def inicia_partida(nomes):
    if _ha_partida_em_andamento():
        return 2
    if any(not valida_jogador(jogador) for jogador in nomes):
        return 1

    data_horario = datetime.now().replace(microsecond=0)
    banco = banco_de_dados.abre_acesso()
    sql_partida = """INSERT INTO Partida VALUES (%s, %s)"""
    banco['cursor'].execute(sql_partida, (data_horario, 'andamento'))
    banco_de_dados.fecha_acesso(banco)

    for jogador in nomes:
        cod_retorno = tabela.cria_tabela(jogador, data_horario) 

    shuffle(nomes)
    partida_atual['data_horario'] = data_horario
    partida_atual['combinacao'] = None
    partida_atual['pts_combinacao'] = None
    partida_atual['turno'] = 1
    partida_atual['tentativas'] = 3
    partida_atual['jogadores'] = nomes
    partida_atual['jogador_da_vez'] = nomes[0]
    partida_atual['status'] = 'andamento'
    partida_atual['salva'] = False

    return data_horario 


#######################################################################
#  Para a partida em andamento. O status da partida será alterado para
#   'pausada' caso esteja salva ou 'encerrada' caso não esteja salva.
#
#   Esta função NÃO se encarrega de salvar a partida em andamento. Para
#    isso deve-se utilizar a função salva_partida.
#
#  A partida continua carregada na memória após chamar esta função para
#   a interface de usuário poder continuar acessando as suas informações
#   por meio da obtem_info_partida(). A partida só sai da memória quando
#   o módulo é recarregado ou quando uma nova partida se inicia.
#
#  Retorna 0 em caso de sucesso.
#   ou retorna 1 caso não haja partida em andamento.
#######################################################################
def para_partida():
    if not _ha_partida_em_andamento():
        return 1
    status = 'pausada' if partida_atual['salva'] else 'encerrada' 
    partida_atual['status'] = status
    _altera_status_bd(status)
    tabelas = tabela.obtem_tabelas([],[partida_atual['data_horario']])
    for tab_jog in tabelas:
        if status == 'encerrada' and not tab_jog['desistencia']:
            atualiza_jogador(tab_jog['nome_jogador'],
                    tab_jog['pontuacao_total'])
    return 0


############################################################################
#  Gera um novo lançamento para o jogador do turno na partida em andamento.
#  
#  dados_escolhidos: lista com os índices (inteiros no intervalo [0,4])
#   dos dados a terem seus valores mantidos
#   ou lista vazia para rolar todos os dados
#
#  Retorna 0 em caso de sucesso
#   ou retorna 1 caso não haja partida em andamento
#   ou retorna 2 caso um dos índices em dados_escolhidos não seja válido
#   ou retorna 3 caso dados_escolhidos não seja uma lista vazia no primeiro
#    lançamento do turno atual.
#   ou retorna 4 caso o jogador do turno atual já tenha esgotado o número 
#    de tentativas.
#
############################################################################
def faz_lancamento(dados_escolhidos):
    if not _ha_partida_em_andamento():
        return 1
    if any(d not in range(0,5) for d in dados_escolhidos):
        return 2
    if partida_atual['tentativas'] == 3 and dados_escolhidos:
        return 3
    if partida_atual['tentativas'] == 0:
        return 4

    comb = combinacao.gera_combinacao(dados_escolhidos)
    partida_atual['combinacao'] = comb['combinacao'] 
    partida_atual['pts_combinacao'] = comb['pontos']
    partida_atual['tentativas'] -= 1

    partida_atual['salva'] = False
    return 0

########################################################################
#
#  Atribui ao jogador do turno da partida atual os pontos do seu último
#   lançamento (do mesmo turno) na categoria escolhida e passa para o
#   próximo turno. Caso a última categoria disponível é marcada, a
#   partida é encerrada.  
#
#  categoria: nome da categoria escolhida
#
#  Retorna 0 em caso de sucesso
#   ou retorna 1 caso não haja partida em andamento
#   ou retorna 2 caso a categoria seja inválida
#   ou retorna 3 caso o jogador do turno ainda não tenha realizado
#     um lançamento no turno atual.
#   ou retorna 4 caso o jogador já tenha marcado pontos
#     na categoria escolhida nessa partida
#
########################################################################
def marca_pontuacao(categoria):
    if not _ha_partida_em_andamento():
        return 1
    if partida_atual['tentativas'] == 3:
        return 3

    for categ in partida_atual['pts_combinacao']:
        if categ['nome'] == categoria:
            pontos = categ['pontuacao']
            break
    else:
        return 2

    args = [partida_atual['jogador_da_vez'],
            partida_atual['data_horario'],
            categoria,
            pontos]
    ret_insere = tabela.insere_pontuacao(*args)

    if ret_insere == 4:
        return 4

    partida_atual['salva'] = False
    if _partida_deve_acabar():
        para_partida()
    else:
        _passa_turno()

    return 0

##############################################################################
# Retira um jogador da partida. Se todos os jogadores desistirem, a partida
#  acaba.
# Retorna 0 em caso de sucesso.
#  ou retorna 1 caso não haja partida em andamento
#  ou retorna 2 caso nome_jogador não seja o nome de nenhum jogador da partida
##############################################################################
def desiste(nome_jogador):
    if not _ha_partida_em_andamento():
        return 1
    if nome_jogador not in partida_atual['jogadores']:
        return 2
    
    if partida_atual['jogador_da_vez'] == nome_jogador:
        _passa_turno()

    partida_atual['jogadores'].remove(nome_jogador)
    tabela.registra_desistencia(nome_jogador, partida_atual['data_horario'])
    partida_atual['salva'] = False
    if _partida_deve_acabar():
        para_partida()
    return 0

############################################################################
# Gera uma lista de dicionários com as partidas registradas no histórico.
# 
# data_horario: data_horario da partida a buscar ou uma lista
#   com os data_horario das partidas a buscar. Se for uma lista vazia ou None,
#   busca partidas com qualquer data_horario.
# 
# status: status da partida a buscar ou uma lista com os status das partidas
#   a buscar. Se for uma lista vazia ou None, busca partidas com qualquer
#   status.
#
# Retorna uma lista de dicionários do tipo { ‘data_horario’, ‘status’ }.
#  ou retorna uma lista vazia caso não haja partida com os parâmetros passados.
#  ou retorna 1 caso um dos parâmetros seja inválido
############################################################################
def obtem_partidas(data_horario = [], status = []):
    if isinstance(data_horario, datetime):
        data_horario = [data_horario]
    if isinstance(status, str):
        status = [status]
    if not isinstance(data_horario, list) or not isinstance(status, list):
        return 1

    sqlBusca = """ SELECT * FROM Partida"""
    
    banco = banco_de_dados.abre_acesso()
    if data_horario:
        sqlBusca += ' WHERE data_horario in (%s{})'.format(
                                                (len(data_horario)-1)*',%s')
        if status:
            sqlBusca += ' AND status in (%s{})'.format((len(status)-1)*',%s')
        banco['cursor'].execute(sqlBusca, data_horario+status)
    elif status:
        sqlBusca += ' WHERE status in (%s{})'.format((len(status)-1)*',%s')
        banco['cursor'].execute(sqlBusca, status)
    else:
        banco['cursor'].execute(sqlBusca)
    resultado = [dictPartida for dictPartida in banco['cursor']]
    banco_de_dados.fecha_acesso(banco)
    return resultado

#############################################################
# Salva a partida em andamento em um arquivo XML.
#
#  path: caminho para a pasta onde o arquivo será criado. 
#
#  retorna 0 em caso de sucesso
#   ou retorna 1 caso não haja partida em andamento
#   ou retorna 2 caso o caminho não seja econtrado
#   ou retorna 3 caso haja erro de escrita.
#
#############################################################
def salva_partida(path):
    if not _ha_partida_em_andamento():
        return 1
    if not isdir(path):
        return 2
    
    elem_partida = Element('partida')
    _preenche_element_tree_partida_atual(elem_partida)
    _preenche_element_tree_tabelas(elem_partida) 

    rough_string = ElementTree.tostring(elem_partida, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    final_string = reparsed.toprettyxml(indent="  ")

    arquivo_nome = partida_atual['data_horario'].strftime('%Y%m%d%H%M%S')
    arquivo_nome += ".xml"
    try:
        with open(join(path,arquivo_nome), 'w') as xml_file:
            xml_file.write(final_string)
    except:
        return 3

    partida_atual['salva'] = True
    return 0

####################################################
# Carrega uma partida que foi salva anteriormente e 
#  a coloca em andamento.
#
# Hipótese: o arquivo xml é considerado
#  corretamente formado já que é produzido pela pró-
#  pria aplicação
#
# path: caminho para o arquivo xml.
# retorna 0 em caso de sucesso
#  ou retorna 1 caso não seja possível ler o arquivo
#
####################################################
def continua_partida(path):
    try:
        arq = open(path, "r")
    except:
        return 1

    tree = ElementTree.parse(arq)
    root = tree.getroot()
    arq.close()
    

    _carrega_dados_partida_atual(root)
    _carrega_dados_tabelas(root)

    if _partida_deve_acabar():
        _altera_status_bd('encerrada')
        partida_atual['status'] = 'encerrada'
    else:
        _altera_status_bd('andamento')
    return 0

##############################################################################
#
# Gera informações gerais sobre a partida atual.
# São por essas informações que a interface de usuário deve se guiar
# sobre as mudanças que ocorrem na partida.
#
# Retorna um dicionário do tipo:
#   {
#   “data_horario”,         #identificador
#   status”,               #status da partida
#   “combinacao”,     #lista com os valores dos 5 dados
#   “pts_combinacao”,      #lista com dicionários com as pontuações possíveis
#                           # (ver abaixo)
#
#   “turno” ,         #número do turno atual
#   “jogador_da_vez” ,      #nome do jogador da vez
#   “tentativas” ,          #número de tentativas restantes para lançamento
#   “jogadores” ,           #lista com os nomes dos jogadores participantes
#                               (jogadores desistentes não inclusos)
#   "salva"                 #diz se a partida foi salva desde a última ação
#                               (True/False)
# }
#
# “pts_combinacao”:
# [ { “nome”: <nome_da_categoria1>, “pontuacao”: <pontuacao_na_categoria_1> },
#   { “nome”: <nome_da_categoria2>, “pontuacao”: <pontuacao_na_categoria_2> },
#   { “nome”: <nome_da_categoria3>, “pontuacao”: <pontuacao_na_categoria_3> }
#  ... ]
#
#  Retorna 1 caso não haja uma partida carregada.
#
##############################################################################
def obtem_info_partida():
    if not partida_atual:
        return 1
    return partida_atual
