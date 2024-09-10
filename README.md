# Sistema de información para la gestión y análisis de ventas.

Este es un sistema de gestión de ventas diseñado para una pequeña empresa llamada Kaip'e Alimentos. Permite manejar inventarios, procesar ventas, generar reportes y realizar un seguimiento detallado de las transacciones.

## Características:

- Gestión de productos: CRUD para almacenamiento, obtención, eliminación y modificación de productos.
- Manejo de ventas: Registro de ventas con cálculo automático de precios y ganancias.
- Reportes: Generación de reportes de ventas y estadísticas de rendimiento.
- Interfaz de usuario: UI responsiva y amigable.

## Instalación:

- Clonar el repositorio:

```bash
git clone https://github.com/Alfa06N/Kalina-System.git
```

- Navegar al repositorio del proyecto:

```bash
cd System/app
```

- Crear un entorno virtual:

```bash
python -m venv myenv
```

- Activar el entorno virtual:

```bash
# Puedes necesitar ejecutar este comando para permitir la ejecución de scripts no confirmados
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
venv\Scripts\activate

```

- Instalar dependencias:

```bash
pip install -r requirements.txt
```

- Configurar variables de entorno: Agregar a tus variables de entorno la variable con el nombre DATABASE_URL con las credenciales para acceder a tu base de datos MySQL (De lo contrario la app no funcionará).

- Ejecutar la aplicación:

```bash
flet main.py
```

- Nota: Es importante activar el entorno virtual para asegurarte de que las dependencias se instalen y se utilicen correctamente dentro de ese entorno.

## Requisitos:

- Python 3.11+
- SQLAlchemy
- Flet
- MySQL o SQLite

## Funcionalidades disponibles:

- Después de iniciar la aplicación, ingresa las credenciales del usuario predeterminado.
- Para crear nuevos usuarios, primero debes registrar los empleados de la empresa en el sistema.
- Puedes crear los usuarios desde la sección de "Usuarios" en la página principal.

## Contribuciones:

- Las contribuciones son bienvenidas. Por favor, abre un issue para discutir los cambios que te gustarían hacer

## Autores:

- Desarrollado por mi persona, Alfa06N.

## Contacto:

- Para preguntas, contacta a mi correo nicolasalfag@gmail.com
