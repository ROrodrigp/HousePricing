#!/usr/bin/env python3

import argparse
import pandas as pd
from src.tools_clean_data import clean_data
from src.tools_encoders import apply_one_hot_encoding, apply_ordinal_encoding
from src.tools_engine_variables import apply_log_transform


def process_raw_data(input_file, output_file):
    """
    Lee un archivo CSV, aplica transformaciones y guarda el resultado en otro archivo.

    :param input_file: Ruta del archivo CSV de entrada (raw.csv).
    :param output_file: Ruta del archivo CSV de salida (prep.csv).
    """
    # Leer el archivo CSV
    df = pd.read_csv(input_file)

    # Aplicar transformaciones
    df = apply_ordinal_encoding(df)
    df = apply_one_hot_encoding(df)
    df = apply_log_transform(df, "SalePrice")
    df = clean_data(df)

    # Guardar el resultado en un nuevo archivo CSV
    df.to_csv(output_file, index=False)

    print(f"Archivo procesado guardado en: {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Procesa datos crudos aplicando transformaciones y guardando el resultado.")
    parser.add_argument("--input", type=str, required=True,
                        help="Ruta del archivo CSV de entrada (raw.csv).")
    parser.add_argument("--output", type=str, required=True,
                        help="Ruta del archivo CSV de salida (prep.csv).")

    # Ejecutar el procesamiento
    args = parser.parse_args()

    process_raw_data(args.input, args.output)
