# BiblioGestor

¡Bienvenidos al repositorio de **BiblioGestor**! Este es nuestro sistema de gestión para la biblioteca de la universidad, desarrollado en Python usando la librería Flet para la interfaz gráfica y MySQL para la base de datos.

## 🚀 Cómo abrir y ejecutar el proyecto

Para que puedan descargar y probar el proyecto en sus computadoras, sigan estos pasos rápidos:

### 1. Clonar el repositorio
Abre tu terminal (o la consola de VS Code) y clona el proyecto:
```bash
git clone https://github.com/Jorgedst/BiblioGestor.git
cd BiblioGestor
```

### 2. Configurar el Entorno Virtual
Es muy importante usar un entorno virtual para no mezclar librerías:
```bash
# Crear el entorno virtual
python -m venv venv

# Activarlo en Windows:
venv\Scripts\activate

# (Si estás en Mac/Linux usa: source venv/bin/activate)
```

### 3. Instalar dependencias
Con el entorno virtual activado, instala las librerías necesarias:
```bash
pip install -r requirements.txt
```

### 4. Configurar la Base de Datos
- Tienes que tener el archivo `.env` en la raíz del proyecto. Si no lo tienes, créalo y pídele a un administrador las credenciales (DB_USER, DB_PASSWORD, etc.).
- Asegúrate de que tu base de datos esté corriendo y tenga la estructura lista. Si usas MySQL Workbench, puedes ejecutar el script `database/schema.sql` para crear las tablas.

### 5. Iniciar la aplicación
Por último, para abrir la interfaz:
```bash
python main.py
```

¡Y listo! Ya deberías ver la pantalla de inicio de BiblioGestor. 
Cualquier duda o cambio, creen una nueva rama (branch) para trabajar. ¡Éxitos!
