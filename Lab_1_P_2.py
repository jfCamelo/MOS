
from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory

Model = ConcreteModel()

# Data de entrada
totales=5

p=RangeSet(1, totales)

trabajadores={1:8,2:10,3:6}
ganancia={1:50, 2:60, 3:40, 4:70, 5:30}
horas={1:4, 2:5, 3:3, 4:6, 5:2}

# Variable de decisión
Model.x = Var(p, domain=Binary)

# Función objetivo
Model.obj = Objective(expr = sum(Model.x[i]*ganancia[i] for i in p), sense=maximize)

# Restricciones
for j in range(1,3):
    Model.res1 = Constraint(expr = sum(Model.x[i]*horas[i] for i in p) <= trabajadores[j])

# Especificación del solver
SolverFactory('glpk').solve(Model)

Model.display()


