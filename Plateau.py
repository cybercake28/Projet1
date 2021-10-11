import numpy as np
import random as rnd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import operator
from copy import copy, deepcopy

ligne = 6
colonne = 7
listwin = []

# nb de parties à simuler
nb_parties = 1000

# nombre de partie fictivce au Monte Carlo afin de determiner le coup à jouer
nb_Monte_carlo = 100

class Plateau :

    def __init__(self, l, c):
        """
        Fonction permettant d'initialiser le plateau du jeu
        """
        self.tab = np.zeros((l,c))
        self.l = ligne
        self.c = colonne
        #lj1 est la liste du nombre de coup joué par le joueur1 lors d'une de ses victoires même chose pour lj2 mais pour le joueur2
        self.lj1 = []
        self.lj2 = []
        self.nb_parties_nulles = 0
        self.listwin = self.listWinInit()

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
        self.tab = np.zeros((self.l,self.c))

    def has_won(self):
        """
        Fonction permettant de savoir si le jeu actuel a un gagnant ou non
        """
        for tup in self.listwin:
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
        fonction permettant de faire jouer un joueur a la colonne c
        """

        for l in range(ligne-1, -1, -1 ):
            if( self.tab[l,c-1] != 0 ):
                continue
            else:
                self.tab[l,c-1] = joueur
                return
        if( c+1 < self.c -1 ):
            self.play(c+1,joueur)

    def is_finished(self):
        """
        fonction qui parcours le plateau pour savoir si la partie est finie ou non
        """
        if( self.has_won() ):
            return 1 # un joueur a gagne
        for l in range(0 , self.l):
            for c in range(0, self.c):
                if( self.tab[l,c] == 0 ):
                    return -1 # le jeu continue personne n'a gagne
        return 0 # impossible de continuer de jouer

    def run(self, joueur1, joueur2):
        cpt = 0
        cpt_coup1 = 0
        cpt_coup2 = 0
        while self.is_finished() == -1 :
            if cpt % 2 == 0 :
                stock = joueur1.play_joueur(self,joueur1)
                cpt_coup1 += 1
                self.play( stock, joueur1.id )
                if( self.is_finished() == 1 ):
                    joueur1.nb_coup = cpt_coup1
                    joueur2.nb_coup = cpt_coup2
                    (self.lj1).append((joueur1.nb_coup))
                    return 1
                cpt+=1
            else:
                stock = joueur2.play_joueur(self,joueur2)
                cpt_coup2 += 1
                self.play( stock, joueur2.id )
                if( self.is_finished()  == 1 ):
                    joueur1.nb_coup = cpt_coup1
                    joueur2.nb_coup = cpt_coup2
                    (self.lj2).append((joueur2.nb_coup))
                    return -1
                cpt+=1
        self.nb_parties_nulles+=1
        return 0

    def distribution(self, joueur1, joueur2, nb_parties):
        for i in range(0, nb_parties):
            self.run(joueur1, joueur2)
            self.reset()
            joueur1.reset_nb_coup()
            joueur2.reset_nb_coup()

    # partie entre deux joueur utilisant le monte carlo
    def run_double_Monte_Carlo(self, joueur1, joueur2):
        cpt = 0
        cpt_coup1 = 0
        cpt_coup2 = 0

        # partie sans gagnant mais encore jouable
        while self.is_finished() == -1 :
            if cpt % 2 == 0 :
                stock = joueur1.monte_carlo_play(self, joueur2)
                cpt_coup1 += 1
                self.play( stock, joueur1.id )
                #La partie s'est terminé sur une victoire et apres le coup de ce joueur
                if( self.is_finished() == 1 ):
                    joueur1.nb_coup = cpt_coup1
                    joueur2.nb_coup = cpt_coup2
                    (self.lj1).append((joueur1.nb_coup))
                    return 1
                cpt+=1
            else:
                stock = joueur2.monte_carlo_play(self, joueur1)
                cpt_coup2 += 1
                self.play( stock, joueur2.id )
                #La partie s'est terminé sur une victoire et apres le coup de ce joueur
                if( self.is_finished()  == 1 ):
                    joueur1.nb_coup = cpt_coup1
                    joueur2.nb_coup = cpt_coup2
                    (self.lj2).append((joueur2.nb_coup))
                    return -1
                cpt+=1
        self.nb_parties_nulles+=1
        return 0

    def run_monteVSrandom(self, j_monte, j_random):
        cpt = 0
        cpt_coup1 = 0
        cpt_coup2 = 0
        # partie sans gagnant mais encore jouable
        while self.is_finished() == -1 :
            if cpt % 2 == 0 :
                stock = j_monte.monte_carlo_play(self, j_random)
                cpt_coup1 += 1
                self.play( stock, j_monte.id )
                if( self.is_finished() == 1 ):
                    j_monte.nb_coup = cpt_coup1
                    j_random.nb_coup = cpt_coup2
                    (self.lj1).append((j_monte.nb_coup))
                    return 1
                cpt+=1
            else:
                stock = j_random.play_joueur(self, j_random)
                cpt_coup2 += 1
                self.play( stock, j_random.id )
                if( self.is_finished()  == 1 ):
                    j_monte.nb_coup = cpt_coup1
                    j_random.nb_coup = cpt_coup2
                    (self.lj2).append((j_random.nb_coup))
                    return -1
                cpt+=1

        self.nb_parties_nulles+=1
        return 0

    def distribution_monteVSmonte(self, joueur1, joueur2, nb_parties):
        for i in range(0, nb_parties):
            self.run_double_Monte_Carlo(joueur1, joueur2)
            self.reset()
            joueur1.reset_nb_coup()
            joueur2.reset_nb_coup()

    def distribution_monteVSrandom(self, monte, random, nb_parties):
        for i in range(0, nb_parties):
            self.run_monteVSrandom(monte, random)
            self.reset()
            monte.reset_nb_coup()
            random.reset_nb_coup()


class Joueur :

    def __init__(self, x):
        self.id = x
        self.nb_coup = 0

    def reset_nb_coup(self):
        self.nb_coup = 0

    def play_joueur(self, plateau, joueur):
        c = rnd.randint(0, (plateau.c)-1)
        return c

    def monte_carlo_play(self, etat, joueuradverse):
        dico = {}

        #on fait une copie du plateau original
        plat = deepcopy(etat)

        for i in range(0, nb_Monte_carlo):
            plat = deepcopy(etat)
            #on recupere un numéro de colonne aléatoire
            a = joueuradverse.play_joueur(plateau, self)
            #si cette action nous permet de gagner la partie sur le même plateau de jeu alors on ajoute cette action au dictionnaire ou on incrémente son compteur 
            stock = plat.run(self,joueuradverse)
            if( stock  == self.id ):
                if a in dico:
                    dico[a] = dico[a]+1
                else:
                    dico[a] = 1
        #verification que le dictionnaire n'est pas vide
        if not dico : 
            return rnd.randint(0, (etat.c)-1)

        return max(dico, key=dico.get)


#---------------------------------------------------------------- PARTIE : 1 ----------------------------------------------------------------
# plateau = Plateau( ligne, colonne )
# joueur1 = Joueur(1)
# joueur2 = Joueur(-1)

# #on simule les parties tout en sauvegardant le nombre de coups joues du gagnant
# plateau.distribution(joueur1, joueur2, nb_parties)

#listes avec le nombre de coup de chaque victoire
# list_tot = plateau.lj1 + plateau.lj2

# nb_win_total = len(list_tot)
# nb_nulle = plateau.nb_parties_nulles
# nb_win_j1 = len(plateau.lj1)
# nb_win_j2 = len(plateau.lj2)

# print("nb win total : " + str(nb_win_total))
# print("nb no win : " + str(nb_nulle))
# print("nb win j1 : " + str(nb_win_j1))
# print("nb win j2 : " + str(nb_win_j2))

# #Deux joueurs hist
# plt.hist(list_tot,  bins=50)
# plt.show()

# #joueur 1 hist
# plt.hist(plateau.lj1,  bins=50)
# plt.show()

# #joueur 2 hist
# plt.hist(plateau.lj2, bins=50)
# plt.show()


#---------------------------------------------------------------- PARTIE : 2 ----------------------------------------------------------------
plateau = Plateau(ligne, colonne)
joueur1 = Joueur(1)
joueur2 = Joueur(-1)

# Distribution joueur monte carlo vs joueur à tirage aléatoire
plateau.distribution_monteVSrandom(joueur1, joueur2, nb_parties)

# listes avec le nombre de coup de chaque victoire
list_tot = plateau.lj1 + plateau.lj2

nb_win_total = len(list_tot)
nb_nulle = plateau.nb_parties_nulles
nb_win_j1 = len(plateau.lj1)
nb_win_j2 = len(plateau.lj2)

print("nb win total : " + str(nb_win_total))
print("nb no win : " + str(nb_nulle))
print("nb win j1 : " + str(nb_win_j1))
print("nb win j2 : " + str(nb_win_j2))

#Deux joueurs hist
plt.hist(list_tot,  bins=50)
plt.show()

#joueur 1 hist
plt.hist(plateau.lj1,  bins=50)
plt.show()

#joueur 2 hist
plt.hist(plateau.lj2, bins=50)
plt.show()
