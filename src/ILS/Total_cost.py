from Puissance import Power_in

'''on va maintenant calculer le coût totale de notre sytème
pour cela il nous faut calculer tous les coût et revenu intermediare'''


'''1 : Revenue'''
def revenue(lambd, D, c_rev, x_var):
    rev = 0
    for key in x_var:
        rev += D[key] * c_rev[key]
    return lambd * rev

#print("revenue : ",revenue(lambd,D,c_rev,optimized_tree))

'''2 : Heat generation Cost'''
def hgc(betta, P_in, T_flh, c_heat, v0):
    hgc=0
    for key in P_in:
        if(key[0]==v0):
            hgc += P_in[key]*c_heat[v0-1]
    return (1/betta)*T_flh*hgc

#print("heat generation cost : ",hgc(betta,P_in,T_flh,c_heat,v0))

'''3 : Mainteance Cost'''
def mc(x, c_om, l):
    mc=0
    for key in x :
        mc += c_om[key]*l[key]
    return mc

#print("mainteance cost : ",mc(optimized_tree,c_om,l))

'''4 : Fixed Invest Cost'''
def fic(alpha, x, c_fix, l):
    fic=0
    for key in x:
        fic += l[key]
    return c_fix*alpha*fic

#print("fixed invest cost : ",fic(alpha,optimized_tree,c_fix,l))

'''5 : Variable Invest Cost'''
def vic(alpha, P_in, c_var, l):
    vic=0
    for key in P_in:
        vic += c_var[key]*l[key]*P_in[key]
    return alpha*vic

#print("variable Invest Cost : ",vic(alpha,P_in,c_var,l))

'''6 : Unmet Demand Penalty'''
def udp(x, D, p_umd,nombre_V):
    udp=0
    for i in range(1,nombre_V+1):
        for j in range(1,nombre_V+1):
            if(j!=i):
                key_ = (i,j)
                _key = (j,i)
                if ((key_ in x) or (_key in x)) :
                    x_value=1
                else :
                    x_value=0
                udp += (1- x_value)*D[key_]*p_umd[key_]
    return (1/2)*udp

#print("Unmet Demand Penalty : ",udp(optimized_tree,D,p_umd))


'''Calcul du coût totale'''
def Cost(x, D, p_umd, alpha, c_var, l, c_fix, c_om, betta, T_flh,c_heat,c_rev, v0,nombre_V,lambd,delta,etha) :
    P_in=Power_in(x,delta,etha)
    if(type(x)==str):
        return "On ne peut pas calculer le cout car on n'a pas une liste de branche en entrée"
    else:
        return hgc(betta, P_in, T_flh, c_heat, v0) + mc(x, c_om, l) + fic(alpha, x, c_fix, l) + vic(alpha, P_in, c_var, l) + udp(x, D, p_umd,nombre_V) - revenue(lambd, D, c_rev, x)