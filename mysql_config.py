##########################################
#  Script para a criação do banco de dados
##########################################

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
            pontucao_total int,
            colocacao int,
            desistencia bool,
            primary key (nome)
        )
        """
        )

tabelas['Categoria'] = (
        """
        create table Categoria (
            nome varchar(255) not null,
            descricao varchar(255),
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
            pontucao_total int,
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
            foreign key (nome_jogador) references Jogador(nome),
            foreign key (nome_categoria) references Categoria(nome) 
        )
        """
        )

def cria_banco_de_dados(cursor):
    try:
        cursor.execute("CREATE DATABASE Yahtzee")
    except mysql.connector.Error as err:
        print("Falha ao criar banco de dados: {}".format(err))
        exit(1)


usuario = input('Usuário MySql: ')
senha = input('Senha: ')

try:
    banco = mysql.connector.connect(
            host = 'localhost',
            user = usuario,
            passwd = senha
        )
    cursor = banco.cursor()
    cursor.execute("USE Yahtzee")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Credenciais inválidas ou sem privilégios")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        cria_banco_de_dados(cursor)
        cursor.execute("USE Yahtzee")
        print("Banco de dados criado")
    else: 
        print(err)
        exit(1)

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

cursor.close()
banco.close()
