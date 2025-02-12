# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo de requerimientos y el código de la aplicación al contenedor
COPY requirements.txt /app/
COPY backend /app/backend

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto en el que la aplicación correrá
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["python", "backend/app/app.py"] 