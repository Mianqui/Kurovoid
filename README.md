# Kurovoid

Tienda online construida con Django y Tailwind CSS.

## Requisitos

- Python 3.14+
- Node.js (para Tailwind CSS)
- PostgreSQL (en Docker) o SQLite (local)

## Instalación

```bash
# Clonar e instalar dependencias
pip install -r requirements.txt
npm install

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus valores

# Migraciones y servidor
python manage.py migrate
python manage.py runserver
```

## Docker

```bash
cp .env.example .env
docker compose up --build
```

## Tailwind CSS

```bash
npm run build:css
```
