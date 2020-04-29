import sys
import fileinput

if len(sys.argv) < 2:
    sys.exit("uso: numeraTestes.py <arquivo1> <arquivo2> ...")

print( "import unittest" )
print( "from entidades import *" )
print( "from funcionalidades import *" )
print("\nclass Test(unittest.TestCase):")
i = 0
for linha in fileinput.input():
    if "unittest" not in linha:
        if "def test" in linha:
                i += 1
        linha = linha.replace("AAA", "%03d" % i)
        print( linha , end='')

print( "unittest.main()" )
