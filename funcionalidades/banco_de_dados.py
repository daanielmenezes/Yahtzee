###########################################
#  MÓDULO BANCO
#  
#  Intermedeia o acesso ao banco de dados.
#  Assume usuário root com senha 'root'.
#
#------------v1.0.0-19/05/2020------------
#  Por: Daniel Menezes
#  Criadas as funções:
#    -abre_acesso()
#    -fecha_acesso()
#  Funcionando e passando nos testes
#
#
#------------v1.1.0-25/05/2020------------
#  Por: Daniel Menezes
#  
#  Funcionalidade de configuração inicial 
#  do banco de dados movido do script de
#  configuração para cá como uma função.
#
###########################################

import mysql.connector
from mysql.connector import errorcode

__all__ = [ "configura", "abre_acesso", "fecha_acesso" ]


tabelas = {}

tabelas['Partida'] = (
        """
        create table Partida (
            data_horario datetime default current_timestamp,
            status enum('andamento', 'encerrada', 'pausada') not null,
            primary key (data_horario)
        )
        """
        )

tabelas['Jogador'] = (
        """
        create table Jogador (
            nome varchar(255) not null,
            data_criacao date,
            pontuacao_total int,
            recorde int,
            ranking int,
            primary key (nome)
        )
        """
        )

tabelas['Jogador_Partida'] = (
        """
        create table Jogador_Partida(
            data_horario datetime,
            nome varchar(255) not null,
            primary key (data_horario, nome),
            foreign key (data_horario) references Partida(data_horario),
            foreign key (nome) references Jogador(nome)
        )
        """
        )

tabelas['Tabela'] = (
        """
        create table Tabela (
            data_horario datetime,
            nome_jogador varchar(255) not null,
            pontuacao_total int,
            colocacao int,
            desistencia bool,
            primary key (data_horario, nome_jogador),
            foreign key (data_horario) references Partida(data_horario),
            foreign key (nome_jogador) references Jogador(nome)
        )
        """
        )

tabelas['Tabela_Pontuacao'] = (
        """
        create table Tabela_Pontuacao (
            data_horario datetime,
            nome_jogador varchar(255),
            nome_categoria varchar(255),
            pontuacao int,
            primary key (data_horario, nome_jogador, nome_categoria),
            foreign key (data_horario) references Partida(data_horario),
            foreign key (nome_jogador) references Jogador(nome)
        )
        """
        )

def _cria_banco_de_dados(cursor):
    try:
        cursor.execute("DROP DATABASE IF EXISTS Yahtzee")
        cursor.execute("CREATE DATABASE Yahtzee")
        cursor.execute("USE Yahtzee")
        print("Criando banco de dados: ", end = '')
    except mysql.connector.Error as err:
        return ("Falha ao criar banco de dados: {}".format(err.msg))
    else:
        print("OK.")
        return 0

def _cria_tabelas(cursor):
    for tabela in tabelas:
        sql = tabelas[tabela]
        try:
            print("Criando tabela {}: ".format(tabela), end ='')
            cursor.execute(sql)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                return ("Tabela já existe: {}".format(err.msg))
            else:
                return ("Erro na criação da tabela {}: {}".format(
                                                       tabela, err.msg))
        else:
            print("OK.")
    return 0

##################################################################
#
#  Cria o banco de dados com todas as tabelas usadas na aplicação.
#  Caso o banco de dados já exista, ele é deletado e recriado.
#
#  Retorna 0 em caso de sucesso,
#  ou retorna uma string de erro.
#
##################################################################
def configura():
    try:
        banco = mysql.connector.connect(
                host = 'localhost',
                user = 'root',
                passwd = 'root'
            )
        cursor = banco.cursor()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            return "Erro: Acesso negado\n"
        else: 
            return "Erro ao conectar com o mysql: {}".format(err)
    else:
        retorno = _cria_banco_de_dados(cursor)
        if retorno:
            return retorno
        retorno = _cria_tabelas(cursor)
        if retorno:
            return retorno
        cursor.close()
        banco.close()
    return 0



##########################################################################
#  Abre uma conexão com o banco de dados
#  
#  Retorna um dicionario { 'conexao', 'cursor' } que poderão ser usados para 
#  executar comandos sql e deverão ser fechados pela função fecha_acesso
#  ou retorna 1 caso haja erro de conexão com o mysql.
#
#  Os cursores terão autocommit, buffer e dictionary ativados para 
#  facilitar o manuseio.
##########################################################################
def abre_acesso():
    try:
        conexao = mysql.connector.connect(
                host = 'localhost',
                user = 'root',
                passwd = 'root',
                database = 'Yahtzee',
                autocommit = True,
                buffered = True
            )
        cursor = conexao.cursor( dictionary = True )
    except mysql.connector.Error as erro:
        return 1
    return {'conexao':conexao, 'cursor':cursor}



#########################################################
#  Fecha a conexão com o banco e o cursor
#  
#  acesso: um dicionario do tipo { 'conexao', 'cursor' }
#  conexao: uma conexão criada pela abre_acesso
#  cursor: um cursor criado pela abre_acesso
#
#  Retorna 0 em caso de sucesso
#  ou retorna 1 em caso de erro.
#  ou retorna 2 caso conexao ou cursor sejam invalidos
#########################################################
def fecha_acesso(acesso):
    conexao = acesso['conexao']
    cursor = acesso['cursor']
    if type(conexao) != mysql.connector.connection.MySQLConnection or\
       type(cursor) != mysql.connector.cursor.MySQLCursorBufferedDict:
           return 2
    try:
        cursor.close()
        conexao.close()
    except mysql.connector.Error as erro:
        return 1
    return 0

