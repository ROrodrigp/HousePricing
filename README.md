# House Prices Prediction

Este repositorio contiene un flujo de trabajo completo para la predicción del precio de viviendas, utilizando Python, pandas y scikit-learn. Incluye:
	•	Scripts para preprocesamiento de datos.
	•	Entrenamiento de un modelo Random Forest (u otros modelos si lo deseas).
	•	Inferencia (predicción) sobre nuevos datos.

## Estructura del proyecto 
.
|-- data
|   |-- data_description.txt      # Descripción original del dataset (opcional)
|   |-- predictions.csv           # Ejemplo de archivo con predicciones generadas
|   |-- prep.csv                  # Dataset procesado (listo para entrenamiento)
|   |-- raw.csv                   # Datos sin procesar (versión inicial)
|   |-- sample_submission.csv     # Ejemplo de CSV con formato de entrega (opcional)
|   |-- test.csv                  # Datos de prueba sin procesar
|   `-- train.csv                 # Datos de entrenamiento sin procesar
|
|-- inference.py                  # Script principal para hacer inferencia
|-- models
|   `-- best_random_forest_model.pkl  # Modelo entrenado en formato pickle
|
|-- notebooks
|   |-- tarea2_house_princing.ipynb   # Jupyter Notebook con análisis/experimentación
|   `-- testing_prep.ipynb           # Jupyter Notebook para testear el preprocesamiento
|
|-- prep.py                     # Script para lanzar preprocesamiento (opcional)
|
|-- src
|   |-- predictions
|   |   `-- predictions_utils.py  # Funciones para cargar modelo y hacer predicciones
|   |-- preprocessing
|   |   `-- process_data.py       # Lógica de preprocesamiento en alto nivel
|   `-- tools
|       |-- tools_clean_data.py
|       |-- tools_encoders.py
|       `-- tools_engine_variables.py
|       
|-- temp_processed.csv          # Archivo temporal con datos procesados
|
|-- test_data
|   |-- userdata.csv
|   `-- userdata2.csv
|
`-- train.py                    # Script para entrenar el modelo

## Explicacion breve de cada carpeta 

	•	data:
Contiene los archivos CSV originales (train.csv, test.csv) y los resultados/artefactos (prep.csv, predictions.csv).
	•	models:
Carpeta donde se guardan los modelos entrenados (por ejemplo, ficheros .pkl con sklearn).
	•	notebooks:
Notebooks de Jupyter con pruebas, experimentos y/o exploración.
	•	src:
	•	predictions: Código para la etapa de inferencia.
	•	preprocessing: Código de preprocesamiento de datos que se llama desde scripts externos.
	•	tools: Módulos auxiliares (funciones limpias, encoders, transformaciones, etc.).
	•	test_data:
Datos de prueba no oficiales para testear localmente.
	•	train.py:
Script (opcional) para entrenar el modelo.
	•	inference.py:
Script para generar predicciones con el modelo entrenado (best_random_forest_model.pkl).