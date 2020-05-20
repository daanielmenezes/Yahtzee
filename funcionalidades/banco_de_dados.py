########################################
#  MÓDULO BANCO
#  
#  Intermedeia o acesso ao banco de dados.
#  Assume usuário root com senha 'root'.
#
#------------v1.0.0-19/05/2020----------
#  Por: Daniel Menezes
#  Criadas as funções:
#    -abre_acesso()
#    -fecha_acesso()
#  Funcionando e passando nos testes
##########################################

import mysql.connector

__all__ = ["abre_acesso", "fecha_acesso" ]


##########################################################################
#  Abre uma conexão com o banco de dados
#  
#  Retorna um dicionario [ conexao, cursor ] que poderão ser usados para 
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
#  Retorna 0 em caso de sucesso
#  ou retorna 1 em caso de erro.
#  ou retorna 2 caso conexao ou cursor sejam invalidos
#########################################################
def fecha_acesso(conexao, cursor):
    if type(conexao) != mysql.connector.connection.MySQLConnection or\
       type(cursor) != mysql.connector.cursor.MySQLCursorBufferedDict:
           return 2
    try:
        cursor.close()
        conexao.close()
    except mysql.connector.Error as erro:
        return 1
    return 0
