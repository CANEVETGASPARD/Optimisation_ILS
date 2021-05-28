import pandas as pd
from Total_cost import Cost
from Starter_tree import Starter_tree
from Local_search import local_search_new, Creation_Hubs_Spokes_List
from Perturbation import perturbation
import matplotlib.pyplot as plt



InputData = "../../Dataset/InputDataEnergySmallInstance.xlsx"

# Input Data Preparation #
def read_excel_data(filename, sheet_name):
    data = pd.read_excel(filename, sheet_name=sheet_name, header=None)
    values = data.values
    if min(values.shape) == 1:  # This If is to make the code insensitive to column-wise or row-wise expression #
        if values.shape[0] == 1:
            values = values.tolist()
            if len(values[0]) == 1:
                return values[0][0]
        else:
            values = values.transpose()
            values = values.tolist()
            if len(values[0]) == 1:
                return values[0][0]
        return values[0]
    else:
        data_dict = {}
        if min(values.shape) == 2:  # For single-dimension parameters in Excel
            if values.shape[0] == 2:
                for i in range(values.shape[1]):
                    data_dict[i + 1] = values[1][i]
            else:
                for i in range(values.shape[0]):
                    data_dict[i + 1] = (values[i][0], values[i][1])

        else:  # For two-dimension (matrix) parameters in Excel
            for i in range(values.shape[0]):
                for j in range(values.shape[1]):
                    data_dict[(i + 1, j + 1)] = values[i][j]
        return data_dict


"""Calcul la distance entre les différents sommets"""
def length_of_edge_definition(vertice_position) :# -->disctionnaire avec en clé le sommet et en valeur la position
    L={}
    for key1 in vertice_position :
        for key2 in vertice_position :
            L[(key1,key2)]= ((vertice_position[key1][0]-vertice_position[key2][0])**(2) +(vertice_position[key1][1]-vertice_position[key2][1])**(2))**(1/2)
    return L

"""calcul de delta"""
def delta_definition(d,betta,lambd,l,theta_fix) : # --> dictionnaire en clé le sommet et en valeur le delta associé
    delta={}
    for key in d :
        delta[key] = d[key]*lambd*betta + l[key]*theta_fix[key]
    return  delta

"""calcul de etha"""
def etha_definition(l,theta_var) : #--> dictionnaire avec en clé le sommet et en valeur le etha assoié (le rendement quoi)
    etha={}
    for key in l :
        etha[key]= 1 - l[key]*theta_var[key]
    return etha

def ILS( D, p_umd, alpha, c_var, l, c_fix, c_om, betta, T_flh,c_heat,c_rev, v0,nombre_V,lambd,delta,etha,repetitionLS,repetitionILS):
    t_cost_list=[]
    optimized_tree = Starter_tree(v0, nombre_V, delta, etha, C_max)
    T_cost = Cost(optimized_tree, D, p_umd, alpha, c_var, l, c_fix, c_om, betta, T_flh, c_heat, c_rev, v0, nombre_V,lambd, delta, etha)
    t_cost_list.append(T_cost)
    local_search=local_search_new(optimized_tree,repetitionLS,T_cost,D, p_umd, alpha, c_var, l, c_fix, c_om,betta, T_flh, c_heat, c_rev, v0, nombre_V, lambd, delta, etha,C_max)
    optimized_tree_etoile=local_search[0]
    optimized_tree_etoile_cost=local_search[1]
    optimized_tree_etoile_hubs=local_search[2]
    optimized_tree_etoile_spokes=local_search[3]
    for k in range(repetitionILS):
        optimized_tree_prime=perturbation(optimized_tree_etoile,D,p_umd, alpha, c_var, l, c_fix, c_om,betta, T_flh, c_heat, c_rev, v0, nombre_V, lambd, delta, etha)
        perturbation_tree=optimized_tree_prime[0]
        perturbation_cost=optimized_tree_prime[1]
        local_search = local_search_new(perturbation_tree, repetitionLS, perturbation_cost, D, p_umd, alpha, c_var, l, c_fix, c_om,betta, T_flh, c_heat, c_rev, v0, nombre_V, lambd, delta, etha,C_max)
        optimized_tree_prime_etoile = local_search[0]
        optimized_tree_prime_etoile_cost = local_search[1]
        optimized_tree_prime_etoile_hubs = local_search[2]
        optimized_tree_prime_etoile_spokes = local_search[3]
        t_cost_list.append(optimized_tree_prime_etoile_cost)
        #acceptance
        if(optimized_tree_etoile_cost>optimized_tree_prime_etoile_cost):
            optimized_tree_etoile=optimized_tree_prime_etoile
            optimized_tree_etoile_cost=optimized_tree_prime_etoile_cost
            optimized_tree_etoile_hubs=optimized_tree_prime_etoile_hubs
            optimized_tree_etoile_spokes=optimized_tree_prime_etoile_spokes

    return optimized_tree_etoile, optimized_tree_etoile_cost,optimized_tree_etoile_hubs,optimized_tree_etoile_spokes,t_cost_list




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

