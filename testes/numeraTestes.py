#####################################################
#
#  Script para numerar os testes em ordem.
#  Le a ordem dos testes no arquivo ordem.txt.
#  Escreve os testes numerados no arquivo testes.py  
#  na raiz do projeto.                               
#
#####################################################


import os

base = os.path.dirname(__file__)
output = open(os.path.join( base, os.pardir, 'testes.py'), 'w')

output.write( "import mysql.connector\n" )
output.write( "import unittest\n" )
output.write( "from os import path\n" )
output.write( "from datetime import datetime\n" )
output.write( "from entidades import *\n" )
output.write( "from funcionalidades import *\n" )

output.write("""
def limpa_tabelas():
    tabelas = ['Tabela_Pontuacao', 'Tabela', 'Jogador', 'Partida']
    banco = banco_de_dados.abre_acesso()
    sqlDelete = "delete from "
    for tab in tabelas:
        banco['cursor'].execute(sqlDelete+tab)
    banco_de_dados.fecha_acesso(banco)
""")

output.write("\nclass Test(unittest.TestCase):\n")


i = 0
testes = open(os.path.join(base, 'ordem.txt'), 'r')
excluir = ["unittest", "import"]
for teste in testes:
    teste = open(os.path.join(base, teste.strip()), 'r')
    for linha in teste:
        if all( x not in linha for x in excluir ):
            if "def test" in linha:
                    i += 1
            linha = linha.replace("AAA", "%03d" % i)
            output.write(linha)
    teste.close()
output.write("unittest.main(exit=False)\n")
output.write("limpa_tabelas()")

output.close()
