# Assegnamento 2 aa 2021-22 622AA modulo programmazione 9 crediti
# Simona Sette mat:544298 s.sette@studenti.unipi.it 3516774933
from rubrica import Rubrica
from Consumatore import Consumatore
from Produttore import Produttore
import tkinter as tk


class Finestra:

    def __init__(self, root):

        self.root = root
        self.root.title("Verifica Simple-Multi Thread")
        self.root.geometry("400x400")

        self.LabelText = tk.Label(bg="white", text='Premere il tasto sottostante per effettuare un SimpleTest.')
        self.LabelText.grid(column=0, row=1, padx=20, pady=5, sticky=tk.W)
        self.btn_Simple = tk.Button(bg="orange", text='Prova Single Thread', width=25, height=3)
        self.btn_Simple.grid(column=0, row=2, padx=20, pady=10, sticky=tk.W)

        self.LabelInputN = tk.Label(bg="white", text='Inserisci Numero di Thread Produttore-Consumatore da lanciare.')
        self.LabelInputN.grid(column=0, row=6, padx=20, pady=5, sticky=tk.W)
        self.InputN = tk.Entry(width=20)
        self.InputN.grid(column=0, row=7, padx=20, pady=5, sticky=tk.W)

        self.btn_Multi = tk.Button(bg="orange", text='Prova Multi-Thread', width=25, height=3)
        self.btn_Multi.grid(column=0, row=8, padx=20, pady=10, sticky=tk.W)

        self.res = tk.Label(bg="white", text="Qui sarà possibile constatare l'esito dell'esecuzione al suo termine.")
        self.res.grid(column=0, row=10, padx=20, pady=5, sticky=tk.W)
        # binding bottoni-eventi
        self.btn_Simple.bind("<Button-1>", self.handler_simpletest)
        self.btn_Multi.bind("<Button-1>", self.handler_multitest)

    # quando invocata tramite evento click avvia il Simple Test
    def handler_simpletest(self, evento):

        m = Rubrica()
        s = Produttore(m, 1)
        c = Consumatore(m, 1)
        s.start()
        c.start()
        s.join()
        c.join()
        # restituisce la risposta
        self.res.destroy()
        self.res = tk.Label(bg="lightgreen", text="Esito esecuzione SimpleTest: il processo si è concluso con successo!", height=5, width=50)
        self.res.grid(column=0, row=10, padx=10, pady=5, sticky=tk.W)

    # quando invocata tramite evento click avvia il Multi Test
    def handler_multitest(self, evento):

        numero = self.InputN.get()
        if numero.isdigit() and int(numero)>0:
            m = Rubrica()
            threads = []
            for i in range(int(numero)):
                s = Produttore(m, i)
                threads.append(s)
                c = Consumatore(m, i)
                threads.append(c)

            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
            # restituisce la risposta
            self.res.destroy()
            self.res = tk.Label(bg="lightgreen", text="Esito esecuzione Multi-Test: il processo si è concluso con successo!", height=5, width=50)
            self.res.grid(column=0, row=10, padx=10, pady=5, sticky=tk.W)
        else:
            self.res.destroy()
            self.res = tk.Label(bg="red", text="Esito esecuzione Multi-Test:\nprocesso non eseguito causa input non valido;\n si ricorda che sono accettati solo valori numerici maggiori di zero.", height=5, width=50)
            self.res.grid(column=0, row=10, padx=10, pady=5, sticky=tk.W)

    def handler_exit(self, evento):
        # chiude la finestra
        self.root.destroy()


if __name__ == '__main__':
    # attivazione dell'interfaccia
    root = tk.Tk()
    Finestra(root)
    # avvio del ciclo ascolto eventi
    root.mainloop()
