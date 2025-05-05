# 🐮 API de Gestión Ganadera - Backend Flask + MySQL con Docker

Este proyecto implementa una API RESTful para gestionar animales, fincas, producciones y eventos relacionados en un sistema ganadero. Utiliza **Flask**, **SQLAlchemy**, **Flask-Migrate**, y **MySQL** dentro de contenedores Docker.

---

## 📁 Estructura del proyecto

```text
📦 proyecto/
 ┣ 📂 app/
 ┃ ┣ 📂 api/
 ┃ ┣ 📂 models/
 ┃ ┣ 📄 app.py          # Código principal (con Flask y Blueprints)
 ┃ ┣ 📄 config/db.py    # Inicialización de Flask, SQLAlchemy, Marshmallow
 ┃ ┣ 📄 requirements.txt
 ┃ ┣ 📄 migrations/     # (se crea después de `flask db init`)
 ┃ ┗ 📄 ...
 ┣ 📄 Dockerfile
 ┣ 📄 docker-compose.yml
 ┗ 📄 README.md
```

---

## 🐳 Archivos Docker

### `Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app

EXPOSE 5050

CMD ["gunicorn", "--workers=4", "--bind", "0.0.0.0:5050", "app:app"]
```

---

### `docker-compose.yml`

```yaml
services:
  db:
    image: mysql:8.0
    container_name: mysql_container_vacas
    restart: always
    command: --default-authentication-plugin=mysql_native_password
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: vacas
    ports:
      - "3308:3306"
    volumes:
      - mysql_data_vacas:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-uroot", "-proot"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 20s

  app:
    build: .
    container_name: backend_vacas
    restart: always
    depends_on:
      db:
        condition: service_healthy
    environment:
      DB_HOST: db
      DB_PORT: 3306
      DB_USER: root
      DB_PASSWORD: root
      DB_NAME: vacas
    ports:
      - "5001:5050"
    volumes:
      - ./app:/app

volumes:
  mysql_data_vacas:
```

---

## 🚀 Pasos para levantar el sistema

### 1. ✅ Construir y levantar los contenedores

```bash
docker-compose up --build
```

Esto levantará la base de datos MySQL en el puerto `3308` y el backend Flask en el puerto `5001`.

---

### 2. 📂 Entrar al contenedor del backend

```bash
docker exec -it backend_vacas bash
```

---

### 3. ⚙️ Inicializar las migraciones de la base de datos (solo una vez)

```bash
flask db init
```

---

### 4. 📄 Generar migraciones con base en tus modelos

```bash
flask db migrate -m "Inicial"
```

---

### 5. ⬇️ Aplicar migraciones a la base de datos

```bash
flask db upgrade
```

---

## 🔍 Verificación rápida

Abre tu navegador en:

```text
http://localhost:5001/
```

Deberías ver:

```text
✅ API de gestión ganadera funcionando correctamente
```

Y los endpoints estarán bajo `/api/...`.

---

## 🧪 Ejemplo de prueba

Puedes probar un endpoint como este con `curl`:

```bash
curl http://localhost:5001/api/animales
```

---

## 🛠 Repetir migraciones (cuando cambias modelos)

```bash
flask db migrate -m "Cambios"
flask db upgrade
```

---

## 🔧 Script `entrypoint.sh` (opcional)

Puedes usar un archivo `entrypoint.sh` para automatizar el proceso de migración al arrancar el contenedor.

### `entrypoint.sh`

```bash
#!/bin/bash

flask db upgrade
exec gunicorn --workers=4 --bind 0.0.0.0:5050 app:app
```

Asegúrate de darle permisos de ejecución:

```bash
chmod +x entrypoint.sh
```

Y luego, en el `Dockerfile`:

```dockerfile
COPY entrypoint.sh /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
```