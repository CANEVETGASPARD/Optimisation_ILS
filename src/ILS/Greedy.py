from copy import deepcopy as dc
from Puissance import Power_in
from Starter_tree import Possible_vertice


"""On va construitre notre premier arbre à l'aide d'un algo basique, on va partir de la source et relié le plus proche et ainsi de suite"""
"""les algo greedy ne marche pas dans le cas de petite dimension en effet pour la version 1 on ne respecte pas les contraintes"""

"""fonction pour verifier si on respecte la contrainte 5"""
def possible_contrainte5(P_in,C_max):
    possible = True  # variable pour savoir si on respecte la contrainte 5
    for key in P_in:  # boucle pour verifier que l'on valide la contrainte 5
        if P_in[key] > C_max[key]:
            possible = False
    return possible


"""dans le cas de la version 2 on est bloqué par les sommets à la fin du code si ils sont trop loin de la source est donc que la puissance à fournir est trop grande"""
def greedyV2(init_vertice,number_of_vertice, etha, delta,C_max,l):
    start_vertice=init_vertice #on initialise le sommet de départ
    greedy_tree=[] #on créer la liste dans laquel on va rajouter les différentes branche de notre arbre
    possible_vertice=Possible_vertice(number_of_vertice,[init_vertice]) #on créer un liste des sommets possible à rencontrer
    impossible_vertice=[] #liste dans laquelle on va rajouter les sommets invisitable
    while (len(greedy_tree)<number_of_vertice-1): #tant qu'on a pas atteint l'objectid de 7 branches on arrete pas la boucle
        arrival_vertice=possible_vertice[0] #on initialise le sommet potentielement le plus proche
        dist=l[(start_vertice,arrival_vertice)] #on calcul la distance entre les deux sommets
        for i in possible_vertice: #on effetue une boucle pout tous les sommet encore ateignable ie ce qui n'ont pas encore effectué de laison
            if (dist>l[(start_vertice,i)]): #si il est plus proche
                arrival_vertice=i
                dist=l[start_vertice,i] #il devient le sommet le proche
        P_in=Power_in(greedy_tree+[(start_vertice,arrival_vertice)],delta,etha) #on calcule la puissance entrante avec l'arbre deja présent
        possible=possible_contrainte5(P_in,C_max) # variable pour savoir si on respecte la contrainte 5
        if (possible) : #si c'est possible alors on rajoute la branche à notre arbre
            greedy_tree.append((start_vertice,arrival_vertice)) #on ajoute la branche à la liste quand la boucle de comparaison est terminé
            possible_vertice.remove(arrival_vertice) #on enlève le sommet d'arrivé au sommet encore ateignable
            start_vertice=arrival_vertice #il devient ensuite le sommet de départ
        else :  #si c'est pas possible on rajoute le sommet d'arrivé au sommet impossible
            impossible_vertice.append(arrival_vertice) #on rajoute le sommet à la liste des sommets impossibles
            possible_vertice.remove(arrival_vertice)  # on enlève le sommet d'arrivé au sommet encore ateignable
        if (len(possible_vertice)==0) : #si aucun sommet restant ne peut etre relié alors on repart du sommet initial
            if(start_vertice==init_vertice): #si on a le sommet de départ qui est deja égal au sommet source c'est qu'on ne peut pas relier le sommet à la source et donc que le greedy n'est pas applicable
              greedy_tree="Le greedy n'est pas applicable sur notre système" #on va donc sortir de la boucle car len(greedy_tree)>7 et renvoyer une erreur
              possible_vertice = dc(impossible_vertice)  # on reinitialise les sommets ateignables et les sommets impossibles
              impossible_vertice = []
            else:
                start_vertice=init_vertice
                possible_vertice=dc(impossible_vertice) #on reinitialise les sommets ateignables et les sommets impossibles
                impossible_vertice=[]
    return greedy_tree #une fois les 7 branches définies on retourne la liste des branches

