# BiblioGestor

BiblioGestor es un sistema moderno de gestión de bibliotecas universitarias desarrollado en Python (con el framework Flet) y MySQL. Este sistema permite a estudiantes y administradores interactuar con el inventario de libros, préstamos, devoluciones y reservas de manera fluida y con una interfaz gráfica amigable.

## Arquitectura General

El proyecto sigue una arquitectura Cliente-Servidor (Frontend-Backend monolítico):
- **Frontend / Interfaz**: Desarrollado con [Flet](https://flet.dev/), que permite crear aplicaciones interactivas en Python multiplataforma.
- **Backend / Lógica**: Funciones modulares de Python que se encargan del enrutamiento de las vistas, autenticación y reglas de negocio (ej. validación de sanciones por entrega tardía, reservas automáticas).
- **Base de Datos**: MySQL relacional, modelado para soportar usuarios, libros, ejemplares físicos (inventario real), préstamos, devoluciones y reservas.

## Estructura del Modelo de Datos (E-R)

1. **Usuarios**: Almacena información de los estudiantes y el personal. Rol (1 = Estudiante, 0 = Admin).
2. **Libros**: Entidad lógica del libro (ISBN, Título, Autores, etc.).
3. **Ejemplares Físicos**: Representa cada copia física de un libro en la biblioteca. Tiene su propio estado (`Disponible`, `Prestado`, `Perdido`).
4. **Préstamos**: Relaciona un usuario con un ejemplar físico. Incluye fechas de préstamo, vencimiento y estados de solicitud.
5. **Devoluciones**: Registra la devolución de un préstamo específico, incluyendo observaciones y cálculo de multas.
6. **Reservas**: Permite a un estudiante reservar un ejemplar cuando no hay disponibilidad inmediata.

## Requisitos Previos

- Python 3.10 o superior.
- MySQL Server (local o en la nube como Railway).
- (Opcional) Docker para despliegue por contenedores.

## Cómo desplegar y ejecutar la aplicación localmente

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/Jorgedst/BiblioGestor.git
   cd BiblioGestor
   ```

2. **Crear y activar un entorno virtual (Recomendado):**
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En Mac/Linux:
   source venv/bin/activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar la Base de Datos:**
   - Asegúrate de tener una instancia de MySQL corriendo.
   - Ejecuta el script `database/schema.sql` en tu gestor de base de datos (por ejemplo, MySQL Workbench) para crear la base de datos `bibliogestor` y todas sus tablas.
   - Configura las credenciales en el archivo `.env` en la raíz del proyecto:
     ```env
     DB_HOST=localhost
     DB_PORT=3306
     DB_USER=tu_usuario
     DB_PASSWORD=tu_contraseña
     DB_NAME=bibliogestor
     ```

5. **Ejecutar la aplicación:**
   ```bash
   python main.py
   ```

## Estructura de Contenedores y Despliegue (Docker)

Para un despliegue en contenedores, se puede utilizar el archivo `Dockerfile` (a configurar) para empaquetar la aplicación Flet. Si se desea desplegar también la base de datos, se recomienda un archivo `docker-compose.yml` que levante un contenedor de la base de datos MySQL y otro para la aplicación de Flet interconectados en una red de Docker.

**¡Gracias por contribuir a BiblioGestor!**
