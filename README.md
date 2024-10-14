# Portal para Registro de Participanes en Labs - LACNOG

## Descripción
El Portal de Estudiantes es una aplicación web desarrollada con Django que facilita la gestión de talleres y equipos de laboratorio para instituciones educativas. Esta herramienta permite a los estudiantes registrarse en talleres, acceder a información sobre equipos de laboratorio asignados y proporciona a los administradores una interfaz para gestionar talleres y equipos.

## Características principales
- Registro de estudiantes y autenticación de usuarios
- Inscripción en talleres
- Interfaz para asignar equipos de laboratorio a participantes
- Panel de administración para gestionar talleres y equipos
- Verificación de correo electrónico para nuevos registros

## Requisitos técnicos
- Python 3.10+
- Django 4.2+
- Django Allauth para autenticación y registro de usuarios
- PostgreSQL como base de datos

## Instalación y configuración

### Opción 1: Instalación local

1. Clonar el repositorio:
   ```
   git clone https://github.com/tu-usuario/portal-estudiantes.git
   cd portal-estudiantes
   ```

2. Crear y activar un entorno virtual:
   ```
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instalar las dependencias:
   ```
   pip install -r requirements.txt
   ```

4. Configurar la base de datos en `student_portal/settings.py`

5. Aplicar las migraciones:
   ```
   python manage.py migrate
   ```

6. Crear un superusuario:
   ```
   python manage.py createsuperuser
   ```

7. Ejecutar el servidor de desarrollo:
   ```
   python manage.py runserver
   ```

### Opción 2: Usando Docker Compose

1. Asegúrate de tener Docker y Docker Compose instalados en tu sistema.

2. Clonar el repositorio:
   ```
   git clone https://github.com/tu-usuario/portal-estudiantes.git
   cd portal-estudiantes
   ```

3. Crea un archivo `.env` en la raíz del proyecto si no existe ya. Asegúrate de que contenga las siguientes variables de entorno (ajusta los valores según sea necesario):
   ```
   DEBUG=1
   SECRET_KEY=tu_clave_secreta
   DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
   SQL_ENGINE=django.db.backends.postgresql
   SQL_DATABASE=portal_estudiantes
   SQL_USER=tu_usuario
   SQL_PASSWORD=tu_contraseña
   SQL_HOST=db
   SQL_PORT=5432
   DATABASE=postgres
   ```

4. Construye y levanta los contenedores:
   ```
   docker-compose up --build
   ```

5. En otra terminal, ejecuta las migraciones:
   ```
   docker-compose exec web python manage.py migrate
   ```

6. Crea un superusuario:
   ```
   docker-compose exec web python manage.py createsuperuser
   ```

7. La aplicación estará disponible en `http://localhost:8000`

Nota: Si encuentras problemas con los permisos de los archivos al usar Docker, puedes ejecutar los comandos con `sudo` o ajustar los permisos de los archivos según sea necesario.

## Estructura del proyecto
- `portal/`: Aplicación principal con modelos, vistas y formularios
- `student_portal/`: Configuración del proyecto Django
- `templates/`: Plantillas HTML para la interfaz de usuario
- `Dockerfile`: Configuración para la imagen Docker de la aplicación
- `docker-compose.yml`: Configuración para orquestar los servicios de la aplicación y la base de datos

## Características técnicas destacadas
- Uso de Django Allauth para manejo avanzado de autenticación y registro
- Implementación de verificación de correo electrónico
- Modelo de datos relacional para talleres, equipos y perfiles de estudiantes
- Vistas basadas en clases y funciones para diferentes funcionalidades
- Uso de formularios personalizados para el registro de estudiantes
- Integración con el panel de administración de Django para gestión de datos
- Configuración de Docker y Docker Compose para desarrollo y despliegue simplificados

## Contribución
Las contribuciones son bienvenidas. Por favor, abre un issue para discutir cambios mayores antes de enviar un pull request.

## Versiones
- **Versión 1 (actual)**: MVP funcional utilizado exitosamente en talleres recientes.

## Contacto
Para más información o soporte, por favor contacta a [cmartinez AT nog.lat].

## Licencia
Este proyecto está licenciado bajo la Licencia BSD de 3 cláusulas. Consulta el archivo `LICENSE` en el repositorio para más detalles.

Copyright (c) 2024, [Carlos Martinez, LACNOG]
Todos los derechos reservados.

