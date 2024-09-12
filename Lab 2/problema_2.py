from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory
import pandas as pd

Model = ConcreteModel()

# Data de entrada
localidades = 5
viajeros = 2


locs=RangeSet(0, localidades)
traverlers = RangeSet(1,viajeros)

#Conjunto
df = pd.read_csv('Lab 2\proof_case.csv')

#Variable de decisión
Model.x = Var(locs, locs, domain= Binary)

#Variable Auxiliar
Model.u = Var(locs, traverlers,domain=Binary)

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


