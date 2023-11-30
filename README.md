## Repaso de Python - CRUD de Serie y Artículos - Con Usuario personalizado e inicio de sesión con OAuth 
### En DJango
Este repo es un proyecto semilla en Django.

Se usa el módulo de auth de django. 
Se personaliza el modelo de Usuario. 
Se modifica el back de autenticación.
Se utiliza y modifica los formularios de Login y registro del módulo de auth.
Se crea decorador 'user_not_authenticated'.
Se usa el módulo para el envío de emails.
se generan tokens para el restaflecimiento de contraseña.



## Getting Started

1. Copiar el .env.example y renombrarlo como .env
2. Cambiar el valor de la variable de entorno
3. Comentar la variable AUTHENTICATION_BACKENDS en  sap/sap/settings.py
4. Correr en la terminal 'python manage.py makemigrations'
5. Correr en la terminal 'python manage.py migrate'
6. Descomentar la variable AUTHENTICATION_BACKENDS en  sap/sap/settings.py
7. Correr en la terminal 'python manage.py runserver'
8. Crear super usuario en la terminal 'python manage.py createsuperuser'
9. Para el Login con OAth en google crear un sitio en la interfaz de administración - Crear una aplicación (Imagen 1 y 2)
10. Descomentar el Botón de Login para OAth en la plantilla 'user/template/user/auth/login.html'
11. Refrescar en caso de ser inconvenientes 'python manage.py runserver'
...


...
# Presentación
![Pagina ViewDominio](https://github.com/ZitelliDZ/django-proyecto-semilla/sap/presentacion/dominio.png?raw=true)

![Pagina ViewAplicacion](https://github.com/ZitelliDZ/django-proyecto-semilla/sap/presentacion/aplicacion.png?raw=true)

![Pagina ViewHome](https://github.com/ZitelliDZ/django-proyecto-semilla/sap/presentacion/home.png?raw=true)

![Pagina ViewLogin](https://github.com/ZitelliDZ/django-proyecto-semilla/sap/presentacion/login.png?raw=true)

![Pagina ViewArticuloDetalle](https://github.com/ZitelliDZ/django-proyecto-semilla/sap/presentacion/articulo_detalle.png?raw=true)

![Pagina ViewArticulo](https://github.com/ZitelliDZ/django-proyecto-semilla/sap/presentacion/articulo.png?raw=true)
