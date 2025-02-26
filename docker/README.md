# House Pricing - Contenedores Docker

Este proyecto contiene dos contenedores Docker:
1. **Entrenamiento**: Ejecuta `train.py` para entrenar un modelo de Random Forest.
2. **Inferencia**: Ejecuta `inference.py` para generar predicciones con el modelo entrenado.

## Requisitos
Asegúrate de tener instalado:
- [Docker](https://docs.docker.com/get-docker/)
- Un sistema operativo compatible (Linux/Mac/Windows con WSL2)

---

## 1. Construcción de Imágenes Docker

### Construir la imagen para entrenamiento
Ejecuta desde el directorio raíz del proyecto:
```sh
docker build -t train-model -f docker/Dockerfile.train .
```

### Construir la imagen para inferencia
Ejecuta desde el directorio raíz del proyecto:
```sh
docker build -t inference-model -f docker/Dockerfile.inference .
```

Para verificar que las imágenes se crearon correctamente:
```sh
docker images
```
Deberías ver `train-model` e `inference-model` en la lista.

---

## 2. Ejecución de Contenedores

### Ejecutar el contenedor de entrenamiento
```sh
docker run --rm -v $(pwd)/models:/app/models -v $(pwd)/data:/app/data train-model
```

**Explicación:**
- `--rm` → Elimina el contenedor después de ejecutarse.
- `-v $(pwd)/models:/app/models` → Guarda el modelo entrenado en `models/` en la máquina local.
- `-v $(pwd)/data:/app/data` → Permite que `train.py` acceda a `data/prep.csv`.

Si deseas usar un archivo de entrada diferente:
```sh
docker run --rm -v $(pwd)/models:/app/models -v $(pwd)/data:/app/data train-model --input data/custom.csv --output models/custom_model.pkl
```

---

### Ejecutar el contenedor de inferencia
```sh
docker run --rm -v $(pwd)/models:/app/models -v $(pwd)/data:/app/data -v $(pwd)/predictions:/app/output inference-model
```

**Explicación:**
- `--rm` → Elimina el contenedor después de ejecutarse.
- `-v $(pwd)/models:/app/models` → Monta el directorio donde está el modelo entrenado.
- `-v $(pwd)/data:/app/data` → Permite acceder al archivo de entrada (`test.csv`).
- `-v $(pwd)/predictions:/app/output` → Guarda las predicciones en `predictions/` en la máquina local.

Para usar archivos personalizados:
```sh
docker run --rm -v $(pwd)/models:/app/models -v $(pwd)/data:/app/data -v $(pwd)/predictions:/app/output inference-model --input data/userdata.csv --output predictions/user_predictions.csv
```

---

## Verificación de Resultados
Después de ejecutar los contenedores, revisa:
- **Modelo entrenado:**
  ```sh
  ls models/
  ```
  Deberías ver `best_random_forest_model.pkl`.
- **Predicciones generadas:**
  ```sh
  ls predictions/
  ```
  Deberías ver `predictions.csv` o el archivo de salida especificado.

---

## Solución de Problemas
Si hay errores en la ejecución de un contenedor, puedes ingresar en modo interactivo:
```sh
docker run --rm -it train-model bash
```
Dentro del contenedor, ejecuta manualmente los comandos para verificar archivos y configuraciones.

---

Ahora puedes entrenar y hacer inferencias usando Docker de manera eficiente.

