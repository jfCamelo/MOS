from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

Model = ConcreteModel()

# Data de entrada
localidades = 5
viajeros = 3


locs=RangeSet(0, localidades)
travelers = RangeSet(1,viajeros)

#Conjunto
df = pd.read_csv('Lab 2\proof_case.csv')
# df = pd.read_csv('MOS\Lab 2\proof_case.csv')
costos = df.to_dict()
costos = {int(k): v for k, v in costos.items()}
costosMatrix = df.values


#Variable de decisión
Model.x = Var(locs, locs, travelers, domain= Binary, initialize=0)

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
        Model.lista1.add(sum(Model.x[i,j,k] for k in travelers for i in locs if i!= j) == 1) # and i!=0
        Model.lista2.add(sum(Model.x[j,i,k] for k in travelers for i in locs if i!= j) == 1) # and i!=0
    else:
        Model.lista5.add(sum(Model.x[i,j,k] for k in travelers for i in locs if i!= j) == sum(Model.x[j,i,k] for k in travelers for i in locs if i!= j))
        

Model.lista3 = ConstraintList()
for k in travelers:
   for i in locs:
       for j in locs:
            if i != j and i != 0 and j != 0:
                Model.lista3.add(Model.u[i,k]-Model.u[j,k]+(localidades)*Model.x[i,j,k] <= (localidades - 1)) 

Model.lista7 = ConstraintList()
for k in travelers:
    for j in locs:
        Model.lista7.add(sum(Model.x[i,j,k] for i in locs if i!= j) == sum(Model.x[j,i,k]  for i in locs if i!= j))

Model.lista4 = ConstraintList()
for k in travelers:
    Model.lista4.add(Model.u[0,k] == 1)

Model.lista6 = ConstraintList()
for k in travelers:
   Model.lista6.add(sum(Model.x[0,j,k] for j in locs if j != 0) == 1)


# Especificación del solver
SolverFactory('glpk').solve(Model)

Model.display()

routes = []
for k in travelers:
    for i in locs:
        for j in locs:
            if i != j and Model.x[i,j,k].value == 1:
                routes.append((i, j))

# Create a directed graph
G = nx.DiGraph()

# Add nodes (locations)
G.add_nodes_from(locs)

# Add edges (routes between locations)
for route in routes:
    G.add_edge(route[0], route[1], weight=costosMatrix[route[0], route[1]])

# Set layout for visualization
pos = nx.spring_layout(G)

# Draw the network graph
plt.figure(figsize=(10, 7))
nx.draw(G, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=14, font_color='black', font_weight='bold', arrows=True)

# Draw the edge labels (costs)
labels = {(i, j): f'{costosMatrix[i,j]:.2f}' for i, j in G.edges()}
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

plt.title("Optimal Travel Routes Between Locations")
plt.show()