# liste de tuple qui contient le tree optimisé
'''on commence par l'initialiser  avec un algo greedy'''
#optimized_tree=[(4,1),(4,2),(4,5),(4,7),(4,8),(2,3),(7,6)]
'''
"""variable avec l'algo starter_tree"""
optimized_tree=Starter_tree(v0,nombre_V, delta, etha,C_max)
optimized_tree_Spokes_Hubs=Creation_Hubs_Spokes_List(optimized_tree)
hubs=optimized_tree_Spokes_Hubs[0]
spokes=optimized_tree_Spokes_Hubs[1]
T_cost=Cost(optimized_tree, D, p_umd, alpha, c_var, l, c_fix, c_om, betta, T_flh,c_heat,c_rev, v0,nombre_V,lambd,delta,etha)
print("x: ",optimized_tree)
print("Hubs", hubs, "Spokes",spokes)
print("total cost : ",T_cost)
print()

repetition=100

local_search=local_search_new(optimized_tree,repetition,T_cost,D, p_umd, alpha, c_var, l, c_fix, c_om,betta, T_flh, c_heat, c_rev, v0, nombre_V, lambd, delta, etha)
local_search_tree=local_search[0]
local_search_cost=local_search[1]
local_search_hubs=local_search[2]
local_search_spokes=local_search[3]
print('x_local_search',local_search_tree)
print("Hubs :",local_search_hubs,"Spokes",local_search_spokes)
print("local search cost : ",local_search_cost)
print()

optimized_tree_perturbation=perturbation(local_search_tree,local_search_hubs,local_search_spokes,D,p_umd, alpha, c_var, l, c_fix, c_om,betta, T_flh, c_heat, c_rev, v0, nombre_V, lambd, delta, etha)
perturbation_tree=optimized_tree_perturbation[0]
perturbation_cost=optimized_tree_perturbation[1]
perturbation_hubs=optimized_tree_perturbation[2]
perturbation_spokes=optimized_tree_perturbation[3]
print('x_perturbation',perturbation_tree)
print("Hubs :",perturbation_hubs,"Spokes",perturbation_spokes)
print("local search cost : ",perturbation_cost)
print()'''


'''
print("-----------------------------------greedy------------------------------------")
"""varaible avec l'algo greedy"""
optimized_tree_greedy=greedyV2(v0,nombre_V, etha, delta,C_max,l)
optimized_tree_greedy_Spokes_Hubs=Creation_Hubs_Spokes_List(optimized_tree_greedy)
greedy_hubs=optimized_tree_greedy_Spokes_Hubs[0]
greedy_spokes=optimized_tree_greedy_Spokes_Hubs[1]
T_cost_greedy=Cost(optimized_tree_greedy, D, p_umd, alpha, c_var, l, c_fix, c_om, betta, T_flh,c_heat,c_rev, v0,nombre_V,lambd,delta,etha)
print("x_greedy :", optimized_tree_greedy)
if(type(optimized_tree_greedy)!=str):
    print("Hubs",greedy_hubs , "Spokes",greedy_spokes)
print
print("total cost : ",T_cost_greedy)
print()
repetition=50

local_search_greedy=local_search_existing(optimized_tree_greedy,repetition,T_cost,D, p_umd, alpha, c_var, l, c_fix, c_om,betta, T_flh, c_heat, c_rev, v0, nombre_V, lambd, delta, etha)
local_search_tree_greedy=local_search_greedy[0]
local_search_cost_greedy=local_search_greedy[1]
local_search_hubs_greedy=local_search_greedy[2]
local_search_spokes_greedy=local_search_greedy[3]
print('x_local_search',local_search_tree_greedy)
print("Hubs :",local_search_hubs_greedy,"Spokes",local_search_spokes_greedy)
print("local search cost : ",local_search_cost_greedy)'''

COST=[]
"""On zpplique notre algo ILS"""

repetitionLS=100 #repetition dans le local search
repetitionILS=70 #repetition dans l'ils
ILS=ILS( D, p_umd, alpha, c_var, l, c_fix, c_om, betta, T_flh,c_heat,c_rev, v0,nombre_V,lambd,delta,etha,repetitionLS,repetitionILS)
optimized_tree=ILS[0]
T_cost=ILS[1]
hubs=ILS[2]
spokes=ILS[3]
t_cost_list=ILS[4]
print("x: ",optimized_tree)
print("Hubs", hubs, "Spokes",spokes)
print("total cost : ",T_cost)
plt.title("Cost evolution")
plt.xlabel("iteration")
plt.ylabel("Cost")
plt.plot(t_cost_list)
plt.show()