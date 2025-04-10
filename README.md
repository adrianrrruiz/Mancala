# Proyecto: Análisis de Algoritmos  
## Mancala - Juego Interactivo

### Integrantes del equipo
- Adrián Ruiz  
- Gustavo Ortiz  
- Leonardo Velázquez  
- Tomás Martínez  

## Descripción del Proyecto

Este proyecto implementa el clásico juego Mancala como parte del curso de Análisis de Algoritmos. La aplicación está compuesta por dos componentes:

- **Backend**: desarrollado con **FastAPI**, maneja la lógica del juego y las operaciones del servidor.
- **Frontend**: desarrollado con **Angular**, proporciona una interfaz web interactiva para jugar.

## Requisitos Previos

Asegúrate de tener instalados los siguientes componentes:

- Python 3.10 o superior  
- pip (gestor de paquetes de Python)  
- Node.js y npm  
- Angular CLI (instalación global):

```bash
npm install -g @angular/cli
```

## Instrucciones de Ejecución

### Backend (FastAPI)

1. Navega al directorio del backend:

```bash
cd back
```

2. Instala las dependencias necesarias:

```bash
pip install "fastapi[standard]"
```

3. Ejecuta el servidor de desarrollo:

```bash
fastapi dev main.py
```

El backend estará disponible en: http://127.0.0.1:8000

### Frontend (Angular)

1. Navega al directorio del frontend:

```bash
cd front
```

2. Instala las dependencias del proyecto:

```bash
npm install
```

3. Ejecuta la aplicación web:

```bash
ng serve
```

La aplicación estará disponible en: http://localhost:4200

## Notas

- Asegúrate de que el backend esté en ejecución antes de iniciar el frontend para evitar errores de conexión.  
