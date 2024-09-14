from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory
import pandas as pd
import numpy as np

Model = ConcreteModel()

# Data de entrada
localidades = 5
viajeros = 1


locs=RangeSet(0, localidades)
travelers = RangeSet(1,viajeros)

#Conjunto
#df = pd.read_csv('Lab 2\proof_case.csv')
df = pd.read_csv('MOS\Lab 2\proof_case.csv')
costos = df.to_dict()
costos = {int(k): v for k, v in costos.items()}
costosMatrix = df.values


#Variable de decisión
Model.x = Var(locs, locs, travelers, domain= Binary)

#Variable Auxiliar
Model.u = Var(locs, travelers,domain= NonNegativeReals)

# Función objetivo
Model.obj = Objective(expr = sum(Model.x[i,j,k]*costosMatrix[i,j] for i in locs for j in locs for k in travelers), sense=minimize)

# Restricciones

Model.lista1 = ConstraintList()
Model.lista2 = ConstraintList()
Model.lista5 = ConstraintList()
for j in locs:
    if j != 0:
        Model.lista1.add(sum(Model.x[i,j,k] for k in travelers for i in locs if i!= j) == 1)
        Model.lista2.add(sum(Model.x[j,i,k] for k in travelers for i in locs if i!= j) == 1)
    else:
        Model.lista5.add(sum(Model.x[i,j,k] for k in travelers for i in locs if i!= j) == sum(Model.x[j,i,k] for k in travelers for i in locs if i!= j))
        

Model.lista3 = ConstraintList()
for k in travelers:
   for i in locs:
       for j in locs:
            if i != j and i != 0 and j != 0:
                Model.lista3.add(Model.u[i,k]-Model.u[j,k]+(localidades)*Model.x[i,j,k] <= (localidades - 1)) 

Model.lista4 = ConstraintList()
for k in travelers:
    Model.lista4.add(Model.u[0,k] == 1)

#Model.lista4 = ConstraintList()
#for k in travelers:
#    Model.lista4.add(sum(Model.x[0,j,k] for j in locs if j != 0) == 1)


# Especificación del solver
SolverFactory('glpk').solve(Model)

Model.display()


