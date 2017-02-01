#! /usr/local/bin/python3

import sys

from diario import Diario


diario = Diario()
argomenti = sys.argv[1:]
if len(argomenti) > 0:
    diario.crea(None, *argomenti)
else:
    if not diario.apri_ultimo_file():
        print("Utilizzo: diario <tag1> [<tag2> <tag3> ...]".format(sys.argv[0]))
        quit(0)
