from copy import deepcopy as dc
import random as rd
from Total_cost import Cost
from Starter_tree import respect_of_contraint5

def Creation_Hubs_Spokes_List(X) :
    if (type(X)==str):
        return "On ne peut pas construire les listes Hubs et Spokes car on n'a pas une liste de branche en entrée"
    else:
        hubs=[]
        spokes=[]
        for branche in range(0,len(X)):
            i=X[len(X)-branche-1][0] #on part de la fin pour commencer par un sommet j qui est un spoke
            j=X[len(X)-branche-1][1]
            if i not in hubs: #pour eviter les redondances
                hubs.append(i)
            if j not in spokes and j not in hubs : #pour eviter les redondances et les sommets qui sont des hubs
                spokes.append(j)

        return hubs,spokes


def Single_spoke_to_a_new_hub(X, hubs, spokes, T_cost, D, p_umd, alpha, c_var, l, c_fix, c_om, betta, T_flh,c_heat,c_rev, v0,nombre_V,lambd,delta,etha):
    if(len(spokes)>1):
        new_X=dc(X) #on copie les liste X, hubs et spokes pour pas les modifier
        new_hubs=dc(hubs)
        new_spokes=dc(spokes)
        N=len(new_spokes)
        i=rd.randrange(0,N) #on génère un entier aléatoire entre 0 et N-1
        vertice=new_spokes[i] #on récupère le sommet

        if(i==0): #si l'index de vertice est égal à zeros
            min_vertice=new_spokes[1] #on initalise à 1
        else: #sinon on initialise à zéros
            min_vertice=new_spokes[0]

        #on initialise les variables de comparaison du cout
        for key in new_X : #on enlève la branche relié au lien précédent
            if key[1]==vertice:
                new_X.remove(key)
        new_X.append((min_vertice,vertice)) #on rajoute le nouveau lien
        min_cost=Cost(new_X, D, p_umd, alpha, c_var, l, c_fix, c_om, betta, T_flh,c_heat,c_rev, v0,nombre_V,lambd,delta,etha)
        for k in new_spokes: #pour tous les sommets restant
            if((k!=vertice) and (k!=min_vertice)):
                new_X.pop(len(new_X)-1) #on cherche le sommet qui minimise le cout
                new_X.append((k,vertice))
                cost=Cost(new_X, D, p_umd, alpha, c_var, l, c_fix, c_om, betta, T_flh,c_heat,c_rev, v0,nombre_V,lambd,delta,etha)
                if(min_cost>cost):
                    min_vertice=k
                    min_cost=cost
        new_X.pop(len(new_X)-1) #quand on la trouvé on modifie les différentes listes.
        new_X.append((min_vertice,vertice))
        new_hubs.append(min_vertice)
        new_spokes.remove(min_vertice)
        return new_X,new_hubs,new_spokes,min_cost
    else:
        return X,hubs,spokes, T_cost



def local_search_new(X,repetition,T_cost,D, p_umd, alpha, c_var, l, c_fix, c_om,betta, T_flh, c_heat, c_rev, v0, nombre_V, lambd, delta, etha,C_max) :
    min_X=dc(X)
    X_Spokes_Hubs = Creation_Hubs_Spokes_List(min_X)
    hubs = X_Spokes_Hubs[0]
    spokes = X_Spokes_Hubs[1]
    min_T_cost = T_cost
    for k in range(repetition):
        new_system = Single_spoke_to_a_new_hub(min_X, hubs, spokes,min_T_cost, D, p_umd, alpha, c_var, l, c_fix, c_om,betta, T_flh, c_heat, c_rev, v0, nombre_V, lambd, delta, etha)
        new_X = new_system[0]
        new_hubs = new_system[1]
        new_spokes = new_system[2]
        new_T_cost = new_system[3]
        if(min_T_cost>new_T_cost and respect_of_contraint5([],new_X,delta,etha,C_max)):
            min_X=dc(new_X)
            hubs=dc(new_hubs)
            spokes=dc(new_spokes)
            min_T_cost=new_T_cost
    return  min_X,min_T_cost,hubs,spokes



'''
def Single_spoke_to_an_existing_hub(X, hubs, spokes, T_cost, D, p_umd, alpha, c_var, l, c_fix, c_om, betta, T_flh,c_heat,c_rev, v0,nombre_V,lambd,delta,etha):
    if(len(hubs)>1):
        new_X=dc(X) #on copie les liste X, hubs et spokes pour pas les modifier
        new_hubs=dc(hubs)
        new_spokes=dc(spokes)
        N=len(new_spokes)
        i=rd.randrange(0,N) #on génère un entier aléatoire entre 0 et N-1
        vertice=new_spokes[i] #on récupère le sommet

        #on initialise les variables de comparaison du cout
        for key in new_X:  # on enlève la branche relié au lien précédent
            if key[1] == vertice:
                new_X.remove(key)
                initial_vertice=key[0]

        if(initial_vertice==new_hubs[0]): #traite le cas ou le sommet initiale est en premiere position dans la liste des hubs
            min_vertice=new_hubs[1]
        else:
            min_vertice = new_hubs[0]
        new_X.append((min_vertice,vertice))
        min_cost=Cost(new_X, D, p_umd, alpha, c_var, l, c_fix, c_om, betta, T_flh,c_heat,c_rev, v0,nombre_V,lambd,delta,etha)
        for k in new_hubs: #pour tous les sommets restant
            if ((k!=initial_vertice) and (k!=min_vertice)):
                new_X.pop(len(new_X)-1) #on cherche le sommet qui minimise le cout
                new_X.append((k,vertice))
                cost=Cost(new_X, D, p_umd, alpha, c_var, l, c_fix, c_om, betta, T_flh,c_heat,c_rev, v0,nombre_V,lambd,delta,etha)
                if(min_cost>cost):
                    min_vertice=k
                    min_cost=cost
        new_X.pop(len(new_X)-1) #quand on la trouvé on modifie les différentes listes.
        new_X.append((min_vertice,vertice))
        return new_X,new_hubs,new_spokes,min_cost
    else:
        return X,hubs,spokes, T_cost

def local_search_existing(X,repetition,T_cost,D, p_umd, alpha, c_var, l, c_fix, c_om,betta, T_flh, c_heat, c_rev, v0, nombre_V, lambd, delta, etha) :
    min_X=dc(X)
    X_Spokes_Hubs = Creation_Hubs_Spokes_List(min_X)
    hubs = X_Spokes_Hubs[0]
    spokes = X_Spokes_Hubs[1]
    min_T_cost = T_cost
    for k in range(repetition):
        new_system = Single_spoke_to_an_existing_hub(min_X, hubs, spokes,min_T_cost, D, p_umd, alpha, c_var, l, c_fix, c_om,betta, T_flh, c_heat, c_rev, v0, nombre_V, lambd, delta, etha)
        new_X = new_system[0]
        new_hubs = new_system[1]
        new_spokes = new_system[2]
        new_T_cost = new_system[3]
        if(min_T_cost>new_T_cost):
            min_X=dc(new_X)
            hubs=dc(new_hubs)
            spokes=dc(new_spokes)
            min_T_cost=new_T_cost
    return  min_X,min_T_cost,hubs,spokes'''