from random import *
from copy import copy, deepcopy
from math import *
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import operator
import matplotlib.pyplot as plt
import numpy as np
import random as rnd



ligne = 6
colonne = 7
listwin = []

# Constantes
# nombre de parties de simulations au Monte Carlo afin de determiner le coup à jouer
nb_Monte_carlo = 100
# nb de parties à simuler partie 3
nb_parties = 1000

# nb iterations pour l'exploration pour algo greed
greed_nb = 50


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

    # partie entre joueur Monte vs joueur random
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

    #  distribution joueurs aléatoires
    def distribution(self, joueur1, joueur2, nb_parties):
        for i in range(0, nb_parties):
            self.run(joueur1, joueur2)
            self.reset()
            joueur1.reset_nb_coup()
            joueur2.reset_nb_coup()

    # distribution joueur monte vs joueur monte
    def distribution_monteVSmonte(self, joueur1, joueur2, nb_parties):
        for i in range(0, nb_parties):
            print(i)
            self.run_double_Monte_Carlo(joueur1, joueur2)
            self.reset()
            joueur1.reset_nb_coup()
            joueur2.reset_nb_coup()

    # distribution joueur monte vs joueur random
    def distribution_monteVSrandom(self, monte, random, nb_parties):
        for i in range(0, nb_parties):
            self.run_monteVSrandom(monte, random)
            self.reset()
            monte.reset_nb_coup()
            random.reset_nb_coup()

