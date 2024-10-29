import numpy as np
import matplotlib.pyplot as plt
from pyomo.environ import *

# Definir el solver
solver = SolverFactory('ipopt')

# Crear el modelo concreto
Model = ConcreteModel()

# Definir la variable 'a' con límites entre 0 y 350
Model.a = Var(domain=NonNegativeReals, bounds=(0, 350))

# Definir las expresiones de ventas unitarias y beneficio como variables
Model.v = Var(domain=Reals)
Model.b = Var(domain=Reals)

# Definir restricciones para que las expresiones sean consistentes con las ecuaciones originales
def ventas_unitarias_rule(model):
    return model.v == 890 - 3.8*model.a + 20*(model.a + 0.01)**0.5

def beneficio_rule(model):
    return model.b == -1.444*(model.a**2) + 7.6*((model.a + 0.01)**1.5) + 80*((model.a + 0.01)**0.5) + 322*model.a + 3560

# Añadir las restricciones al modelo
Model.ventas_unitarias_constr = Constraint(rule=ventas_unitarias_rule)
Model.beneficio_constr = Constraint(rule=beneficio_rule)

# Definir una función de objetivo que maximice el beneficio
Model.max_b = Objective(expr=Model.b, sense=maximize)

# Resolver el modelo una vez para obtener el valor máximo y mínimo de b
solver.solve(Model)
max_b = Model.b.value
max_v = Model.v.value

# Ahora cambiaremos la función de objetivo para ponderar entre b y v
pareto = []

# Borrar el objetivo actual
del Model.max_b

# Crear un rango de pesos
w = np.linspace(0, 1, 10)

# Definir el nuevo objetivo multiobjetivo ponderado
for i in w:
    # Ponderación entre beneficio y ventas unitarias
    Model.obj = Objective(expr=i * Model.b + (1 - i) * Model.v, sense=maximize)
    
    # Resolver el modelo
    solver.solve(Model)
    
    # Guardar los puntos de la frontera de Pareto
    pareto.append((Model.b.value, Model.v.value))
    
    # Borrar el objetivo anterior para actualizarlo en la siguiente iteración
    del Model.obj

# Convertir los resultados de Pareto en arrays
pareto = np.array(pareto)

# Graficar la frontera de Pareto
plt.figure(figsize=(8, 6))
plt.plot(pareto[:, 0], pareto[:, 1], '-o', label="Frontera de Pareto")
plt.xlabel('Beneficio (b)')
plt.ylabel('Ventas unitarias (v)')
plt.title('Frontera de Pareto entre Beneficio y Ventas Unitarias')
plt.legend()
plt.grid(True)
plt.show()