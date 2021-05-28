# -*- coding: utf-8 -*-
"""
Created on Thu May 14 16:17:39 2020

@author: lucie
"""


# Import PuLP modeler functions
from pulp import LpStatus,LpVariable,LpProblem,LpMinimize,value,lpSum
import pandas as pd





InputData = "../../Dataset/InputDataEnergySmallInstance.xlsx"

  # Input Data Preparation #
def read_excel_data(filename, sheet_name):
  data = pd.read_excel(filename, sheet_name=sheet_name, header=None)
  values = data.values
  if min(values.shape) == 1:  # This If is to make the code insensitive to column-wise or row-wise expression #
      if values.shape[0] == 1:
          values = values.tolist()
          if len(values[0])==1:
              return values[0][0]
      else:
          values = values.transpose()
          values = values.tolist()
          if len(values[0])==1:
              return values[0][0]
      return values[0]
  else:
      data_dict = {}
      if min(values.shape) == 2:  # For single-dimension parameters in Excel
          if values.shape[0] == 2:
              for i in range(values.shape[1]):
                  data_dict[i+1] = values[1][i]
          else:
              for i in range(values.shape[0]):
                  data_dict[i+1] = (values[i][0],values[i][1])

      else:  # For two-dimension (matrix) parameters in Excel
          for i in range(values.shape[0]):
              for j in range(values.shape[1]):
                  data_dict[(i+1, j+1)] = values[i][j]
      return data_dict


     ### Paramètres ###

def length_of_edge_definition(vertice_position) :# -->disctionnaire avec en clé le sommet et en valeur la position
    L={}
    for key1 in vertice_position :
        for key2 in vertice_position :
            L[(key1,key2)]= ((vertice_position[key1][0]-vertice_position[key2][0])**(2) +(vertice_position[key1][1]-vertice_position[key2][1])**(2))**(1/2)
    return L

def delta_definition(d,betta,lambd,l,theta_fix) : # --> dictionnaire en clé le sommet et en valeur le delta associé
    delta={}
    for key in d :
        delta[key] = d[key]*lambd*betta + l[key]*theta_fix[key]
    return  delta

def etha_definition(l,theta_var) : #--> dictionnaire avec en clé le sommet et en valeur le etha assoié (le rendement quoi)
    etha={}
    for key in l :
        etha[key]= 1 - l[key]*theta_var[key]
    return etha



#Les intersections et leurs coordonnées
V = read_excel_data(InputData, "NodesCord")
nombre_V = read_excel_data(InputData, "Nodes")

#L'usine et le prix de génération de la chaleur
v0 = read_excel_data(InputData, "SourceNum")
c_heat = read_excel_data(InputData, "cheat(ciheat)")

#Les pertes thermiques fixes et variables en fontion de i et j
theta_fix = read_excel_data(InputData, "vfix(thetaijfix)")
theta_var = read_excel_data(InputData, "vvar(thetaijvar)")

#Les investissements fixes et variables
c_fix = read_excel_data(InputData, "FixedUnitCost")     
c_var = read_excel_data(InputData, "cvar(cijvar)")

#Le prix de maintenance
c_om = read_excel_data(InputData, "com(cijom)")

#Revenu en € par kWh en fonction de i et j
c_rev = read_excel_data(InputData, "crev(cijrev)")

#Nombre d'heures de production
T_flh = read_excel_data(InputData, "Tflh(Tiflh)")

#L'effet de concurrence, le quota de connexion et le facteur de rente
betta = read_excel_data(InputData, "Betta")
lambd = read_excel_data(InputData, "Lambda")
alpha = read_excel_data(InputData, "Alpha")
if (InputData == "../../Dataset/InputDataEnergySmallInstance.xlsx"): #pour palier à l'erreur lors du chargement d'alpha -> liste avec la valeur et des Nan et non juste la valeur
    alpha = alpha[0]

#Le pic de demande et la demande annuelle
d = read_excel_data(InputData, "EdgesDemandPeak(dij)")      #en kWh
D = read_excel_data(InputData, "EdgesDemandAnnual(Dij)") 

#Capacité maximale des canalisations
C_max = read_excel_data(InputData, "Cmax(cijmax)")

#Capacité maximale de production de la source
Q_max = read_excel_data(InputData, "SourceMaxCap(Qimax)")

#Pénalité en cas de demande non-atteinte
p_umd = read_excel_data(InputData, "pumd(pijumd)")

#longueur des canalisation calculé en faisant pythagore
l=length_of_edge_definition(V)

#delta et etha
delta=delta_definition(d,betta,lambd,l,theta_fix)
etha=etha_definition(l,theta_var)

print(l)
print(delta)
print(etha)



  ### Decision Variables ###

