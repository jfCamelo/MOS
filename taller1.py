
from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory

Model = ConcreteModel()

# Data de entrada
grupos_a=4

p=RangeSet(1, grupos_a)
q=RangeSet(1, 5)

calorias={1:287,2:204,3:146,4:245}
proteina={1:26, 2:4.2, 3:8, 4:6}
azucar={1:0, 2:0.01, 3:13, 4:25}
grasa={1:19.3, 2:0.5, 3:8, 4:0.8}
carbohidratos={1:0, 2:44.1, 3:11, 4:55}
precio={1:3000, 2:1000, 3:600, 4:700}

matrix = {1:calorias, 2:proteina, 3:azucar, 4:grasa, 5:carbohidratos}

restriccion_max={1:8000, 2:8000, 3:25, 4:50, 5:200}
restriccion_min={1:1500, 2:63, 3:0, 4:0, 5:0}

# Variable de decisión
Model.x = Var(p,domain=NonNegativeReals)

# Función objetivo
Model.obj = Objective(expr = sum(Model.x[i]*precio[i] for i in p), sense=minimize)

# Restricciones
Model.lista1 = ConstraintList()
Model.lista2 = ConstraintList()
for j in q:
   Model.lista1.add(sum(Model.x[i]*matrix[j][i] for i in p) <= restriccion_max[j])
   Model.lista2.add(sum(Model.x[i]*matrix[j][i] for i in p) >= restriccion_min[j])


# Especificación del solver
SolverFactory('glpk').solve(Model)

Model.display()


