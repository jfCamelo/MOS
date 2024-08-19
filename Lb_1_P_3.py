
from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory

Model = ConcreteModel()

# Data de entrada
Recursos=5 # Recursos
Aviones=3 # Aviones

R=RangeSet(1, Recursos)
A=RangeSet(1, Aviones)

#caracteristicas recursos
val = {1:50, 2:100, 3:120, 4:60, 5:40}
p = {1:15, 2:5, 3:20, 4:18, 5:10}
vol = {1:8, 2:2, 3:10, 4:12, 5:6}

#caracteristicas aviones
c = {1:30, 2:40, 3:50}
cv = {1:25, 2:30, 3:35}

# Variable de decisión
Model.x = Var(R,A,domain=Binary)

# Función objetivo
Model.obj = Objective(expr = sum(Model.x[i,j]*val[i] for i in R for j in A), sense=maximize)

# Restricciones
Model.lista1 = ConstraintList()
Model.lista2 = ConstraintList()
for j in A:
   Model.lista1.add(sum(Model.x[i,j]*p[i] for i in R) <= c[j])
   Model.lista2.add(sum(Model.x[i,j]*vol[i] for i in R) <= cv[j])
   
Model.lista3 = ConstraintList()
Model.lista3.add(Model.x[2,1] == 0)

Model.lista4 = ConstraintList()
for j in A:
    Model.lista4.add((Model.x[3,j]+Model.x[4,j]) <= 1) 

Model.lista5 = ConstraintList()
for i in R:
    Model.lista5.add(sum(Model.x[i,j] for j in A) <= 1)

# Especificación del solver
SolverFactory('glpk').solve(Model)

Model.display()