#### Partie 3 ####
class Bandits_manchots:

    def __init__(self, nb_action, nb_partie, List_modele=0 ):
        # nb de parties à simuler partie 3
        self.nb_levier = nb_action
        if( List_modele == 0 ) : self.L_rendement = l = [random() for i in range(nb_action)]
        else : self.L_rendement = List_modele
        self.t = nb_partie

    #### Partie 3 ####
    def actu_regret(self, time, count, count_best, l_regret, l_time):
        l_time.append(time)
        l_regret.append(count_best-count)


    def gain_binaire(self ,L, a ): # Renvoie le résultat d'un tirage de bernoulli
        r = L[a] # ( rendement )
        tirage = uniform(0,1) # tirage nombre réel entre 0 et 1
        if tirage <= r : # succès
            return 1
        else :
            return 0

    def algo_alea(self, L_recompense, cpt_levier = {} ): # L est vide et contient le rendement de chaque action
        l_time = list()
        timer = 0
        l_regret = list()
        count_best = 0 # compteur de meilleur cas à t
        count = 0 # compteur action random au temps tirage
        best_indice = np.argmax(self.L_rendement) # levier ayant le meilleur rendement
        for i in range(0, self.t):
            count_best += self.gain_binaire(self.L_rendement, best_indice)
            a_aleat = randint(0, self.nb_levier-1) # action à jouer choisie aléatoirement
            stock = self.gain_binaire(self.L_rendement, a_aleat)
            L_recompense[a_aleat] += stock
            count += stock
            self.actu_regret(timer, count, count_best, l_regret, l_time)
            timer+=1

        plt.plot(l_time, l_regret)
        plt.title("regret en fonction du temps algorithme aléatoire")
        plt.ylabel("regret")
        plt.xlabel("temps")
        plt.show()
        return count_best - count

    def algo_greed(self, L_recompense, cpt_levier = {} ):
        count_best = 0
        count = 0
        best_indice = np.argmax(self.L_rendement) # levier ayant le meilleur rendement
        for i in range(self.t//3):
            x = randint(0, self.nb_levier-1)
            count_best += self.gain_binaire(self.L_rendement, best_indice)
            stock = self.gain_binaire(self.L_rendement, x)
            count += stock
            L_recompense[x] += stock
        best_to_play = np.argmax(L_recompense) # meilleure levier dans la nouvelle liste de rendement

        for i in range(0, self.t-(self.t//3)):
            count_best += self.gain_binaire(self.L_rendement, best_indice)
            stock = self.gain_binaire(self.L_rendement, best_to_play)
            count += stock
            self.L_rendement[best_to_play] += stock
        return (count_best - count, best_to_play)



    def algo_greed_courbe(self, L_recompense, cpt_levier = {} ):
        l_regret = list()
        l_time = list()
        timer = 0
        count_best = 0
        count = 0
        best_indice = np.argmax(self.L_rendement) # levier ayant le meilleur rendement
        for i in range(self.t//3):
            x = randint(0, self.nb_levier-1)
            count_best += self.gain_binaire(self.L_rendement, best_indice)
            stock = self.gain_binaire(self.L_rendement, x)
            count += stock
            L_recompense[x] += stock
            self.actu_regret(i, count, count_best, l_regret, l_time)
            timer+=1
        best_to_play = np.argmax(L_recompense) # meilleure levier dans la nouvelle liste de rendement

        for i in range(0, self.t-(self.t//3)):
            count_best += self.gain_binaire(self.L_rendement, best_indice)
            stock = self.gain_binaire(self.L_rendement, best_to_play)
            count += stock
            self.L_rendement[best_to_play] += stock
            self.actu_regret(timer, count, count_best, l_regret, l_time)
            timer+=1

        plt.plot(l_time, l_regret)
        plt.title("regret en fonction du temps algorithme greedy")
        plt.ylabel("regret")
        plt.xlabel("temps")
        plt.show()
        return (count_best - count, best_to_play)


    def algo_e_greed(self, L_recompense, nb=0):
        l_regret = list()
        l_time = list()
        timer = 0
        eps = 0.1
        self.t
        count_best = 0
        count = 0
        best_indice = np.argmax(self.L_rendement) # levier ayant le meilleur rendement

        for i in range(self.t//3):
            x = randint(0, self.nb_levier-1) # levier aleat deter
            count_best += self.gain_binaire(self.L_rendement, best_indice) # on incrémente le compteur de gain plus opti
            stock = self.gain_binaire(self.L_rendement, x) # determiner une action aléatoire
            count += stock # on incrémente le compteur de gain pour action aleat
            L_recompense[x] += stock
            self.actu_regret(timer, count, count_best, l_regret, l_time)
            timer+=1

        for x in range(0, self.t-(self.t//3)):
            # best action
            count_best += self.gain_binaire(self.L_rendement, best_indice)
            rand = random()
            if rand < eps :
                x = randint(0, self.nb_levier-1)
                stock = self.gain_binaire(self.L_rendement, x)
                count += stock
                L_recompense[x] += stock
                self.actu_regret(timer, count, count_best, l_regret, l_time)
                timer+=1
            else :
                (gain_diff, to_play)= self.algo_greed(L_recompense)
                y = self.gain_binaire(self.L_rendement, to_play)
                count += y
                L_recompense[to_play] += y
                self.actu_regret(timer, count, count_best, l_regret, l_time)
                timer+=1

        plt.plot(l_time, l_regret)
        plt.title("regret en fonction du temps algorithme E-greedy")
        plt.ylabel("regret")
        plt.xlabel("temps")
        plt.show()
        return count_best - count

    def algo_ucb(self, L_recompense, L_played):
        l_regret = list()
        l_time = list()
        timer = 0
        count = 0
        count_best = 0
        best_indice = np.argmax(self.L_rendement)
        nb_coup_tot = 0

        for x in range(0,len(self.L_rendement)): # on suppose que tous les coups ont été joue au moins une fois
            L_played[x]=1
            nb_coup_tot += 1

        for i in range(self.t//3): # exploration
            x = randint(0, self.nb_levier-1)
            count_best += self.gain_binaire(self.L_rendement, best_indice)
            stock = self.gain_binaire(self.L_rendement, x)
            count += stock
            L_played[x] += 1
            L_recompense[x] += stock
            nb_coup_tot += 1
            self.actu_regret(timer, count, count_best, l_regret, l_time)
            timer+=1


        for i in range(len(L_played)): # apply formule
            L_recompense[i] = (L_recompense[i]/nb_coup_tot) + sqrt( 2 * log(nb_coup_tot)/ L_played[i])
        to_play = np.argmax(L_recompense)

        for x in range(0, self.t-(self.t//3)):
            count_best += self.gain_binaire(self.L_rendement, best_indice)
            count += self.gain_binaire(self.L_rendement, to_play)
            self.actu_regret(timer, count, count_best, l_regret, l_time)
            timer+=1

        plt.plot(l_time, l_regret)
        plt.title("regret en fonction du temps algorithme UCB")
        plt.ylabel("regret")
        plt.xlabel("temps")
        plt.show()
        return count_best-count


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


plateau = Plateau( ligne, colonne )
joueur1 = Joueur(1)
joueur2 = Joueur(-1)
#---------------------------------------------------------------- PARTIE : 1 ----------------------------------------------------------------


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

# # Distribution joueur monte carlo vs joueur à tirage aléatoire
# plateau.distribution_monteVSrandom(joueur1, joueur2, nb_parties)

# # listes avec le nombre de coup de chaque victoire
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


# # Distribution joueur monte carlo vs joueur monte carlo
# plateau.distribution_monteVSmonte(joueur1, joueur2, nb_parties)
# # listes avec le nombre de coup de chaque victoire
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


#---------------------------------------------------------------- PARTIE : 3 ----------------------------------------------------------------

# nb iterations pour l'exploration pour algo greed
nb_tirage = 100

# nombre de parties à jouer
T = 200

# Nombre d'actions possibles
taille_action = 100

# determiner le nombre de fois Maximum que l'on peut jouer un levier
max_lev = 100


# nombre de fois ou chaque levier a ete joue
## def __init__(self, nb_action, nb_partie, List_modele=0 )


bandit = Bandits_manchots(100, 1000) # en 3 eme arg la List

list_alea = [0 for i in range(bandit.nb_levier)]
list_greed = [0 for i in range(bandit.nb_levier)]
list_e_greed = [0 for i in range(bandit.nb_levier)]
list_ucb = [0 for i in range(bandit.nb_levier)]

list_cpt_alea = [0 for i in range(bandit.nb_levier)]
list_cpt_greed = [0 for i in range(bandit.nb_levier)]
list_cpt_e_greed = [0 for i in range(bandit.nb_levier)]
list_cpt_ucb = [0 for i in range(bandit.nb_levier)]



# print(bandit.algo_alea(list_alea))
# (x,y) = bandit.algo_greed_courbe(list_greed)
# print(x)
# print(bandit.algo_e_greed(list_e_greed))
for i in range(10):
    print(bandit.algo_ucb(list_ucb, list_cpt_ucb))