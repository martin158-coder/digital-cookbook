# Español
# 🍽 Recetario Digital
# Proyecto de reingeniería de software: modernización de una aplicación web con Flask y MongoDB

## Descripción

Recetario Digital es una aplicación web *responsive* (adaptable) desarrollada con Flask y MongoDB que permite a los usuarios crear, editar, eliminar, buscar y visualizar recetas de cocina.

Este proyecto fue modernizado como parte de un curso de **Reingeniería de Software**. El objetivo era mejorar la arquitectura, la mantenibilidad y la experiencia de usuario de la aplicación, preservando al mismo tiempo su funcionalidad original.

---

# Reingeniería de Software

## Arquitectura Original (Legado)

La versión original de la aplicación seguía una arquitectura monolítica.

Características:

- La mayor parte de la lógica de la aplicación estaba contenida en un único archivo `app.py`.
- Las variables de entorno estaban configuradas directamente dentro de la aplicación.
- Varias funciones contenían código duplicado.
- Las operaciones CRUD estaban fuertemente acopladas a la lógica de la aplicación.
- La interfaz ofrecía una navegación básica y una usabilidad limitada.

---

## Problemas Identificados

Durante el análisis se identificaron los siguientes problemas:

- Estructura de aplicación monolítica.
- Baja reutilización de código.
- Configuración mezclada con la lógica de negocio.
- Mantenimiento y escalabilidad difíciles.
- Operaciones de base de datos repetidas.
- Votación ilimitada por parte de los usuarios.
- Interfaz de usuario básica.

---

## Mejoras Implementadas

Durante el proceso de modernización se implementaron las siguientes mejoras:

- Variables de entorno centralizadas en `config.py`.
- Inicialización de MongoDB trasladada a `extensions.py`.
- Funciones auxiliares reutilizables trasladadas a `utils.py`.
- Inicio de la modularización de rutas mediante *Blueprints*.
- Funciones CRUD refactorizadas para una mejor mantenibilidad.
- Sistema de votación actualizado para permitir un solo voto por usuario.
- Sección "Mis recetas" corregida para mostrar solo las recetas creadas por el usuario actual.
- Navegación mejorada con una opción de cierre de sesión (*Logout*).
- Interfaz de usuario mejorada utilizando Bootstrap y optimizaciones de CSS.

---

## Nueva Estructura del Proyecto

```
digital-cookbook/
│
├── app.py
├── config.py
├── extensions.py
├── utils.py
├── forms.py
├── routes/
│   └── recipes.py
├── templates/
├── static/
├── data/
└── README.md
```

---

## Funcionalidades

- Explorar recetas.
- Buscar recetas.
- Añadir recetas.
- Editar recetas.
- Eliminar recetas.
- Votar recetas.
- Ver recetas personales. - Cerrar sesión y volver a la página de inicio.

---

## Tecnologías utilizadas

- Python
- Flask
- MongoDB Atlas
- Flask-PyMongo
- HTML5
- CSS3
- Bootstrap
- JavaScript
- jQuery

---

## Instalación

1. Clona el repositorio.

```bash
git clone <repository_url>
```

2. Crea un entorno virtual.

```bash
python -m venv venv
```

3. Activa el entorno virtual.

Windows:

```bash
venv\Scripts\activate
```

4. Instala las dependencias.

```bash
pip install -r requirements.txt
```

5. Crea un archivo `.env` con el siguiente contenido:

```env
SECRET=your_secret_key
DBNAME=your_database_name
URI=your_mongodb_connection_string
```

6. Ejecuta la aplicación.

```bash
python app.py
```

---

## Pruebas

Se realizaron pruebas manuales en los siguientes módulos:

- Página de inicio
- Ver recetas
- Mis recetas
- Búsqueda
- Añadir receta
- Editar receta
- Eliminar receta
- Sistema de votación
- Cerrar sesión

---

## Agradecimientos

El diseño original del proyecto se basó en el tema "Creative Bootstrap" de Start Bootstrap.

Esta versión incluye mejoras arquitectónicas y de interfaz desarrolladas como parte de un proyecto de reingeniería de software.


# English
# 🍽 Digital Cookbook

## Description

Digital Cookbook is a responsive web application developed with Flask and MongoDB that allows users to create, edit, delete, search and view cooking recipes.

This project was modernized as part of a **Software Reengineering** course. The objective was to improve the application's architecture, maintainability and user experience while preserving its original functionality.

---

# Software Reengineering

## Original Architecture (Legacy)

The original version of the application followed a monolithic architecture.

Characteristics:

- Most of the application logic was contained in a single `app.py` file.
- Environment variables were configured directly inside the application.
- Several functions contained repeated code.
- CRUD operations were tightly coupled with the application logic.
- The interface provided basic navigation and limited usability.

---

## Problems Identified

The following issues were identified during the analysis:

- Monolithic application structure.
- Low code reusability.
- Configuration mixed with business logic.
- Difficult maintenance and scalability.
- Repeated database operations.
- Unlimited voting by users.
- Basic user interface.

---

## Improvements Implemented

The following improvements were implemented during the modernization process:

- Environment variables centralized in `config.py`.
- MongoDB initialization moved to `extensions.py`.
- Reusable helper functions moved to `utils.py`.
- Beginning of route modularization using Blueprints.
- CRUD functions refactored for better maintainability.
- Voting system updated to allow only one vote per user.
- "My Recipes" section corrected to display only recipes created by the current user.
- Navigation improved with a Logout option.
- User interface enhanced using Bootstrap and CSS improvements.

---

## New Project Structure

```
digital-cookbook/
│
├── app.py
├── config.py
├── extensions.py
├── utils.py
├── forms.py
├── routes/
│   └── recipes.py
├── templates/
├── static/
├── data/
└── README.md
```

---

## Features

- Browse recipes.
- Search recipes.
- Add recipes.
- Edit recipes.
- Delete recipes.
- Vote recipes.
- View personal recipes.
- Logout and return to the home page.

---

## Technologies Used

- Python
- Flask
- MongoDB Atlas
- Flask-PyMongo
- HTML5
- CSS3
- Bootstrap
- JavaScript
- jQuery

---

## Installation

1. Clone the repository.

```bash
git clone <repository_url>
```

2. Create a virtual environment.

```bash
python -m venv venv
```

3. Activate the virtual environment.

Windows:

```bash
venv\Scripts\activate
```

4. Install dependencies.

```bash
pip install -r requirements.txt
```

5. Create a `.env` file containing:

```env
SECRET=your_secret_key
DBNAME=your_database_name
URI=your_mongodb_connection_string
```

6. Run the application.

```bash
python app.py
```

---

## Testing

Manual testing was performed on the following modules:

- Home page
- View Recipes
- My Recipes
- Search
- Add Recipe
- Edit Recipe
- Delete Recipe
- Voting system
- Logout

---

## Acknowledgements

The original project design was based on the Creative Bootstrap Theme by Start Bootstrap.

This version includes architectural improvements and interface enhancements developed as part of a Software Reengineering project.
