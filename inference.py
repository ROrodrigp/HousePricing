#!/usr/bin/env python3

"""
Script para hacer predicciones usando un modelo entrenado.

Uso:
    python predict.py --input data/test.csv --model best_random_forest_model.pkl --output predictions.csv

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
        # 1. Preprocesar los datos
        processed_file = "temp_processed.csv"  # Archivo temporal
        process_raw_data(input_file, processed_file)

        # 2. Cargar datos preprocesados
        df_processed = pd.read_csv(processed_file)

        if df_processed.empty:
            raise ValueError(
                "ERROR: El DataFrame procesado está vacío. Revisa el preprocesamiento.")

        # 3. Cargar modelo entrenado
        model = load_model(model_file)

        # 4. Hacer predicciones
        # Eliminar ID si está presente
        X = df_processed.drop(columns=["Id"], errors="ignore")

        if X.empty:
            raise ValueError(
                "ERROR: No hay columnas predictoras después del preprocesamiento.")

        predictions = model.predict(X)

        # 5. Guardar predicciones en un CSV
        df_predictions = pd.DataFrame({
            # Si no hay Id, se genera un índice
            "Id": df_processed.get("Id", range(len(predictions))),
            "SalePrice_Predicted": predictions
        })
        df_predictions.to_csv(output_file, index=False)

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
