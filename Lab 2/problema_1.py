from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory

Model = ConcreteModel()
Model.dual = Suffix(direction=Suffix.IMPORT)

# Data de entrada
ciudadesDestino = 6
ciudadOrigen = 2

destino=RangeSet(1, ciudadesDestino)
origen=RangeSet(1, ciudadOrigen)

#Variable Auxiliar

desde = ["Bogotá", "Medellín"]
hasta = ["Cali", "Barranquilla", "Pasto", "Tunja", "Chía", "Manizales."]

#Conjunto
demanda = {1:125,2:175,3:225, 4:250, 5:225, 6:200}
oferta = {1:550, 2:700}
costos = {1:{1:999, 2:2.5}, 2:{1:2.5, 2:999}, 3: {1:1.6, 2:2.0}, 4:{1:1.4, 2:1.0}, 5:{1:0.8, 2:1.0}, 6:{1:1.4, 2:0.8}}

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

#Análisis de sensibilidad

# print("\nSensitivity Analysis")
# print(f"Oferta desde orígen = {-Model.dual[Model.lista1]}")
# print(f"Demanda en destino = {-Model.dual[Model.lista2]}")

print("\nAnálisis de sensibilidad")
for i, constr in enumerate(Model.lista1):
    print(f"Oferta desde orígen {desde[i]} = {-Model.dual[Model.lista1[i+1]]}")

for i, constr in enumerate(Model.lista2):
    print(f"Demanda en destino {hasta[i]} = {-Model.dual[Model.lista2[i+1]]}")


