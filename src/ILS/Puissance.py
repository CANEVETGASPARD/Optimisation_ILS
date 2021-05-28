'''fonction qui verifie si on est en bout de branche ou non'''
def Present_in_x(j,x) : #en argument on le sommet d'arrivé x et l'ensemble des branches formant notre arbre
    present=False #on part du principe que le sommet n'est pas présent une autre fois dans notre arbre
    other = [] #on part du principe qu'on n'a pas de tuple à garder en mémoire
    for k in x: #on parcout toutes les branches de notre arbres
        if(j==k[0]): #si il est deja présent
            present=True
            other.append(k) #on garde en mémoire le tuple
    return (present,other)

'''on va maintenant calculer les puissance entrante correspondant à notre chemin'''
def Power_in(x,delta,etha) : #en argument on a que la liste de tupe qui correspon à notre arbre
    if(type(x)==str): #si on a retourné une erreur avec le calcul de x
        return "On ne peut pas calculer la puissance car on n'a pas une liste de branche en entrée"
    else:
        P_in={} #dictionnaire qui a en clé le tupe (i,j) et en argument la puissance associé
        for k in range(0,len(x)) :
            tupleij=x[len(x)-k-1] #on part du dernier tuple pour partir d'un sommet qui correspond à un bout de branche
            present_in=Present_in_x(tupleij[1],x) #on applique la fonction present_in à notre tupleij
            present=present_in[0] #on initialise le booleen qui verifie la presence de tupleij[j] dans l'arbre
            other_tuple=present_in[1] #on extrait la liste des tuples où il est présent dans l'arbre
            if(present) : #si il est deja present dans l'arbre on lui applique la formule suivante
                P_out=0 #si le sommet en question à plusieur enfant il faut calculer la somme des puissances à fournir
                for l in range(0,len(other_tuple)):
                    P_out+=P_in[other_tuple[l]]
                P_in[tupleij]=(P_out+delta[tupleij])/etha[tupleij]
            else : #si il est en bout de branche il n'a pas de puissance de sortie et donc on a la formule suivante
                P_in[tupleij]=delta[tupleij]/etha[tupleij]
        return P_in #on renvoie le dictionnaire de puissance

