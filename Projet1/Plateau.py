import numpy as np
import random as rnd
from matplotlib import cm
import matplotlib.pyplot as plt
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
        self.cptj1 = 0
        self.cptj2 = 0

    def affichePlateau(self):
        """
        Fonction permettant avec la bibli matplotlib d'afficher le terrain
        """
        plt.matshow(self.tab)
        plt.show()

    def listWinInit(self):
        """
        fonction qui stocke dans une liste toute les tuples gagnants possibles sur le plateau
        """ 
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
        """
        fonction permettant de reinitialiser toutes les valeurs du tableau a zero
        """
        self.tab = np.zeros((L,l))

    def has_won(self):
        """
        Fonction permettant de savoir si le jeu actuel a un gagnant ou non 
        """       
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
        """
        fonction permettant de faire jouer un joueur a la colonne c si c est possible
        """
        for l in range(ligne-1, -1, -1 ):
            if( self.tab[l,c-1] != 0 ):
                continue
            else:
                self.tab[l,c-1] = joueur
                return

    def is_finished(self):
        """
        fonction qui parcours le plateau pour savoir si la partie est finie ou non
        """
        if( self.has_won() ):
            print("We have a winner !")
            self.affichePlateau()
            return True
        for l in range(0 , self.l):
            for c in range(0, self.c):
                if( self.tab[l,c] == 0 ):
                    return False
        print("Game is over without winner..!")
        return True

    def run(self, joueur1, joueur2):
        """
        Tant que le jeu n est pas fini chaques joueurs jouent a tour de role
        """
        cpt = 0
        while not self.is_finished() :
            if cpt % 2 == 0 :
                stock = joueur1.play_joueur(self,joueur1)
                self.play( stock, joueur1.id )
                self.cptj1+=1
                if( self.is_finished() ):
                    return 1
                cpt+=1
            else:
                stock = joueur2.play_joueur(self,joueur2)
                self.play( stock, joueur2.id )
                self.cptj2+=1
                if( self.is_finished() ):
                    return -1
                cpt+=1


class Joueur :

    def __init__(self, x):
        """
        Fonction permettant d'initialiser un joueur avec pour jeton x
        """
        self.id = x

    def play_joueur(self, plateau, joueur):
        """
        Fonction permettant de faire jouer un joueur
        """
        c = rnd.randint(0, (plateau.c)-1)
        return c


pl = Plateau( ligne, colonne )
j1 = Joueur(1)
j2 = Joueur(-1)
print(pl.tab)
pl.run(j1,j2)
print(pl.tab)
print(pl.cptj1)
print(pl.cptj2)
