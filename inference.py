#!/usr/bin/env python3

"""
Script para hacer predicciones usando un modelo entrenado.

Uso:
    python inference.py --input data/test.csv --model models/best_random_forest_model.pkl --output data/predictions.csv

Este script:
1. Lee un archivo CSV con datos sin procesar.
2. Aplica el preprocesamiento usando `process_raw_data()`.
3. Carga un modelo `pickle` ya entrenado.
4. Hace predicciones con el modelo y las guarda en `predictions.csv`.
"""

import argparse
import pickle
import pandas as pd
import os
import numpy as np
from src.preprocessing.process_data import process_raw_data


def load_model(model_path):
    """
    Carga un modelo serializado en formato pickle.

    :param model_path: Ruta del archivo pickle (.pkl) del modelo entrenado.
    :return: Modelo cargado.
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"ERROR: El archivo de modelo '{model_path}' no existe.")

    try:
        with open(model_path, "rb") as file:
            model = pickle.load(file)
        print(f"Modelo cargado desde: {model_path}")
        return model
    except Exception as e:
        raise RuntimeError(f"ERROR al cargar el modelo: {e}")


def make_predictions(input_file, model_file, output_file):
    """
    Procesa un CSV de entrada, carga un modelo y genera predicciones.

    :param input_file: Ruta del CSV de entrada sin procesar.
    :param model_file: Ruta del modelo serializado en pickle.
    :param output_file: Ruta del CSV donde se guardarán las predicciones.
    """
    # Validar archivo de entrada
    if not os.path.exists(input_file):
        raise FileNotFoundError(
            f"ERROR: El archivo de entrada '{input_file}' no existe.")

    try:
        # 1. Preprocesar los datos de entrada (test)
        processed_file = "temp_processed.csv"  # Archivo temporal
        process_raw_data(input_file, processed_file)

        # 2. Cargar datos preprocesados de test
        df_processed = pd.read_csv(processed_file)
        if df_processed.empty:
            raise ValueError(
                "ERROR: El DataFrame procesado está vacío. Revisa el preprocesamiento."
            )

        # 3. Cargar el DataFrame 'prep.csv' con el que se entrenó el modelo
        #    (ya tiene las columnas exactas que el modelo vio en training).
        train_df = pd.read_csv("data/prep.csv")
        if train_df.empty:
            raise ValueError(
                "ERROR: El DataFrame de entrenamiento (prep.csv) está vacío o no se cargó correctamente."
            )

        # --- Alinear columnas ---
        # Quitar columnas que no sean features en train_df (por ejemplo, 'Id' y 'SalePrice').
        # Dejas SOLO las columnas que se usaron como features en el entrenamiento.
        train_features = train_df.drop(
            columns=["Id", "SalePrice", "SalePrice_Log"], errors="ignore")

        # Para el DataFrame de test preprocesado (df_processed), también
        # quitamos 'Id' y 'SalePrice' (en caso de que exista 'SalePrice').
        X_test = df_processed.drop(
            columns=["Id"], errors="ignore")

        # Alinear para que X_test tenga exactamente las mismas columnas que train_features.
        train_features, X_test = train_features.align(
            X_test, join="left", axis=1)

        # Rellenar con 0 los valores NaN que aparezcan en X_test
        X_test = X_test.fillna(0)

        # 4. Cargar modelo entrenado
        model = load_model(model_file)

        # 5. Hacer predicciones con X_test (ya alineado)
        predictions_log = model.predict(X_test)

        # 6. Revertir la funcion logaritmica
        predictions = np.expm1(predictions_log)

        # 7. Guardar predicciones en un CSV
        #    Usamos la columna "Id" de df_processed, si está presente.
        df_predictions = pd.DataFrame({
            "Id": df_processed.get("Id", range(len(predictions))),
            "SalePrice_Predicted": predictions
        })
        df_predictions.to_csv(output_file, index=False)

        print(f"Archivo procesado guardado en: {processed_file}")
        print(f"Predicciones guardadas en: {output_file}")

    except FileNotFoundError as fnf_error:
        print(fnf_error)
    except ValueError as val_error:
        print(val_error)
    except Exception as e:
        print(f"ERROR inesperado: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Realiza predicciones usando un modelo entrenado.")
    parser.add_argument("--input", type=str, required=True,
                        help="Ruta del archivo CSV de entrada sin procesar.")
    parser.add_argument("--model", type=str, required=True,
                        help="Ruta del modelo entrenado en formato .pkl.")
    parser.add_argument("--output", type=str, default="predictions.csv",
                        help="Ruta del archivo CSV de salida con predicciones.")

    args = parser.parse_args()

    try:
        make_predictions(args.input, args.model, args.output)
    except Exception as e:
        print(f"ERROR: {e}")
