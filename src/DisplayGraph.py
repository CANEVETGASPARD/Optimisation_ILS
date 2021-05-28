#librairy
import numpy as np
import random as rd
import matplotlib.pyplot as plt

"try to display a graph -> not finished"
#variables
number_of_vertex=5
edge=np.array(np.zeros([number_of_vertex,number_of_vertex]))

def graphe(vertex, link,xmin,xmax,ymin,ymax): # --> vertex: int, link: matrix
    L=VertexLocation(vertex,xmin,xmax,ymin,ymax) # --> (liste des pos x, liste des pos y)
    plt.scatter(L[0],L[1])
    decalage=0.1
    for k in range(vertex) : #boucle pour faire apparaitre les numeros des points
        plt.text(L[0][k]+decalage,L[1][k], k)
    plt.show()


"""fonction qui retourne une liste de position aléatoire pour les sommets"""
def VertexLocation(vertex, xmin,xmax,ymin,ymax): # -->vertex, xmin, xmax, ymin, ymax: int
    Lx=[] #liste des positions x des sommets
    Ly=[] #liste des positions y des sommets
    for i in range(0,vertex) :
        x= rd.randint(xmin,xmax) #on donne des positions aléatoire au sommets
        y=rd.randint(ymin,ymax)
        Lx.append(x) #on ajoute la position à la liste
        Ly.append((y))
    return (Lx, Ly)

graphe(number_of_vertex,edge,1,10,1,10)