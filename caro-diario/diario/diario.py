# -*- coding: utf-8 -*-

import os
import datetime

from .configurazione import Configurazione


class Diario:

    def __init__(self):
        """
        Inizializza la classe e crea il file
        con le impostazioni se necessario
        """

        self.config = Configurazione(".diario-config.json")

        # Prova ad impostare alcuni valori di default
        self.config.set_default("path", os.path.join(os.path.expanduser("~"), "diario"))
        self.config.set_default("application", "nano")
        self.config.set_default("extension", "md")
        self.config.set_default("last_opened", "")

        self.workdir = self.config.tag("path")

        # Crea la cartella iniziale se non esiste
        if not os.path.exists(self.workdir):
            os.mkdir(self.workdir)

    def _percorso(self, *args):
        """
        Partendo da un'elenco di parametri restituisce il
        percorso alla cartella costruita con la directory
        base (workdir) e con i parametri passati.

        Es: _percorso("tizio", "caio") --> ~/diario/tizio/caio
        """

        percorso = self.workdir
        for elemento in args:
            percorso = os.path.join(percorso, elemento)
        return percorso

    def _esiste(self, *args):
        """
        Restituisce un booleano per indicare se una cartella
        indicata dai parametri passati esiste
        """

        return os.path.exists(self._percorso(*args))

    def _crea_se_inesistente(self, *args):
        """
        Crea una cartella indicata dai parametri se questa
        non esiste già.

        Es: _crea("tizio", "caio") --> mkdir ~/diario/tizio/caio
        """

        if not self._esiste(*args):
            os.mkdir(self._percorso(*args))
            return False
        else:
            return True

    def _dict_da_data(self, p_data):
        """
        Partendo da un oggetto datetime restituisce
        un dizionario contenenti i parametri
        formattati ed organizzati proprio come servono
        a me
        """

        giorno = dict()
        giorno["anno"] = str(p_data.year)
        giorno["mese"] = str(p_data.month).zfill(2)
        giorno["giorno"] = str(p_data.day).zfill(2)
        giorno["ora"] = str(p_data.hour).zfill(2)
        giorno["minuto"] = str(p_data.minute).zfill(2)
        giorno["secondo"] = str(p_data.second).zfill(2)
        giorno["timestamp"] = str(p_data.timestamp())

        return giorno

    def _apri_editor(self, p_file):
        """
        Apre l'editor di testo indicato nel file JSON.
        Restituisce True se è stato impostato un editor
        """

        if self.config.tag("application") != "":
            os.system(self.config.tag("application") + " " + p_file)
            return True
        else:
            return False

    def _crea_template(self, p_data, p_tags):
        """
        Crea il modello che verrà scritto su file
        """
        righe = list()
        righe.append("----")
        righe.append("Title: ")
        righe.append("Date: {}-{}-{} {}:{}".format(p_data["anno"],
                                                   p_data["mese"],
                                                   p_data["giorno"],
                                                   p_data["ora"],
                                                   p_data["minuto"], ))
        righe.append("Tags: {}".format(", ".join(p_tags)))
        righe.append("----")
        righe.append("\n")

        return "\n".join(righe)

    def apri_ultimo_file(self):
        """
        Apre con l'editor di testo l'ultimo file
        modificato dal programma
        """

        return self._apri_editor(self.config.tag("last_opened"))

    def crea(self, p_data=None, *p_tags):
        """
        Crea la struttura delle cartelle necessaria
        ed il file
        """

        # Ripulisce e sistema i tags prima di utilizzarli
        p_tags = [tag.replace("_", "-").lower() for tag in p_tags]
        p_tags.sort()

        # Verifica se è stato passato il parametro data
        if not p_data:
            p_data = datetime.datetime.now()
        giorno = self._dict_da_data(p_data)

        # Verifica se esiste la sottocartella con l'anno
        self._crea_se_inesistente(self._percorso(giorno["anno"]))
        # Verifica se esiste la sottocartella con il mese
        self._crea_se_inesistente(self._percorso(giorno["anno"],
                                                 giorno["mese"]))
        # Verifica se esiste la sottocartella con il giorno
        self._crea_se_inesistente(self._percorso(giorno["anno"],
                                                 giorno["mese"],
                                                 giorno["giorno"]))

        # Prepara il nome del file che sarà scritto su disco
        proposto = "{}{}{}-{}".format(giorno["anno"][2:],
                                      giorno["mese"],
                                      giorno["giorno"],
                                      "-".join(p_tags))

        # Prova a controllare se esiste già un file con questo nome
        nomefile = "{}.{}".format(proposto, self.config.tag("extension"))
        if os.path.exists(nomefile):
            # Purtroppo esiste già, ed allora
            # prova a cambiare il nome al nuovo file
            indice = 1
            while True:
                nomefile = "{}-{}.{}".format(proposto,
                                             str(indice),
                                             self.config.tag("extension"))
                # Se non esiste lo usa
                if not os.path.exists(nomefile):
                    break
                else:
                    indice += 1

        # Ora si prepara a creare il file
        file_da_creare = self._percorso(giorno["anno"],
                                        giorno["mese"],
                                        giorno["giorno"],
                                        nomefile)

        # Scrive il file su disco
        f = open(file_da_creare, "w")
        f.write(self._crea_template(giorno, p_tags))
        f.close()

        # Apre l'editor con il file
        self._apri_editor(file_da_creare)

        # Salva la configurazione su disco con l'ultimo file creato
        self.config.tag("last_opened", file_da_creare)
        self.config.salva()
