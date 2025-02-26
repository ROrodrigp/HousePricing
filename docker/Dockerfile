# Usa Miniconda como imagen base
FROM continuumio/miniconda3

# Configurar el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos necesarios desde el contexto de construcción
COPY ../train.py .
COPY ../data ./data
COPY environment.yml .

# Crear el entorno Conda dentro del contenedor
RUN conda env create -f environment.yml && conda clean --all -y

# Establecer el entorno Conda como predeterminado
ENV PATH /opt/conda/envs/arquitectura/bin:$PATH

# Crear un volumen dentro del contenedor para almacenar el modelo
VOLUME /app/output

# Definir el comando de ejecución
ENTRYPOINT ["python", "train.py"]
