###################################################
#
#    Script para a criação do banco de dados
# -----------------v1.0.0-------------------
#    Por: Daniel Menezes
#    Criadas as cofigurações das tabelas:
#       - Partida
#       - Jogador
#       - Categoria
#       - Jogador_Partida
#       - Tabela
#       - Tabela_Pontuacao
#       
#    Criada a verificação de banco de dados 
#    já existente.
#  
#    Criado o loop para execução de cada
#    comando de criação de tabelas.
#  
#    Criado input das credencias do mysql
#  
# -----------------v1.0.1-------------------
#    Por: Daniel Menezes
#    
#    Removida a configuração da tabela Categoria,
#    pois é hardcoded no módulo Categoria
#
#    Input de credenciais removido, sera assumido
#    usuário 'root' com senha 'root'.
# ------------------v1.1.0------------------
#    Por: Daniel Menezes
#    
#    Caso já exista um banco de dados Yahtzee,
#    o banco de dados será deletado e recriado
#    para garantir que terá todas as configurações
#    corretas.
#
#    Criação de tabelas separada em uma função 
###################################################


import mysql.connector
from mysql.connector import errorcode


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

def cria_banco_de_dados(cursor):
    try:
        print("Criando Banco de Dados Yahtzee: ", end = '')
        cursor.execute("DROP DATABASE IF EXISTS Yahtzee")
        cursor.execute("CREATE DATABASE Yahtzee")
        cursor.execute("USE Yahtzee")
    except mysql.connector.Error as err:
        print("Falha ao criar banco de dados: {}".format(err))
        exit(1)
    else:
        print("OK.")
    return

def cria_tabelas(cursor):
    for tabela in tabelas:
        sql = tabelas[tabela]
        try:
            print("Criando tabela {}: ".format(tabela), end='')
            cursor.execute(sql)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("já existe.")
            else:
                print(err.msg)
        else:
            print("OK.")
    return

try:
    banco = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            passwd = 'root'
        )
    cursor = banco.cursor()
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Credenciais inválidas ou sem privilégios")
    else: 
        print(err)
        exit(1)
else:
    cria_banco_de_dados(cursor)
    cria_tabelas(cursor)
    cursor.close()
    banco.close()
