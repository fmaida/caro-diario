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
        self.config.set_default_se_inesistente("path", os.path.join(os.path.expanduser("~"), "diario"))
        self.config.set_default_se_inesistente("application", "nano")
        self.config.set_default_se_inesistente("extension", "md")
        self.config.set_default_se_inesistente("last_opened", "")

        self.workdir = self.config.tag("path")

        # Crea la cartella iniziale se non esiste
        if not os.path.exists(self.workdir):
            os.mkdir(self.workdir)

    def _percorso(self, *args):
        percorso = self.workdir
        for elemento in args:
            percorso = os.path.join(percorso, elemento)
        return percorso

    def _esiste(self, *args):
        return os.path.exists(self._percorso(*args))

    def _crea_se_inesistente(self, *args):
        if not self._esiste(*args):
            os.mkdir(self._percorso(*args))
            return False
        else:
            return True

    def _dict_da_data(self, p_data):
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
        if self.config.tag("application") != "":
            os.system(self.config.tag("application") + " " + p_file)
            return True
        else:
            return False

    def apri_ultimo_file(self):
        return self._apri_editor(self.config.tag("last_opened"))

    def crea(self, p_data=None, *p_tags):

        if not p_data:
            p_data = datetime.datetime.now()
        giorno = self._dict_da_data(p_data)

        nomefile = "{}{}{}{}{}{}-{}.{}".format(giorno["anno"],
                                               giorno["mese"],
                                               giorno["giorno"],
                                               giorno["ora"],
                                               giorno["minuto"],
                                               giorno["secondo"],
                                               "-".join(p_tags),
                                               self.config.tag("extension"))

        # Elimina le prime due cifre dell'anno ("2017" -> "17")
        nomefile = nomefile[2:]

        # Verifica se esiste la sottocartella con l'anno
        self._crea_se_inesistente(self._percorso(giorno["anno"]))
        # Verifica se esiste la sottocartella con il mese
        self._crea_se_inesistente(self._percorso(giorno["anno"],
                                                 giorno["mese"]))
        # Verifica se esiste la sottocartella con il giorno
        self._crea_se_inesistente(self._percorso(giorno["anno"],
                                                 giorno["mese"],
                                                 giorno["giorno"]))

        # Ora si prepara a creare il file
        file_da_creare = self._percorso(giorno["anno"],
                                        giorno["mese"],
                                        giorno["giorno"],
                                        nomefile)

        # Si prepara a creare il file
        righe = list()
        righe.append("----")
        righe.append("Title: ")
        righe.append("Date: {}-{}-{} {}:{}".format(giorno["anno"],
                                                   giorno["mese"],
                                                   giorno["giorno"],
                                                   giorno["ora"],
                                                   giorno["minuto"], ))
        righe.append("Tags: {}".format(", ".join(p_tags)))
        righe.append("----")
        righe.append("\n")

        # Scrive il file su disco
        f = open(file_da_creare, "w")
        f.write("\n".join(righe))
        f.close()

        # Apre l'editor con il file
        self._apri_editor(file_da_creare)

        # Salva la configurazione su disco con l'ultimo file creato
        self.config.tag("last_opened", file_da_creare)
        self.config.salva()