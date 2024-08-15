
from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory

Model = ConcreteModel()

# Data de entrada
totales=11

p=RangeSet(1, totales)

puntos_historia={1:5, 2:3, 3:13, 4:1, 5:21, 6:2, 7:2, 8:5, 9:8, 10:13, 11:21}
puntos_prioridada={1:7, 2:5, 3:6, 4:3, 5:1, 6:4, 7:6, 8:6, 9:2, 10:7, 11:6}

# Variable de decisión
Model.x = Var(p, domain=Binary)

# Función objetivo
Model.obj = Objective(expr = sum(Model.x[i]*puntos_prioridada[i] for i in p), sense=maximize)

# Restricciones
Model.res1 = Constraint(expr = sum(Model.x[i]*puntos_historia[i] for i in p) <= 52)

# Especificación del solver
SolverFactory('glpk').solve(Model)

Model.display()


