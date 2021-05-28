from Puissance import Power_in

def Possible_vertice(number_of_vertice,list_of_impossible_vertice): #va construire une liste avec les sommets ateignables
    possible_vertice=[]  #on intialise la liste de sommet
    for k in range(1,number_of_vertice+1): #on va balayer l'ensemble des sommets
        if k not in list_of_impossible_vertice: #si le sommet n'est pas un sommet inateignable
            possible_vertice.append(k) #on le rajoute à notre liste
    return possible_vertice

def respect_of_contraint5(impossible_vertices,starter_tree,delta,etha,C_max) : #verifie si on respecte la contrainte 5
    P_in = Power_in(starter_tree, delta, etha) #on calcul les puissance P_in pour l'arbre en arguemnt
    possible = True #on suppose que de base il n'y a pas de problème avec cette arbre
    for key in P_in: #on va maintenant verifier u'il n'y a pas de problème
        if P_in[key] > C_max[key]: #si on ne respecte pas la condition
            possible = False #alors on dit que le pronlème est impossible
            impossible_vertices.append(key[1]) #on rajoute le sommet qui pose problème à la liste des sommets impossibles
            starter_tree.remove(key) #on enlève la branche de l'arbre deja construit
    return possible #on renvoie si la contrainte 5 est respecté


def Starter_tree(init_vertice,number_of_vertice,delta,etha,C_max) :
    starter_tree=[] #arbre dans lequel on va ajouter les branches
    impossible_vertices=[] #list ou on rajoute les sommets qui ne peuvent pas etre relié à init_vertice
    possible_vertices_global=Possible_vertice(number_of_vertice,[init_vertice]) #list des sommets reliable à la source
    for k in possible_vertices_global: #on relie tous les sommets à la source
        starter_tree.append((init_vertice,k))
    possible1=respect_of_contraint5(impossible_vertices,starter_tree,delta,etha,C_max) #on verifie que l'on respecte la contrainte 5
    if(possible1==False): #si non
        for i in impossible_vertices: #on va modifier les liens pour les sommets qui ne marche pas
            possible_vertices_i=Possible_vertice(number_of_vertice,[init_vertice,i]) #on créer la liste des sommets ateignables en enlevant le sommet de départ et le sommets que l'on traite pour eviter de prendre le chemin (4,4) par exemple
            possible2 = False  # on part du principe que aucun sommet ne marche
            for j in possible_vertices_i: #on parcourt ces sommets
                if (respect_of_contraint5([],starter_tree+[(j,i)],delta,etha,C_max)): #si un un des sommets respecte la contrainte 5, in s'en fout ici de rajouter les sommets qui ne marchent pas car seul les sommets qui marchent nous interresse
                    start_vertice=j; #on initialise start vertice
                    possible2=True; #on dit qu'il existe au moins une solution
            if(possible2): #si une solution existe on la rajoute à l'arbre
                starter_tree.append((start_vertice,i))
            else : #si non on renvoie une erreur
                starter_tree ="il n'y pas de telle solution pour notre problème"
    return starter_tree