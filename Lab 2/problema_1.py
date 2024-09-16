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
hasta = ["Cali", "Bquilla", "Pasto", "Tunja", "Chía", "Manizales", "Bogotá"]

#Conjunto
demanda = {1:125,2:175,3:225, 4:250, 5:225, 6:200, 7:50}
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
results = SolverFactory('glpk').solve(Model)

Model.display()

#Análisis de sensibilidad

print("\nAnálisis de sensibilidad")
for i, constr in enumerate(Model.lista1):
    print(f"Oferta desde orígen {desde[i]} = {-Model.dual[Model.lista1[i+1]]}")

for i, constr in enumerate(Model.lista2):
    print(f"Demanda en destino {hasta[i]} = {-Model.dual[Model.lista2[i+1]]}")


print("\n")
if 'ok' in str(results.Solver.status):    
    print("Cliente      Demanda   Enviado    Margen")
    for i, destino_name in enumerate(hasta):
        total_enviado = sum(Model.x[i+1, j]() for j in origen)
        print(f"{destino_name:10s}{demanda[i+1]:10.1f}{total_enviado:10.1f}{Model.dual[Model.lista2[i+1]]:10.4f}")
else:
    print("No Valid Solution Found")


