# Assegnamento 1  aa 2021-22 622AA modulo programmazione 9 crediti
# Simona Sette 544298 s.sette@studenti.unipi.it 3516774933

class Rubrica:
    
    
   #Costruttore: crea una rubrica vuota rappresentata come dizionario di contatti vuoto
    def __init__(self):
        #crea una nuova rubrica vuota
        self.rub = {}

        
    #Serializza una rubrica attraverso una stringa con opportuna codifica (a scelta dello studente)   
    def  __str__(self):
        #creo variabile records a cui verranno concatenate le stringhe prodotte all'esecuzione dell'if-else
        records = "RUBRICA"+"\n"+"CONTATTO : NUMERO"+ "\n"*2
        #se il dizionario è vuoto
        if len(self.rub) == 0:
            #concateno a records la stringa definita nel return
            return("Spiacenti,la tua rubrica è ancora vuota! Perchè non aggiungi un numero?")
        #se il dizionario non è vuoto
        else:
            #per ogni chiave del dizionario
            for k in self.rub:
                stringkey = ""
                #per ogni elemento(tipo stringa) nella chiave (tipo tupla)
                for i in k:
                    #concateno a stringkey il proprio valore corrente, a cui faccio seguire uno spazio e l'elemento d'iterazione corrente
                    stringkey = stringkey+" "+str(i)
                #definisco stampa di ogni contatto: 
                #chiave stringa definita nel for precedente, a cui concateno ":" e il numero di telefono (di tipo stringa)
                record = stringkey+':'+ str(self.rub[k]) 
                #assegno il precedente record a records, seguito da un newline
                records += str(record)+"\n"
            #restituisco variabile records che conterrà i singoli dati dei contatti seguiti dal newline
            return(records)
                
            
    #stabilisce se due rubriche contengono esattamente le stesse chiavi con gli stessi dati        
    def __eq__(self, r2):
        #se le due rubriche sono equivalenti restituisce true, false altrimenti
        if (self.rub == r2.rub):
            return True
        else:
            return False
    
    
    #crea una nuova rubrica unendone due (elimina i duplicati) e la restituisce come risultato 
    #se ci sono contatti con la stessa chiave nelle due rubriche ne riporta uno solo
    def __add__(self, r2):
        #assegno a varibili r1 e r2 le rubriche da sommare
        r1 = self.rub
        r2 = r2.rub
        #dichiaro una nuova rubrica vuota
        r3 = Rubrica()
        #assegno a r3 un dizionario che contiene la somma del contenuto dei dizionari (precedentemente convertiti in tipo lista)
        r3.rub = dict(list(r1.items()) + list(r2.items()))
        #restituisco la somma dei dizionari
        return r3
    
    
    #carica da file una rubrica eliminando il precedente contenuto di self
    def load(self, nomefile):
        
        self.rub={}
        #apro il file in lettura e assegno le singole righe ad aline
        with open(nomefile, "r") as inline:
            aline = inline.read().splitlines() 
            #per ogni riga contenuta in aline faccio uno split della riga sul carattere ":"
            for line in aline:
                tuplakey = ()
                items = line.split(':')
                #per ogni elemento contenuto nel primo elemento generato dello splitting (contiene nome_cognome)
                for i in items[0]:
                    listakey = []
                    #faccio uno split sul carattere "_"
                    x = items[0].split('_')
                    #assegno gli elementi generati dello splitting a una lista
                    listakey = [x[0],x[1]]
                    #assegno a tuplakey la lista precedentemente definita e convertita in tupla
                    tuplakey = tuple(listakey)
                #assegno a value il numero di telefono come un intero
                value = int(items[1])
                #assegno iterativamente alla rubrica le coppie chiavi,valore 
                #la chiave è una tupla contenente le stringhe di nome e cognome; il valore è un intero
                self.rub[tuplakey]=value
    
    
    #inserisce un nuovo contatto con chiave (nome,cognome) restituisce "True" se l'inserimento è andato a buon fine e "False" altrimenti (es chiave replicata) -- case insensitive
    def inserisci(self, nome, cognome, dati):
        #definisco la futura key che potrebbe essere inserita
        key = ((str(nome)),(str(cognome)))
        NomeCI=(str(nome)).lower()
        CognomeCI=(str(cognome)).lower()
        #definisco una versione lowercase della possibile futura key 
        keyLower=((NomeCI),(CognomeCI))
        
        #se dizionario è vuoto inserisce primo record
        if bool(self.rub) == False:
            self.rub[key]=int(dati)
            return True 
        #se dizionario non è vuoto 
        else:
            #inizializzo variabile contatore a 0
            NoOk=0
            #per ogni chiave contenuta nel dizionario
            for e in self.rub.keys():
                current=[]
                #per ogni elemento stringa contenuto nelle singole chiavi
                for i in e:
                    #appendo alla lista current gli elementi stringa in lowercase
                    current.append(i.lower())
                #assegno a currenTuple la lista definita nel precedente for e convertita in tupla
                currenTuple=tuple(current)
                #se la tupla di chiavi contenute nel dizionario in lowercase è equivalente a keyLower
                if currenTuple==keyLower:
                    #vuol dire che sono la stessa chiave e quindi incremento NoOk ed interrompe l'iterazione
                    NoOk+=1
                    break
            #se NoOk è maggiore di 0 è stata trovata una chiave non idonea all'inserimento e restituisce False
            if NoOk>0:
                return False  
            #se la chiave è idonea inserisce il contatto nella rubrica e restituisce true
            else:
                self.rub[key]=int(dati)
                return True
    
    
    #modifica i dati relativi al contatto con chiave (nome,cognome)sostituendole con "newdati" 
    #restituisce "True" se la modifica è stata effettuata e "False" altrimenti (es: la chiave non è presente )
    def modifica(self, nome, cognome, newdati):
       
        NomeCI=(str(nome)).lower()
        CognomeCI=(str(cognome)).lower()
        #definisco una versione lowercase della key da cercare
        KeySearchLower=((NomeCI),(CognomeCI))
        #inizializzo variabile contatore a 0
        trovato=0
        #per ogni chiave contenuta nel dizionario
        for k in self.rub: 
            current=[]
            #per ogni elemento stringa contenuto nella chiave corrente
            for i in k:
                #appendo alla lista current gli elementi stringa in lowercase
                current.append(i.lower())
            #assegno a currenTuple la lista definita nel precedente for e convertita in tupla
            currenTuple=tuple(current)
            #se la tupla di chiavi contenute nel dizionario in lowercase è equivalente a KeySearchLower
            if currenTuple==KeySearchLower:
                #vuol dire che sono la stessa chiave e quindi incremento trovato ed interrompe l'iterazione
                trovato+=1
                break
        #Se la chiave di ricerca ha ottenuto riscontro nel dizionario modifica i dati del contatto nella rubrica e restituisce true
        if trovato>0:
            self.rub[k]=int(newdati)
            return True
        #se la chiave ricercata non esiste restiuisce False
        else:
            return False
    
    
    #il contatto con chiave (nome,cognome) esiste lo elimina insieme ai dati relativi e restituisce True -- altrimenti restituisce False        
    def cancella(self, nome, cognome):
      
        NomeCI=(str(nome)).lower()
        CognomeCI=(str(cognome)).lower()
        #definisco una versione lowercase della key da cercare
        KeySearchLower=((NomeCI),(CognomeCI))
        #inizializzo variabile contatore a 0
        trovato=0
        #per ogni chiave contenuta nel dizionario
        for k in self.rub:
            current=[]
            #per ogni elemento stringa contenuto nella chiave corrente
            for i in k:
                #appendo alla lista current gli elementi stringa in lowercase
                current.append(i.lower())
            #assegno a currenTuple la lista definita nel precedente for e convertita in tupla
            currenTuple=tuple(current)
            #se la tupla di chiavi contenute nel dizionario in lowercase è equivalente a KeySearchLower
            if currenTuple==KeySearchLower:
                #vuol dire che sono la stessa chiave e quindi incremento trovato ed interrompe l'iterazione
                trovato+=1
                break
        #Se la chiave di ricerca ha ottenuto riscontro nel dizionario cancella il contatto dalla rubrica e restituisce true
        if trovato>0:
            del self.rub[k]
            return True
        #se la chiave cercata non esiste restituisce False
        else:
            return False
        
        
    #restitusce i dati del contatto se la chiave e' presente nella rubrica e "None" altrimenti -- case insensitive       
    def cerca(self, nome, cognome):
        
        NomeCI=(str(nome)).lower()
        CognomeCI=(str(cognome)).lower()
        #definisco una versione lowercase della key da cercare
        KeySearchLower=((NomeCI),(CognomeCI))
        #inizializzo variabile contatore a 0
        trovato=0
        #per ogni chiave contenuta nel dizionario
        for k in self.rub:
            current=[]
            #per ogni elemento stringa contenuto nella chiave corrente
            for i in k:
                #appendo alla lista current gli elementi stringa in lowercase
                current.append(i.lower())
            #assegno a currenTuple la lista definita nel precedente for e convertita in tupla
            currenTuple=tuple(current)
            #se la tupla di chiavi contenute nel dizionario in lowercase è equivalente a KeySearchLower
            if currenTuple==KeySearchLower:
                #vuol dire che sono la stessa chiave e quindi incremento trovato ed interrompe l'iterazione
                trovato+=1
                break
        #Se la chiave di ricerca ha ottenuto riscontro nel dizionario restituisce il numero di telefono del contatto in rubrica
        if trovato>0:
            return (self.rub[k])
        #se la chiave cercata non esiste restituisce None
        else:
            return None
        
        
    #salva su file il contenuto della rubrica secondo un opportuno formato (a scelta dello studente)
    # il formato da me scelto prevede un contatto per linea
    # nome_cognome:telefono\n
    def store(self, nomefile):
        #creo (o sovrascrivo se già esiste) un file
        outfile = open(nomefile, "w")
        #per ogni chiave contenuta nel dizionario
        for k in self.rub:
            key=""
            #per ogni elemento stringa contenuto nella chiave corrente
            for i in k:
                #se variabile key è una stringa vuota (prima iterazione), gli assegno l'elemento stringa corrente
                if not key:
                    key=i
                #se key non è una stringa vuota concateno il proprio valore corrente con il carattere "_" seguito dall'elemento stringa corrente
                else:
                    key=key+"_"+i   
            #definisco formattazione di ogni contatto: 
            #chiave stringa definita nel for precedente, a cui concateno ":" e il numero di telefono in formato string
            record = key + ':' + str(self.rub[k])
            #concateno a record il carattere newline
            outfile.write(record + '\n')   
        #chiusura scrittura del file
        outfile.close()
        
        
    # serializza su stringa il contenuto della rubrica: le chiavi ordinate lessicograficamente per Cognome -- Nome in modo crescente (True) o decrescente (False)
    #Fra nome, cognome e telefono seve essere presente ESATTAMENTE uno spazio-- Restituisce la stringa prodotta
    def ordina(self,crescente=True):

        show=""
        rubricalist=[]
        #per ogni chiave contenuta nel dizionario
        for k in self.rub:
            #trasformo la tupla chiave in lista
            keylist=list(k)
            #assegno a variabili nome e cognome i corrispettivi valori all'interno della keylist
            nome=keylist[0]
            cognome=keylist[1]
            numero= str(self.rub[k])
            #appendo cognome nome e numero (in formato stringa) a rubricalist 
            rubricalist.append([cognome,nome,numero])
        #se il valore passato come parametro è True (ordine dalla A-Z)
        if crescente==True:
            #ordino la lista contenente i dati dei singoli contatti (ulteriori liste contenenti stringhe)
            cresc=sorted(rubricalist, key=lambda row: [row[0].casefold(), row[1]])
            #per ogni lista contenuta nella lista ordinata
            for c in cresc:
                #assegno a show il proprio valore corrente concatenandogli la stringa "Cognome Nome numero" estratti dalla lista corrente
                show=show+ str("%s %s %s" % (c[0].title(), c[1].title(),c[2]))+ "\n"
        #se il valore passato come parametro è False (ordine dalla Z-A)
        else:
            #ordino la lista contenente i dati dei singoli contatti (ulteriori liste contenenti stringhe)
            decresc=sorted(rubricalist, reverse=True, key=lambda row: [row[0].casefold(), row[1]])
            #per ogni lista contenuta nella lista ordinata
            for d in decresc:
                #assegno a show il proprio valore corrente concatenandogli la stringa "Cognome Nome numero" estratti dalla lista corrente
                show=show+ str("%s %s %s" % (d[0].title(), d[1].title(),d[2]))+ "\n"   
        #restituisci variabile show
        return show       