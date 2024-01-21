import numpy as np
import matplotlib.pyplot as plt

class Hanoi:
    def __init__ (self):

        # Anzahl der Scheiben eingeben
        self.n = int(input("Geben Sie die Anzahl der Scheiben ein: "))

        self.st = np.zeros((self.n,3), dtype=int)
        print(self.st)
        # Initialstate wird erstellt (nullermatrix)

        for i in range (self.n,0,-1):
            self.st[i-1,0]=i
        # erste Spalte wird mit n Zahlen gefüllt
        
        self.count=0   #Zugzähler
        self.dumm=0    #Dummzähler für illegale und schlechte Züge
        self.visualisierung()
        #print (self.st) # nur zum gucken
        
        
    def move(self,her,zil): #stab der herkunft und zielstab für oberste scheibe
        
        if her==zil:
            self.dumm+=1
            print ("so kann man auch Zeit verbringen...\nNeudumm = ", self.dumm)
            self.play()
            return
        
        i=0
        while self.st[i,her]==0:
            i+=1
            if i==self.n:
                self.dumm+=1
                print ("da is nix, mach nochmal\nNeudumm = ", self.dumm)
                self.play()
                return
            
        print ("Herkunftsspalte, Eintrag in Zeile i: ",i)
        
        if np.sum(self.st[:,zil])==0:
            self.st[self.n-1,zil]=self.st[i,her]
            self.st[i,her]=0
            self.count+=1
       
        else: 
            j=0
            while self.st[j,zil]==0:
                j+=1
            if self.st[j,zil]<self.st[i,her]: 
                self.dumm+=1
                print ("du schummler willst ja schummeln, aber das geht nich!!!!\nNeudumm = ", self.dumm)
                self.play()
                return
            else:
                self.st[j-1,zil]=self.st[i,her]
                self.st[i,her]=0
                self.count+=1
            
            
        print(self.st, "\nnach Zug Nr. ", self.count)
        self.visualisierung()
        self.sieg()  #hab ich schon gewonnen?

    def sieg(self): #Siegbedingung checken
        if np.sum(self.st[:,0])+np.sum(self.st[:,1])==0:
            print ("Winner, Winner, Chicken dinner!\nBenötigte Züge: ", self.count, "\nUnd das nur mit ",self.dumm," Dummzügen")
            
            restart = str(input("wollen Sie nochmal spielen, du Aal? y/n?"))
            
            match restart:
                case "y":
                    game=Hanoi()
                    game.play()# das ist noch nicht global und läuft nicht.
                case "n":
                    print ("byeeeee")
                    return
        else:
            self.play()
            
    def visualisierung(self):
        plt.clf() # vorherigen Plot löschen
        plt.axis('off')
        plt.text(0,4,'0')
        # Stäbe visualisieren
        stab1 = 0
        stab2 = self.n/2
        stab3 = self.n
        Dicke_stab = 0.1
        Dicke_scheibe = 0.4
        plt.bar([stab1, stab2, stab3], self.n, width = Dicke_stab, color = (0.55, 0.3, 0.1))
        plt.text((stab3 + Dicke_scheibe*self.n)/2, self.n*1.1, f"Anzahl der Züge: {self.count}")
        # Farbcodierung muss <=1!!
        r = 0.7
        g = 0.4
        b = 0.8
        # Achse festlegen, damit alles zu sehen ist
        xmin, xmax, ymin, ymax = plt.axis([stab1 - Dicke_scheibe*self.n, stab3 + Dicke_scheibe*self.n, 0, self.n])
        
        # Scheiben visualisieren
        for i in range(3): # Stabschleife (Spalten)
            boden = self.n-1 # Damit wird festgelegt, auf welche Höhe die Scheibe zulegen ist
            for j in range(self.n): # Scheibenschleife (Zeilen)
                Scheibe = self.st[j,i]
                
                if Scheibe == 0:
                    pass
                
                elif i == 0:
                    plt.bar([stab1], 1, width = Dicke_scheibe*Scheibe, bottom = boden, color = (Scheibe/self.n*r, Scheibe/self.n*g, Scheibe/self.n*b))
                elif i == 1:
                    plt.bar([stab2], 1, width = Dicke_scheibe*Scheibe, bottom = boden, color = (Scheibe/self.n*r, Scheibe/self.n*g, Scheibe/self.n*b))
                else:
                    plt.bar([stab3], 1, width = Dicke_scheibe*Scheibe, bottom = boden, color = (Scheibe/self.n*r, Scheibe/self.n*g, Scheibe/self.n*b))
                    
                boden -=1
        plt.pause(0.2) # Plot für jeweils n Sekunden 
                   
    def play(self):
        
        s1 = int(input("Von welchem Stab soll die oberste Scheibe entnommen werden? (0,1 oder 2)\nzum Abbrechen: exit\n"))
        if s1 <3:
            pass
        elif s1 == "exit":
            return
        else:
            print("ungültige Angabe, versuche es nochmal (Erlaubt: 0,1 oder 2)")
            self.play()
        s2 = int(input("Auf welchem Stab soll die gewählte Scheibe gelegt werden? (0,1 oder 2)\nzum Abbrechen: exit\n"))
        if s2<3:
            pass
        elif s2 == "exit":
            return
        else:
            print("ungültige Angabe, versuche es nochmal (Erlaubt: 0,1 oder 2)")
            self.play()
        self.move(s1,s2)
        
            
test = Hanoi()
test.play()