import os
import json


class Configurazione:

    def __init__(self, p_file=None, p_percorso=None):
        """
        Inizializza la classe
        """

        if not p_percorso:
            p_percorso = os.path.expanduser("~")
        if not p_file:
            p_file = ".config.json"

        self.basedir = p_percorso
        self.file = os.path.join(self.basedir, p_file)

        # Controlla l'esistenza di un file di configurazione
        if os.path.exists(self.file):
            with open(self.file, "r") as f:
                self.config = json.load(f)
        else:
            self.config = {"path": self.configdir, "application": "nano", "extension": "md", "last_opened": ""}
            self.salva()

    def set_default_se_inesistente(self, p_tag, p_valore_default):
        """
        Se non esiste un valore per la chiave specificata,
        crea la chiave con il valore di default suggerito
        """

        # Prova ad impostare alcuni valori di default
        try:
            if self.config[p_tag] == "":
                self.config[p_tag] = p_valore_default
        except KeyError:
            self.config[p_tag] = p_valore_default

    def tag(self, p_nome_tag, p_valore=None):
        """
        Imposta o restituisce la chiave richiesta
        """

        if p_valore:
            self.config[p_nome_tag] = p_valore
        return self.config[p_nome_tag]

    def salva(self):
        """
        Salva il file di configurazione su disco
        """

        with open(self.file, "w") as f:
            f.write(json.dumps(self.config, indent=4, sort_keys=True))
