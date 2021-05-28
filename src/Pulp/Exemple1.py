from pulp import LpVariable, LpStatus, LpProblem, LpMaximize, value

if __name__ == "main":
    """exemple number1"""

#create the decision variables
x1 = LpVariable('x1', lowBound=0, cat='Continous')
x2 = LpVariable('x2', lowBound=0, cat='Continous')
x3 = LpVariable('x3', lowBound=0, cat='Continous')



#create the problem1 to contain the problem data
example1 = LpProblem('example1', LpMaximize)

#the objective function is added to 'pb1' first
example1 += 3*x1 + 2*x2 + x3

#the constraints are added to 'pb1'

example1 += x1 + 2*x2 == 12
example1 += x2 == 5
example1 += x1 + x2 + 3*x3 == 10


#example1 is solved using Pulp'"s choice of solver
# (the default solver is Coin Cbc)
example1.solve()

#The status of the solution is printed to screen
print("Status", LpStatus[example1.status])

for v in example1.variables():
    print(v.name, "=", v.varValue)

print("Objective value Example 1 =", value(example1.objective))