#####################################################
#
#  Script para numerar os testes em ordem.
#  Le a ordem dos testes no arquivo ordem.txt.
#  Escreve os testes numerados no arquivo testes.py  
#  na raiz do projeto.                               
#  So testei no linux, mas escrevi para funcionar no 
#  windows tambem. Testar no windows quando possivel.
#
#####################################################


import os

base = os.path.dirname(__file__)
output = open(os.path.join( base, os.pardir, 'testes.py'), 'w')

output.write( "import unittest\n" )
output.write( "from entidades import *\n" )
output.write( "from funcionalidades import *\n" )
output.write("\nclass Test(unittest.TestCase):\n")

i = 0
testes = open(os.path.join(base, 'ordem.txt'), 'r')
for teste in testes:
    teste = open(os.path.join(base, teste.strip()), 'r')
    for linha in teste:
        if "unittest" not in linha:
            if "def test" in linha:
                    i += 1
            linha = linha.replace("AAA", "%03d" % i)
            output.write(linha)
    teste.close()
output.write("unittest.main()\n")
output.close()
