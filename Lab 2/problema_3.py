from pyomo.environ import *

# Variables
localizaciones = ["L1", "L2", "L3", "L4", "L5", "L6", "L7", "L8", "L9", "L10", "L11", "L12"]
sensores = ["S1", "S2", "S3"]

# Parámetros
energia = {"S1": 7, "S2": 4, "S3": 8}
instalacion = {"L1": 250, "L2": 100, "L3": 200, "L4": 250, "L5": 300, "L6": 120, "L7": 170,
               "L8": 150, "L9": 270, "L10": 130, "L11": 100, "L12": 230}
comunicacion = {
    "L1": {"S1": 48, "S2": 49, "S3": 31},
    "L2": {"S1": 38, "S2": 33, "S3": 34},
    "L3": {"S1": 24, "S2": 12, "S3": 36},
    "L4": {"S1": 17, "S2": 31, "S3": 37},
    "L5": {"S1": 30, "S2": 11, "S3": 25},
    "L6": {"S1": 48, "S2": 33, "S3": 24},
    "L7": {"S1": 28, "S2": 39, "S3": 12},
    "L8": {"S1": 32, "S2": 47, "S3": 46},
    "L9": {"S1": 20, "S2": 11, "S3": 16},
    "L10": {"S1": 20, "S2": 30, "S3": 30},
    "L11": {"S1": 33, "S2": 42, "S3": 18},
    "L12": {"S1": 45, "S2": 21, "S3": 48}
}
adyas = {
    'L1': ['L1', 'L2', 'L3', 'L5'],
    'L2': ['L1', 'L2', 'L5'],
    'L3': ['L1', 'L3', 'L4', 'L5', 'L6', 'L7', 'L8'],
    'L4': ['L3', 'L4', 'L5', 'L6', 'L11'],
    'L5': ['L1', 'L2', 'L3', 'L4', 'L5', 'L10', 'L11'],
    'L6': ['L3', 'L4', 'L6', 'L8', 'L11'],
    'L7': ['L3', 'L7', 'L8', 'L12'],
    'L8': ['L3', 'L6', 'L7', 'L8', 'L9', 'L11', 'L12'],
    'L9': ['L8', 'L9', 'L10', 'L11', 'L12'],
    'L10': ['L5', 'L9', 'L10', 'L11'],
    'L11': ['L4', 'L5', 'L6', 'L8', 'L9', 'L10', 'L11', 'L12'],
    'L12': ['L7', 'L8', 'L9', 'L11', 'L12']
}
sens_locs = {
    "L1": {"S1": 1, "S2": 0, "S3": 1},
    "L2": {"S1": 1, "S2": 0, "S3": 1},
    "L3": {"S1": 1, "S2": 0, "S3": 1},
    "L4": {"S1": 1, "S2": 1, "S3": 0},
    "L5": {"S1": 1, "S2": 1, "S3": 1},
    "L6": {"S1": 1, "S2": 1, "S3": 1},
    "L7": {"S1": 1, "S2": 0, "S3": 1},
    "L8": {"S1": 1, "S2": 1, "S3": 1},
    "L9": {"S1": 1, "S2": 1, "S3": 1},
    "L10": {"S1": 1, "S2": 1, "S3": 0},
    "L11": {"S1": 1, "S2": 1, "S3": 1},
    "L12": {"S1": 1, "S2": 0, "S3": 1}
}

# Lista de sensores
sens = ["S1", "S2", "S3"]

# Crear y resolver un modelo para cada sensor
for sensor in sens:
    # Crear el modelo
    model = ConcreteModel()

    # Variables de decisión
    model.x = Var(localizaciones, within=Binary)

    # Función objetivo
    def objetivo(model):
        return sum(model.x[loc] * (energia[sensor] + instalacion[loc] + comunicacion[loc][sensor]) for loc in localizaciones)
    model.objetivo = Objective(rule=objetivo, sense=minimize)

    ### Restricciones
    # Restricción de "or": una localización debe tener un sensor o una localización adyacente debe tenerlo
    def restriccion_or(model, loc):
        if sens_locs[loc][sensor] == 1:
            return model.x[loc] + sum(model.x[adyacente] for adyacente in adyas[loc]) >= 1
        else:
            return Constraint.Skip
    model.restriccion_or = Constraint(localizaciones, rule=restriccion_or)

    # Resolver el modelo
    solver = SolverFactory('glpk')
    solver.solve(model)

    # Mostrar la solución para el sensor actual
    solucion_sensor = [loc for loc in localizaciones if model.x[loc].value == 1]
    print(f"Solución para el sensor {sensor}: {solucion_sensor}")
