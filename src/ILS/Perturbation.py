from copy import deepcopy as dc
import random as rd
from Total_cost import Cost
from Local_search import Creation_Hubs_Spokes_List

def presence(itox,xtoi):
    present=False
    for i in range(len(itox)):
        if(itox[i]==xtoi):
            present=True
    return present

def verrif_position_vertice(X,Vi1,Vi2,V0): #fonction qui permet de verifier que les 2 sommets choisi ne sont pas séparé par le même sommet car cela engendrerait un cycle ou que un de sommets n'est pas la source
    possible=True
    if(Vi1==V0): #si un des sommets est la source c'est pas possibles
        possible=False
    elif(Vi2==V0):
        possible=False
    else:
        i1tox=[]
        i2tox=[]
        for key in X:  # on va chercher les sources et les laisons des deux sommets
            if (key[0] == Vi1):
                i1tox.append(key[1])
            if (key[1] == Vi1):
                xtoi1=key[0]
            if (key[0] == Vi2):
                i2tox.append(key[1])
            if (key[1] == Vi2):
                xtoi2=key[0]
        if(presence(i1tox,xtoi2)): #si ils sont séparer par un même sommet
            possible=False
        elif(presence(i2tox,xtoi1)):
            possible=False
    return possible

def vertice_choice(X,hubs,V0): #fonction retourne les deux sommets auxquels on va echanger les propriétés
    N=len(hubs)
    i1=rd.randrange(N) #on initialise les deux sommets
    i2=rd.randrange(N)
    Vi1=hubs[i1]
    Vi2=hubs[i2]
    possible=verrif_position_vertice(X,Vi1,Vi2,V0)
    while(Vi1==Vi2 or possible==False): #tant que les sommets sont identique ou qu"ils sont séparés par un même sommet ou qu'ils sont égals à la source
        i1 = rd.randrange(N) #on recommence
        i2 = rd.randrange(N)
        Vi1 = hubs[i1]
        Vi2 = hubs[i2]
        possible = verrif_position_vertice(X, Vi1, Vi2,V0)
    return Vi1,Vi2

def arrival_research(X,V): #fonction qui renvoie la liste des sommets auquels le sommet V est relié
    arrival=[]
    for i in range(len(X)) : #on balaye X
        if (X[i][0]==V): #quand on a trouvé le sommet
            arrival.append((i,X[i][1])) #on rajoute le sommet d'arrivé à la liste
    return arrival

def source_research(X,V1,V2):
    for i in range(len(X)): #on recherche les sources
        if(X[i][1]==V1):
            sourceV1=X[i][0]
            indexsourceV1=i
        if(X[i][1]==V2):
            sourceV2=X[i][0]
            indexsourceV2=i

    if (sourceV1==V2): #On prend en compte les cas ou les sommets choisis peuvent être relié
        return (sourceV2,indexsourceV1),(V1,indexsourceV2)
    elif(sourceV2==V1):
        return (V2,indexsourceV1),(sourceV1,indexsourceV2)
    else : #sinon on retourne les 2 sources
        return (sourceV2,indexsourceV1),(sourceV1,indexsourceV2)

def perturbation(X,D, p_umd, alpha, c_var, l, c_fix, c_om, betta, T_flh,c_heat,c_rev, v0,nombre_V,lambd,delta,etha):
    new_X=dc(X)
    hubs=Creation_Hubs_Spokes_List(new_X)[0]
    V1,V2=vertice_choice(new_X,hubs,v0) #on définie les deux sommets à modifier
    arrivalV1=arrival_research(new_X,V1) #on determine les listes des sommets dont ils sont la source
    arrivalV2=arrival_research(new_X,V2)
    (new_sourceV1,indexV1),(new_sourceV2,indexV2)=source_research(new_X,V1,V2) #on cherche les sommets qui leurs sont sources
    for k1 in range(len(arrivalV1)): #on echange leurs sommets d'arrivés
        new_X[arrivalV1[k1][0]]=(V2,arrivalV1[k1][1])
    for k2 in range(len(arrivalV2)):
        new_X[arrivalV2[k2][0]]=(V1,arrivalV2[k2][1])
    new_X[indexV2]=(new_sourceV1, V1)  # on echange leurs source
    new_X[indexV1]=(new_sourceV2, V2)
    new_T_cost=Cost(new_X,D, p_umd, alpha, c_var, l, c_fix, c_om, betta, T_flh,c_heat,c_rev, v0,nombre_V,lambd,delta,etha) #on recalcul le cout total
    new_hubs_spokes=Creation_Hubs_Spokes_List(new_X)
    new_hubs=new_hubs_spokes[0]
    new_spokes=new_hubs_spokes[1]
    return new_X,new_T_cost,new_hubs,new_spokes
