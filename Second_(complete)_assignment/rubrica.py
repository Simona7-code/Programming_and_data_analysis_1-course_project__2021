# Assegnamento 2 aa 2021-22 622AA modulo programmazione 9 crediti
# Simona Sette 544298 s.sette@studenti.unipi.it 3516774933
import os
from threading import Condition
from queue import Queue
import random as r
import logging

# Impostazione dei messaggi log con conseguente creazione di un file di log e un file txt
Log_Format = "[%(levelname)s - %(asctime)s - %(threadName)s --> %(message)s]"
logging.basicConfig(filename="logfile.log", filemode="w", format=Log_Format, level=logging.DEBUG)
file_handler = logging.FileHandler("log.txt")
file_handler.setFormatter(logging.Formatter(Log_Format))
logger = logging.getLogger().addHandler(file_handler)


class Rubrica:

    # ASCII 255 -> Non-breaking space
    SERIALIZATION_SEPARATOR = chr(255)

    # Costruttore: crea una rubrica vuota rappresentata come dizionario di contatti vuoto
    def __init__(self):
        # Crea una nuova rubrica vuota
        self.rub = {}
        self.rubLock = Condition()
        self.queue = Queue(maxsize=3)

    # Serializza una rubrica attraverso una stringa con opportuna codifica (a scelta dello studente)
    def __str__(self):

        # Acquisizione del lock
        self.rubLock.acquire()
        logging.info("Inizio processo di stampa della rubrica")
        # Creo variabile records a cui verranno concatenate le stringhe prodotte all'esecuzione dell'if-else
        records = "RUBRICA\nCONTATTO : NUMERO\n\n"

        # Se il dizionario è vuoto
        if len(self.rub) == 0:
            # Concateno a records la stringa definita nel return
            self.rubLock.release()
            logging.info("Rubrica corrente vuota.")
            return "Spiacenti,la tua rubrica è ancora vuota! Perchè non aggiungi un numero?"

        # Se il dizionario non è vuoto, per ogni chiave del dizionario
        for nomeCognomeKey in self.rub:
            nomeCognome = ' '.join(nomeCognomeKey)
            numeroTelefono = str(self.rub[nomeCognomeKey])
            # Definisco stampa di ogni contatto:
            linea = nomeCognome + ':' + numeroTelefono
            # Assegno il precedente record a records, seguito da un newline
            records += linea + "\n"

        # Rilascio del lock
        self.rubLock.release()
        logging.info("stampa della rubrica corrente: {}".format(records))
        # Restituisco variabile records che conterrà i singoli dati dei contatti seguiti dal newline
        return records

    # Stabilisce se due rubriche contengono esattamente le stesse chiavi con gli stessi dati
    def __eq__(self, r2):
        # Se le due rubriche sono equivalenti restituisce true, false altrimenti
        return self.rub == r2.rub

    # Crea una nuova rubrica unendone due (elimina i duplicati) e la restituisce come risultato
    # Se ci sono contatti con la stessa chiave nelle due rubriche ne riporta uno solo
    def __add__(self, r2):

        # Acquisizione del lock
        self.rubLock.acquire()
        # Assegno a varibili r1 e r2 le rubriche da sommare
        r1 = self.rub
        r2 = r2.rub
        retVal = Rubrica()

        # Assegno a r3 un dizionario che contiene la somma del contenuto dei dizionari (precedentemente convertiti in tipo lista)
        retVal.rub = dict(list(r1.items()) + list(r2.items()))
        # Rilascio del lock
        self.rubLock.release()
        return retVal

    # Carica da file una rubrica eliminando il precedente contenuto di self
    def load(self, nomefile):

        # Acquisizione del lock
        self.rubLock.acquire()
        # Se il file non esiste evoco un eccezione che comunichi all'utente l'informazione.
        if not os.path.exists(nomefile):
            raise Exception("Spiacenti, il file risulta inesistente!")

        # Sovrascrivo il corrente contenuto di self
        self.rub = {}

        # Apro il file in lettura e assegno le singole righe a lineList
        with open(nomefile, "r") as inline:
            lineList = inline.read().splitlines()

            # Per ogni riga contenuta in aline faccio uno split della riga sul carattere ":"
            for line in lineList:
                lineSplit = line.split(':')
                # Ricostruisco la tupla da usare come chiave nel dizionario
                nameSplit = lineSplit[0].split(self.SERIALIZATION_SEPARATOR)
                nomeCognomeKey = (nameSplit[0], nameSplit[1])
                # Assegno iterativamente alla rubrica le coppie chiavi,valore
                # La chiave è una tupla contenente le stringhe di nome e cognome; il valore è un intero
                self.rub[nomeCognomeKey] = int(lineSplit[1])  # TODO Gestire come stringhe per supportare prefissi internazionali e numeri che cominciano per 0
        # Rilascio del lock
        self.rubLock.release()

    # Inserisce un nuovo contatto con chiave (nome,cognome) restituisce "True" se l'inserimento è andato a buon fine e "False" altrimenti (es chiave replicata) -- case insensitive
    def inserisci(self, nome, cognome, dati):

        # Acquisizione del lock
        self.rubLock.acquire()
        logging.info(f'Inizio processo di inserimento contatto {nome} {cognome} dalla rubrica.')
        # Definisco la futura possibile key che potrebbe essere inserita
        nomeCognomeKeyProposta = ((str(nome)), (str(cognome)))
        nomeLow = (str(nome)).lower()
        cognomeLow = (str(cognome)).lower()
        # Definisco una versione lowercase della possibile futura key
        nomeCognomeKeyLow = (nomeLow, cognomeLow)

        # Se dizionario è vuoto inserisce primo record
        if not bool(self.rub):
            self.rub[nomeCognomeKeyProposta] = int(dati)
            self.rubLock.release()
            logging.info(f' Primo Contatto della rubrica inserito con successo: {nome} {cognome}')
            return True
        # Se dizionario non è vuoto
        else:
            # Inizializzo variabile contatore a 0
            Conta = 0
            # Per ogni chiave contenuta nel dizionario
            for nomeCognomeKey in self.rub.keys():
                # Converto le stringhe contenute nella chiave in lowercase e costuisco una versione lowercase della tupla originale
                CurrentKeyLowTuple = tuple([element.lower() for element in nomeCognomeKey])
                # Se la tupla di chiavi contenute nel dizionario (in versione lowercase) è equivalente a nomeCognomeKeyLow
                if CurrentKeyLowTuple == nomeCognomeKeyLow:
                    # Vuol dire che sono la stessa chiave e quindi incremento Conta ed interrompe l'iterazione
                    Conta += 1
                    break

            # Se Conta è maggiore di 0 è stata trovata una chiave non idonea all'inserimento e restituisce False
            if Conta > 0:
                # Rilascio del lock
                self.rubLock.release()
                logging.info(f' Contatto {nome} {cognome}  non inserito in rubrica in quanto già presente')
                return False
            # Se la chiave è idonea inserisce il contatto nella rubrica e restituisce true
            else:
                self.rub[nomeCognomeKeyProposta] = int(dati)
                # Rilascio del lock
                self.rubLock.release()
                logging.info(f'Contatto {nome} {cognome} inserito in rubrica con successo')
                return True

    # Modifica i dati relativi al contatto con chiave (nome,cognome)sostituendole con "newdati"
    # Restituisce "True" se la modifica è stata effettuata e "False" altrimenti (es: la chiave non è presente )
    def modifica(self, nome, cognome, newdati):

        # Acquisizione del lock
        self.rubLock.acquire()
        logging.info(f'Inizio processo di modifica contatto {nome} {cognome} dalla rubrica.')
        nomeLower = (str(nome)).lower()
        cognomeLower = (str(cognome)).lower()
        # Definisco una versione lowercase della key da cercare
        KeySearchLower = (nomeLower, cognomeLower)
        # Inizializzo variabile contatore a 0
        Trovato = 0

        # Per ogni chiave contenuta nel dizionario
        for nomeCognomeKey in self.rub:
            # Converto le stringhe contenute nella chiave in lowercase e costuisco una versione lowercase della tupla originale
            CurrentKeyLowTuple = tuple([element.lower() for element in nomeCognomeKey])
            # Se la tupla di chiavi contenute nel dizionario (in versione lowercase) è equivalente a KeySearchLower
            if CurrentKeyLowTuple == KeySearchLower:
                # Vuol dire che sono la stessa chiave e quindi incremento trovato ed interrompe l'iterazione
                Trovato += 1
                break

        # Se la chiave di ricerca ha ottenuto riscontro nel dizionario modifica i dati del contatto nella rubrica e restituisce true
        if Trovato > 0:
            self.rub[nomeCognomeKey] = int(newdati)
            # Rilascio del lock
            self.rubLock.release()
            logging.info(f'Il contatto {nome} {cognome} modificato con successo con il seguente numero {newdati}')
            return True
        # Se la chiave ricercata non esiste restiuisce False
        else:
            # Rilascio del lock
            self.rubLock.release()
            logging.info(f'Il contatto {nome} {cognome} non può essere modificato in quanto non esistente in rubrica corrente.')
            return False

    # Il contatto con chiave (nome,cognome) esiste lo elimina insieme ai dati relativi e restituisce True -- altrimenti restituisce False
    def cancella(self, nome, cognome):

        # Acquisizione del lock
        self.rubLock.acquire()
        logging.info(f'Inizio processo di eliminazione contatto {nome} {cognome} dalla rubrica.')
        nomeLower = (str(nome)).lower()
        cognomeLower = (str(cognome)).lower()
        # Definisco una versione lowercase della key da cercare
        KeySearchLower = (nomeLower, cognomeLower)
        # Inizializzo variabile contatore a 0
        Trovato = 0

        # Per ogni chiave contenuta nel dizionario
        for nomeCognomeKey in self.rub:
            # Converto le stringhe contenute nella chiave in lowercase e costuisco una versione lowercase della tupla originale
            CurrentKeyLowTuple = tuple([element.lower() for element in nomeCognomeKey])
            # Se la tupla di chiavi contenute nel dizionario (in versione lowercase) è equivalente a KeySearchLower
            if CurrentKeyLowTuple == KeySearchLower:
                # Vuol dire che sono la stessa chiave e quindi incremento trovato ed interrompe l'iterazione
                Trovato += 1
                break

        # Se la chiave di ricerca ha ottenuto riscontro nel dizionario cancella il contatto dalla rubrica e restituisce true
        if Trovato > 0:
            del self.rub[nomeCognomeKey]
            # Rilascio del lock
            self.rubLock.release()
            logging.info(f'Il contatto {nome} {cognome} è stato eliminato con successo.')
            return True
        # Se la chiave cercata non esiste restituisce False
        else:
            # Rilascio del lock
            self.rubLock.release()
            logging.info(f'Il contatto {nome} {cognome} non può essere eliminato in quanto non esistente nella rubrica corrente.')
            return False

    # Restitusce i dati del contatto se la chiave e' presente nella rubrica e "None" altrimenti -- case insensitive
    def cerca(self, nome, cognome):

        # Acquisizione del lock
        self.rubLock.acquire()
        logging.info(f'Inizio processo di ricerca contatto {nome} {cognome} nella rubrica.')
        nomeLower = (str(nome)).lower()
        cognomeLower = (str(cognome)).lower()
        # Definisco una versione lowercase della key da cercare
        KeySearchLower = (nomeLower, cognomeLower)
        # Inizializzo variabile contatore a 0
        Trovato = 0

        # Per ogni chiave contenuta nel dizionario
        for nomeCognomeKey in self.rub:
            # Converto le stringhe contenute nella chiave in lowercase e costuisco una versione lowercase della tupla originale
            CurrentKeyLowTuple = tuple([element.lower() for element in nomeCognomeKey])
            # Se la tupla di chiavi contenute nel dizionario (in versione lowercase) è equivalente a KeySearchLower
            if CurrentKeyLowTuple == KeySearchLower:
                # Vuol dire che sono la stessa chiave e quindi incremento trovato ed interrompe l'iterazione
                Trovato += 1
                break

        # Se la chiave di ricerca ha ottenuto riscontro nel dizionario restituisce il numero di telefono del contatto in rubrica
        if Trovato > 0:
            #asssegno il valore del numero cellulare ad una variabile
            numero = self.rub[nomeCognomeKey]
            # Rilascio del lock
            self.rubLock.release()
            logging.info(f'Contatto {nome} {cognome} dal numero: {numero} rinvenuto nella rubrica corrente.')
            return numero
        # Se la chiave cercata non esiste restituisce None
        else:
            # Rilascio del lock
            self.rubLock.release()
            logging.info(f'Contatto {nome} {cognome} non rinvenuto nella rubrica corrente.')
            return None

    # Salva su file il contenuto della rubrica secondo un opportuno formato (a scelta dello studente)
    # Il formato da me scelto prevede un contatto per linea--> nome_cognome:telefono\n
    def store(self, nomefile):

        # Acquisizione del lock
        self.rubLock.acquire()
        # Creo (o sovrascrivo se già esiste) un file
        outfile = open(nomefile, "w")

        # Per ogni chiave contenuta nel dizionario
        for nomeCognomeKey in self.rub:
            rigaContatto = ""
            # Per ogni elemento stringa contenuto nella chiave corrente
            for elemento in nomeCognomeKey:
                # Se variabile key è una stringa vuota (prima iterazione), gli assegno l'elemento stringa corrente
                if not rigaContatto:
                    rigaContatto = elemento
                # Se key non è una stringa vuota concateno il proprio valore corrente con il carattere di separazione seguito dall'elemento stringa corrente
                else:
                    rigaContatto = rigaContatto + self.SERIALIZATION_SEPARATOR + elemento
            # Definisco formattazione di ogni contatto:
            # Chiave stringa definita nel for precedente, a cui concateno ":" e il numero di telefono in formato string
            righeContattiStr = rigaContatto + ':' + str(self.rub[nomeCognomeKey])
            # Concateno a record il carattere newline
            outfile.write(righeContattiStr + '\n')
            # Chiusura scrittura del file
        outfile.close()
        # Rilascio del lock
        self.rubLock.release()

    # Serializza su stringa il contenuto della rubrica: le chiavi ordinate lessicograficamente per Cognome -- Nome in modo crescente (True) o decrescente (False)
    # Fra nome, cognome e telefono seve essere presente ESATTAMENTE uno spazio-- Restituisce la stringa prodotta
    def ordina(self, crescente=True):

        # Acquisizione del lock
        self.rubLock.acquire()
        logging.info(f'Inizio processo di ordinamento contatti della rubrica.')
        rubOrdinataMostrata = ""
        rubricaList = []

        # Per ogni chiave contenuta nel dizionario
        for nomeCognomeKey in self.rub:
            # Trasformo la tupla chiave in lista
            nomeCognomeList = list(nomeCognomeKey)
            # Assegno a variabili nome e cognome i corrispettivi valori all'interno della keylist
            nome = nomeCognomeList[0]
            cognome = nomeCognomeList[1]
            numero = str(self.rub[nomeCognomeKey])
            # Appendo cognome nome e numero (in formato stringa) a rubricalist
            rubricaList.append([cognome, nome, numero])

        # Se il valore passato come parametro è True (ordine dalla A-Z)
        if crescente:
            logging.info(f'Ordine selezionato: Crescente.')
            # Ordino la lista contenente i dati dei singoli contatti (ulteriori liste contenenti stringhe)
            listaOrdineCrescente = sorted(rubricaList, key=lambda row: [row[0].casefold(), row[1]])
            # Per ogni lista contenuta nella lista ordinata
            for contatto in listaOrdineCrescente:
                # Assegno a show il proprio valore corrente concatenandogli la stringa "Cognome Nome numero" estratti dalla lista corrente
                rubOrdinataMostrata = rubOrdinataMostrata + str("%s %s %s" % (contatto[0].title(), contatto[1].title(), contatto[2])) + "\n"
        # Se il valore passato come parametro è False (ordine dalla Z-A)
        else:
            logging.info(f'Ordine selezionato: Decrescente.')
            # Ordino la lista contenente i dati dei singoli contatti (ulteriori liste contenenti stringhe)
            listaOrdineDecrescente = sorted(rubricaList, reverse=True, key=lambda row: [row[0].casefold(), row[1]])
            # Per ogni lista contenuta nella lista ordinata
            for contatto in listaOrdineDecrescente:
                # Assegno a show il proprio valore corrente concatenandogli la stringa "Cognome Nome numero" estratti dalla lista corrente
                rubOrdinataMostrata = rubOrdinataMostrata + str("%s %s %s" % (contatto[0].title(), contatto[1].title(), contatto[2])) + "\n"
                # Restituisci variabile show
        # Rilascio del lock
        self.rubLock.release()
        logging.info("Visualizzazione Contatti della Rubrica ordinati: {}".format(rubOrdinataMostrata))
        return rubOrdinataMostrata

    # Il metodo suggerisci viene invocato da un thread per effettuare un suggerimento di un contatto nella rubrica.
    # Prende come parametro il nome ed il cognome del contatto e lo inserisce in una coda (di lunghezza massima 3).
    # Non si puo’ inserire un elemento nella coda se la coda e’ piena.
    def suggerisci(self, nome, cognome):

        # Acquisizione del lock
        self.rubLock.acquire()
        logging.info(f'Inizio processo suggerisci contatto {nome} {cognome} al consumatore.')
        #finchè la coda condivisa è piena attendi
        while self.queue.full():
            self.rubLock.wait()

        nomeCognomeKeyProposta = ((str(nome)), (str(cognome)))
        nomeLower = (str(nome)).lower()
        cognomeLower = (str(cognome)).lower()
        # Definisco una versione lowercase della key da cercare
        KeySearchLower = (nomeLower, cognomeLower)

        # Per ogni chiave contenuta nel dizionario
        for nomeCognomeKey in self.rub:
            # Converto le stringhe contenute nella chiave in lowercase e costuisco una versione lowercase della tupla originale
            CurrentKeyLowTuple = tuple([element.lower() for element in nomeCognomeKey])
            # Se la tupla di chiavi contenute nel dizionario (in versione lowercase) è equivalente a KeySearchLower
            if CurrentKeyLowTuple == KeySearchLower:
                # Vuol dire che sono la stessa chiave, assegno a variabile record il record di contatto
                record = {nomeCognomeKeyProposta: self.rub.get(nomeCognomeKeyProposta)}
                # Inserisco record precedentemente creato in coda
                self.queue.put(record)
                # Risveglio agli altri thread in attesa
                self.rubLock.notifyAll()
                # Rilascio del lock
                self.rubLock.release()
                logging.info(f'Contatto {nome} {cognome} esistente nella rubrica e suggerito al Consumatore - correttamente inserito in coda.')
                return

        logging.info(f'Contatto {nome} {cognome} non esistente nella rubrica: inizio processo di inserimento.')
        # Primo numero tra 1 e 9
        telefonoList = [r.randint(1, 9)]
        # Appendo 9 cifre generate al numero
        for i in range(1, 10):
            telefonoList.append(r.randint(0, 9))
        # Converto lista in numero intero di 10 cifre
        TelefonoNum = int(''.join(str(i) for i in telefonoList))
        # Invoco inserisci contatto in rubrica
        self.inserisci(nome, cognome, TelefonoNum)
        logging.debug("Stampa struttura dati rubrica per verificare l'aggiunta del contatto: {}".format(self.rub))
        logging.info(f'Contatto {nome} {cognome}: {TelefonoNum} da suggerire non precedentemente esistente nella rubrica è stato aggiunto con successo')
        # Assegno a variabile il record di contattto
        record = {nomeCognomeKeyProposta: TelefonoNum}
        # Inserisco record in coda
        self.queue.put(record)
        # Risveglio agli altri thread in attesa
        self.rubLock.notifyAll()
        # Rilascio del lock
        self.rubLock.release()
        logging.info(f'Contatto {nome} {cognome} (ora esistente nella rubrica) suggerito al consumatore - correttamente inserito in coda.')
        return

    # Il metodo suggerimento viene invocato da un thread per ottenere un suggerimento recuperato dalla rubrica.
    # Il thread legge gli elementi presenti in una coda di lunghezza 3.
    # Se la coda è vuota, attende l’inserimento diun elemento, altrimenti prende il primo elemento della coda e lo stampa
    def suggerimento(self):

        # Acquisizione del lock
        self.rubLock.acquire()
        logging.info("Inizio processo estrazione suggerimento contatto della rubrica da parte del consumatore.")
        # Finchè la coda è vuota resta in attesa
        while self.queue.empty():
            self.rubLock.wait()
        # Assegno a variabile suggerimento il record contenuto in coda FIFO (primo record che è stato inserito)
        suggerimento = self.queue.get()
        # Comunico la conclusione della fase di utlizzo della struttura condivisa coda
        self.queue.task_done()
        # Risveglio agli altri thread in attesa
        self.rubLock.notifyAll()
        # Itero gli elementi nel record appena recuperato per assegnare i valori di interesse a variabili
        for key, value in suggerimento.items():
            numero = value
            nome = key[0]
            cognome = key[1]

        # Assegno a stringaSugg una stringa che comunichi il suggerimento all'utente
        stringaSugg = "Suggerimento: "+str("%s %s %s" % (nome.title(), cognome.title(), numero))
        # Rilascio del lock
        self.rubLock.release()
        logging.info("Contatto Suggerito dal Produttore {}".format(stringaSugg))
        return stringaSugg
