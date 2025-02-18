#!/usr/bin/env python3


"""
Entrenamiento y serialización de un modelo RandomForestRegressor.

Este script entrena un modelo de regresión usando RandomForestRegressor,
optimiza los hiperparámetros mediante GridSearchCV y serializa el mejor
modelo utilizando pickle.
"""

import pickle
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import mean_absolute_error

input = "data/prep.csv"

df = pd.read_csv(input)

# Definir X (variables predictoras) y y (variable objetivo transformada)
# Eliminamos la variable objetivo y el Id
X = df.drop(columns=['SalePrice_Log', 'SalePrice', 'Id'])
y = df['SalePrice_Log']  # Usamos la versión transformada como objetivo

# Dividir en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Definir el modelo base
model = RandomForestRegressor(random_state=60)

# Definir la cuadrícula de hiperparámetros para la búsqueda
param_grid = {
    'n_estimators': [100, 200, 300],  # Número de árboles en el bosque
    'max_depth': [10, 20, None],  # Profundidad máxima del árbol
    'min_samples_split': [2, 5, 10],  # Mínimo de muestras para dividir un nodo
    'min_samples_leaf': [1, 2, 4]  # Mínimo de muestras en una hoja
}

# Configurar la búsqueda con validación cruzada
grid_search = GridSearchCV(
    estimator=model,
    param_grid=param_grid,
    # Optimizar para MAE (Mean Absolute Error)
    scoring='neg_mean_absolute_error',
    cv=5,  # Validación cruzada con 5 folds
    n_jobs=-1,  # Usar todos los núcleos de la CPU
    verbose=2,
    return_train_score=True  # Ver scores de entrenamiento
)

# Ejecutar Grid Search
grid_search.fit(X_train, y_train)

# Obtener el mejor modelo
best_model = grid_search.best_estimator_

# Evaluar en el conjunto de prueba
y_pred = best_model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f"MAE del mejor modelo en test set: {mae:.4f}")

# Guardar el modelo serializado con pickle
model_filename = "best_random_forest_model.pkl"
with open(model_filename, "wb") as file:
    pickle.dump(best_model, file)

print(f"Modelo guardado como {model_filename}")
