# Caro diario

Un programma in miniatura scritto in Python per gestire i vostri appunti 
e per organizzare i pensieri.

## A cosa serve il programma

Avevo bisogno di un programmino scemo che mi permettesse da riga di 
comando di creare dei file 
di testo con i miei pensieri ed i miei appunti, catalogandoli per data e 
magari aggiungendo dei tag per 
poterli ritrovare facilmente in seguito.
Questo programma serve proprio a questo scopo.


## Disclaimer

A me il programma funziona senza dare problemi. Se però nel vostro caso 
dovesse mandarvi in crash 
il computer, cancellare cartelle o files sensibili o fare danni di 
qualsiasi genere beh... sappiate che io
non me ne assumo nessuna responsabilità. Se scegliete di provare il mio 
programma vi assumete ogni responsabilità.

## Installazione 

Scaricate il programma in una cartella di vostro gradimento. Il 
programma non ha dipendenze esterne, basta 
una qualsiasi versione di Python a partire dalla 3.3 in su (perlomeno 
credo).

Se avete Mac OS X, Linux oppure un sistema operativo Unix vi consiglio 
di creare un symlink sul vostro computer. 
Dal vostro terminale digitate il comando:

~~~~sh
ln -s <percorso al file __main__.py> /usr/local/bin/diario
~~~~

Ad esempio nel mio specifico caso questo comando diventa:

~~~~sh
ln -s ~/Documents/Progetti/Python/caro-diario/__main__.py /usr/local/bin/diario
~~~~

Se vi stancate del programma e decidete di voler cancellare il symlink, 
il comando da terminale per cancellarlo è:

~~~~sh
unlink /usr/local/bin/diario
~~~~

## Configurazione

Dopo il primo avvio del programma, nella vostra home directory vi 
troverete un file di configurazione in formato JSON 
chiamato `~/.diario-config.json. Occhio che il file è nascosto.
Se lo aprirete con un'editor di testo vedrete questi parametri, 
modificabili:

~~~~json
{
    "application": "nano",
    "extension": "md",
    "last_opened": "<percorso all'ultimo file aperto dal programma>",
    "path": "~/diario"
}
~~~~

* il parametro "application" consente di indicare l'editor di testo da lanciare per modificare l'entry
* il parametro "extension" indica l'estensione che dovrà avere il file creato
* il parametro "last_opened" viene gestito internamente e ricorda al programma il percorso all'ultimo file creato
* il percorso "path" consente di indicare il percorso nel quale verrà creata la struttura con i files e le directories

## Utilizzo da terminale

Per creare una nuova entry nel vostro diario digitate il comando:

~~~~sh
diario <tag1> [<tag2> <tag3> ...]
~~~~

Per modificare l'ultima entry che avete creato, digitate il comando 
senza parametri:

~~~~sh
diario
~~~~

Buon divertimento!
