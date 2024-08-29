from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory

Model = ConcreteModel()

# Data de entrada
ciudadesDestino = 6
ciudadOrigen = 2

destino=RangeSet(1, ciudadesDestino)
origen=RangeSet(1, ciudadOrigen)

#Conjunto
demanda = {1:125,2:175,3:225, 4:250, 5:225, 6:200}
oferta = {1:550, 2:700}
bogota = {1:999, 2:2.5, 3:1.6, 4:1.4, 5:1.6, 6:1.4}
medellin = {1:2.5, 2:999, 3:2.0 , 4:1.0, 5:1.0, 6:0.8}

# Variable de decisión
Model.x = Var(destino, origen, domain=NonNegativeReals)

# Función objetivo
Model.obj = Objective(expr = sum(Model.x[i,j]*ganancia[i] for i in p for j in q), sense=maximize)

# Restricciones
Model.lista1 = ConstraintList()
for j in q:
   Model.lista1.add(sum(Model.x[i,j]*horas[i] for i in p) <= workers[j]) 

Model.lista2 = ConstraintList()
for i in p:
    Model.lista2.add(sum(Model.x[i,k] for k in q) == 1) 


# Especificación del solver
SolverFactory('glpk').solve(Model)

Model.display()


