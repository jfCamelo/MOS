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
costos = {1:{1:999, 2:2.5}, 2:{1:2.5, 2:999}, 3: {1:1.6, 2:2.0}, 4:{1:1.4, 2:1.0}, 5:{1:1.6, 2:1.0}, 6:{1:1.4, 2:0.8}}

# Variable de decisión
Model.x = Var(destino, origen, domain=NonNegativeReals)

# Función objetivo
Model.obj = Objective(expr = sum(Model.x[i,j]*costos[i][j] for i in destino for j in origen), sense=minimize)

# Restricciones
Model.lista1 = ConstraintList()
for j in origen:
   Model.lista1.add(sum(Model.x[i,j] for i in destino) <= oferta[j]) 

Model.lista2 = ConstraintList()
for i in destino:
    Model.lista2.add(sum(Model.x[i,j] for j in origen) == demanda[i]) 


# Especificación del solver
SolverFactory('glpk').solve(Model)

Model.display()


