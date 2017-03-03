#! /usr/local/bin/python3
# -*- coding: utf-8 -*-

import os
import stat
import sys

from diario import Diario


symlink = "/usr/local/bin/diario"

# Verifica se esiste già un symlink per il programma
# Se non esiste lo crea
if not os.path.exists(symlink):
    # Crea il symlink
    sorgente = os.path.abspath(__file__)
    os.symlink(sorgente, symlink)

    # Rende il file python eseguibile (spero)
    st = os.stat(sorgente)
    os.chmod(sorgente, st.st_mode | stat.S_IEXEC)

    # Informa l'utente che da questo momento in poi può
    # utilizzare il symlink per lanciare il programma
    print("Creato un symlink al programma su {}".format(symlink))
    print("Da questo momento in poi puoi richiamare")
    print("il programma semplicemente utilizzando il comando:")
    print("")
    print("diario <tag1> [<tag2> <tag3> ...]")

diario = Diario()

# Salta il primo elemento dell'array
# che tanto è il nome del programma stesso
argomenti = sys.argv[1:]
if len(argomenti) > 0:
    # Se è stato passato almeno un tag, crea un nuovo file
    diario.crea(None, *argomenti)
else:
    # Altrimenti tenta di aprire l'ultimo file
    if not diario.apri_ultimo_file():
        print("Utilizzo: diario <tag1> [<tag2> <tag3> ...]".format(sys.argv[0]))
        quit(0)
