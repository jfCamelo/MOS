
from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory

Model = ConcreteModel()

# Data de entrada
tareas=5
trabajadores=3

p=RangeSet(1, tareas)
q=RangeSet(1, trabajadores)

trabajadores={1:8,2:10,3:6}
ganancia={1:50, 2:60, 3:40, 4:70, 5:30}
horas={1:4, 2:5, 3:3, 4:6, 5:2}

# Variable de decisión
Model.x = Var(p,q,domain=Binary)

# Función objetivo
Model.obj = Objective(expr = sum(Model.x[i,j]*ganancia[i] for i in p for j in q), sense=maximize)

# Restricciones
for j in range(1,3):
    Model.res1 = Constraint(expr = sum(Model.x[i,j]*horas[i] for i in p) <= trabajadores[j])

for i in p:
    Model.res2 = Constraint(expr = sum(Model.x[i,k] for k in q) == 1)


# Especificación del solver
SolverFactory('glpk').solve(Model)

Model.display()


