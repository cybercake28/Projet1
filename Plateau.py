import numpy as np
import random as rnd
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

ligne = 6
colonne = 7
listwin =[]

class Plateau :

    def __init__(self, L, l):

        """
        Fonction permettant d'initialiser le plateau du jeu

        """
        self.tab = np.zeros((L,l))
        self.l = ligne
        self.c = colonne

    def listWinInit(self):
        #ajout des tuples de victoires sur les lignes
        for lcpt in range(0 , self.l):
            for ccpt in range(0, self.c-3):
                listwin.append(((lcpt,ccpt),(lcpt,ccpt+1),(lcpt,ccpt+2),(lcpt,ccpt+3)))

        #ajout des tuples de victoires sur les colonnes
        for ccpt in range(0 , self.c):
            for lcpt in range(0, self.l-3):
                listwin.append(((lcpt,ccpt),(lcpt+1,ccpt),(lcpt+2,ccpt),(lcpt+3,ccpt)))

        #ajout des tuples de victoires sur les diagonales vers le bas
        for lcpt in range(0 , self.l-3):
            for ccpt in range(0, self.c-3):
                listwin.append(((lcpt,ccpt),(lcpt+1,ccpt+1),(lcpt+2,ccpt+2),(lcpt+3,ccpt+3)))

        #ajout des tuples de victoires sur les diagonales vers le haut
        for lcpt in range(0, self.l-3):
            for ccpt in range(3, self.c):
                listwin.append(((lcpt,ccpt),(lcpt+1,ccpt-1),(lcpt+2,ccpt-2),(lcpt+3,ccpt-3)))
        return listwin

    def reset(self):
        self.tab = np.zeros((L,l))

    def has_won(self):
        listwin = self.listWinInit()
        tmp = 0
        for tup in listwin:
            tup1 = tup[0]
            tup2 = tup[1]
            tup3 = tup[2]
            tup4 = tup[3]
            if( self.tab[tup1] == 0 or self.tab[tup2] == 0 or self.tab[tup3] == 0 or self.tab[tup4] == 0 ):
                continue
            else:
                if( self.tab[tup1] == self.tab[tup2] and self.tab[tup2] == self.tab[tup3] and self.tab[tup3] == self.tab[tup4] ):
                    return True
        return False

    def play(self, c, joueur):
        for l in range(ligne-1, -1, -1 ):
            if( self.tab[l,c-1] != 0 ):
                continue
            else:
                self.tab[l,c-1] = joueur
                return

    def is_finished(self):
        if( self.has_won() ):
            print("We have a winner !")
            return True
        for l in range(0 , self.l):
            for c in range(0, self.c):
                if( self.tab[l,c] == 0 ):
                    return False
        print("Game is over without winner..!")
        return True

    def run(self, joueur1, joueur2):
        cpt = 0
        while( not self.is_finished() ):
            if( cpt % 2 == 0 ):
                stock = joueur1.play(self,joueur1)
                self.play( stock, joueur1.id )
                if( self.is_finished() ):
                    return 1
                cpt+=1
            else:
                stock = joueur2.play(self,joueur2)
                self.play( stock, joueur2.id )
                if( self.is_finished() ):
                    return -1
                cpt+=1


class Joueur :
    def __init__(self, x):
        self.id = x

    def play(self, plateau, joueur):
        c = rnd.randint(0, (plateau.c)-1)
        return c


pl = Plateau( ligne, colonne )
j1 = Joueur(1)
j2 = Joueur(-1)
pl.run(j1,j2)
print(pl.tab)

