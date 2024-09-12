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
comunication_costs = {1:125,2:175,3:225, 4:250, 5:225, 6:200}
covertura_sensor = {"L1":[1,0,1], "L2":[1,0,1], "L3":[1,0,1], "L4":[1,1,0], "L5":[1,1,1], "L6":[1,1,1], "L7":[1,0,1], "L8":[1,1,1], "L9":[1,1,1], "L10":[1,1,0], "L11":[1,1,1], "L12":[1,0,1]}
adjacencias = {("L1","L1"):1 , ("L1", "L2"):1, ("L1", "L3"):1, ("L1", "L4"):0, ("L1", "L5"):1, 
               ("L1", "L6"):0, ("L1", "L7"):0, ("L1", "L8"):0, ("L1", "L9"):0, ("L1", "L10"):0,
               ("L1", "L11"):0, ("L1", "L12"):0,
               ("L2","L1"):1 , ("L2", "L2"):1, ("L2", "L3"):0, ("L2", "L4"):0, ("L2", "L5"):1, 
               ("L2", "L6"):0, ("L2", "L7"):0, ("L2", "L8"):0, ("L2", "L9"):0, ("L2", "L10"):0,
               ("L2", "L11"):0, ("L2", "L12"):0,
               ("L3","L1"):1 , ("L3", "L2"):0, ("L3", "L3"):1, ("L3", "L4"):1, ("L3", "L5"):1, 
               ("L3", "L6"):1, ("L3", "L7"):1, ("L3", "L8"):1, ("L3", "L9"):0, ("L3", "L10"):0,
               ("L3", "L11"):0, ("L3", "L12"):0,
               ("L4","L1"):0 , ("L4", "L2"):0, ("L4", "L3"):1, ("L4", "L4"):1, ("L4", "L5"):1, 
               ("L4", "L6"):1, ("L4", "L7"):0, ("L4", "L8"):0, ("L4", "L9"):0, ("L4", "L10"):0,
               ("L4", "L11"):1, ("L4", "L12"):0,
               ("L5","L1"):1 , ("L5", "L2"):1, ("L5", "L3"):1, ("L5", "L4"):1, ("L5", "L5"):1, 
               ("L5", "L6"):0, ("L5", "L7"):0, ("L5", "L8"):0, ("L5", "L9"):0, ("L5", "L10"):1,
               ("L5", "L11"):1, ("L5", "L12"):0,
               ("L6","L1"):0 , ("L6", "L2"):0, ("L6", "L3"):1, ("L6", "L4"):1, ("L6", "L5"):0, 
               ("L6", "L6"):1, ("L6", "L7"):0, ("L6", "L8"):1, ("L6", "L9"):0, ("L6", "L10"):0,
               ("L6", "L11"):1, ("L6", "L12"):0,
               ("L7","L1"):0 , ("L7", "L2"):0, ("L7", "L3"):1, ("L7", "L4"):0, ("L7", "L5"):0, 
               ("L7", "L6"):0, ("L7", "L7"):1, ("L7", "L8"):1, ("L7", "L9"):0, ("L7", "L10"):0,
               ("L7", "L11"):0, ("L7", "L12"):1,
               ("L8","L1"):0 , ("L8", "L2"):0, ("L8", "L3"):1, ("L8", "L4"):0, ("L8", "L5"):1, 
               ("L8", "L6"):1, ("L8", "L7"):1, ("L8", "L8"):1, ("L8", "L9"):1, ("L8", "L10"):0,
               ("L8", "L11"):1, ("L8", "L12"):1,
               ("L9","L1"):0 , ("L9", "L2"):0, ("L9", "L3"):0, ("L9", "L4"):0, ("L9", "L5"):0, 
               ("L9", "L6"):0, ("L9", "L7"):0, ("L9", "L8"):1, ("L9", "L9"):1, ("L9", "L10"):1,
               ("L9", "L11"):1, ("L9", "L12"):1,
               ("L10","L1"):0 , ("L10", "L2"):0, ("L10", "L3"):0, ("L10", "L4"):0, ("L10", "L5"):1, 
               ("L10", "L6"):0, ("L10", "L7"):0, ("L10", "L8"):0, ("L10", "L9"):1, ("L10", "L10"):1,
               ("L11", "L11"):1, ("L11", "L12"):0,
               ("L11","L1"):0 , ("L11", "L2"):0, ("L11", "L3"):0, ("L11", "L4"):1, ("L11", "L5"):1, 
               ("L11", "L6"):1, ("L11", "L7"):1, ("L11", "L8"):1, ("L11", "L9"):1, ("L11", "L10"):1,
               ("L10", "L11"):1, ("L10", "L12"):0, 
               ("L12","L1"):0 , ("L12", "L2"):0, ("L12", "L3"):0, ("L12", "L4"):0, ("L12", "L5"):0, 
               ("L12", "L6"):0, ("L12", "L7"):1, ("L12", "L8"):1, ("L12", "L9"):1, ("L12", "L10"):0,
               ("L12", "L11"):0, ("L12", "L12"):1}
energy_costs = {1:7, 2:4, 3:8}
location_costs = {1:250, 2:100, 3:200, 4:250, 5:300, 6:120, 7:170, 8:150, 9:270, 10:130, 11:100, 12:230}


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