x = LpVariable.dicts('x',[(i,j) for i in V for j in V],lowBound=0, cat='Binary')

P_in = LpVariable.dicts('P_in', [(i,j) for i in V for j in V], lowBound=0, cat='Continuous')

P_out = LpVariable.dicts('P_out', [(i,j) for i in V for j in V], lowBound=0, cat='Continuous')




def revenue(lambd, D, c_rev, x_var):
    
    rev=0
    for key in x_var:
        rev += D[key]*c_rev[key]*x_var[key]
    return lambd*rev


def hgc(betta, P_in, T_flh, c_heat, v0,nombre_V):     #heat_generation_cost
    hgc=0
    for j in range(1,nombre_V+1):
        if(j!=v0):
            hgc += P_in[(v0,j)]*c_heat[v0-1]
    return (1/betta)*T_flh*hgc


def mc(x, c_om, l):                         #maintenance_cost
    mc=0
    for key in x :
        mc += x[key]*c_om[key]*l[key]
    return mc



def fic(alpha, x, c_fix, l):                #fixed_investment_cost
    fic=0
    for key in x:
        fic += x[key]*l[key]
    return c_fix*alpha*fic


def vic(alpha, x, P_in, c_var, l):          #variable_investment_cost
    vic=0
    for key in x:
        vic += c_var[key]*l[key]*P_in[key]
    return alpha*vic

def udp(x, D, p_umd):                       #unmet_demand_penalty
    udp=0
    for i in range(1,nombre_V+1):
        for j in range(1,nombre_V+1):
            if(j!=i):
                key_ = (i,j)
                _key = (j,i)
                udp += (1- x[key_]- x[_key])*D[key_]*p_umd[key_]
    return (1/2)*udp


dho = LpProblem("dho",LpMinimize)
dho += hgc(betta, P_in, T_flh, c_heat, v0,nombre_V) + mc(x, c_om, l) + fic(alpha, x, c_fix, l) + vic(alpha, x, P_in, c_var, l) + udp(x, D, p_umd) - revenue(lambd, D, c_rev, x)


"""Constraints"""

"""Contraint 1"""
dho += lpSum(x[(i,j)] for i in range(1, nombre_V+1) for j in range(1,nombre_V+1) if (i!=j)) <= nombre_V-1 #la je sais pas si c'est utilse de diferencier i et j vu qu'on les utilises tout le temps avant

"""contraint 2"""
for i in range(1,nombre_V+1) :
    for j in range(1,nombre_V+1) :
        if(i!=j)and (i<j): #la contrainte (i<j) permet d'eviter la redondance des equations du à la symetrie des arguments des x (i,j) et (j,i)
            dho+= x[(i,j)] + x[(j,i)] <=1


"""contraint 3"""
for i in range(1,nombre_V+1):
    for j in range(1,nombre_V+1):
        if(i!=j):
            dho+= etha[(i,j)]*P_in[(i,j)] - P_out[(i,j)] == delta[(i,j)]*x[(i,j)]

"""contraint 4"""
for j in range(1,nombre_V+1) :
    sumin=0
    sumout=0
    if (j!=v0) :
        for i in range(1,nombre_V+1) :
            if (j!=i):
                sumin+=P_in[(j,i)]
                sumout+=P_out[(i,j)]
        dho += sumin - sumout ==0



"""contraint 5"""
for i in range(1,nombre_V+1):
    for j in range(1,nombre_V+1):
        if (i!=j):
            dho+= P_in[(i,j)] <=x[(i,j)]*C_max[(i,j)]


"""contraint 6"""
dho+= lpSum(x[(i,v0)] for i in range(1,nombre_V+1) if(i!=v0)) ==0


"""contraint 7"""
dho+= lpSum(P_in[(v0,j)] for j in range(1,nombre_V+1) if(j!=v0)) <= Q_max[v0]

"""contraint 8"""
for j in range(1, nombre_V+1) :
    if (j!=v0) :
        sum=0
        for i in range(1,nombre_V+1) :
            if(i!=j):
                sum+= x[(i,j)]
    dho+= sum ==1

"""contraint8bis"""
dho+= lpSum(x[(v0,j)] for j in range(1,nombre_V+1) if(j!=v0)) >=1

print(dho)
"""contraint 9"""
#elle est effectué lors de la définition des variables décisionnelles


### then we resolve the problem ###

# the problem is solved
dho.solve()

#the status of the solution is printed
print("Status", LpStatus[dho.status])

#the optimal value of the decision varaibles and the
#optimised objective function values is printed
for v in dho.variables():
    print(v.name, "=", v.varValue)

print("objective Value dho = ", value(dho.objective))