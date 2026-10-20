# rememberIt
Sistema integral de gestión de residentes, control de tratamientos medicamentosos y seguimiento de turnos para optimizar la administración en centros de cuidado.


## Django version 6.1.2

para que todos tenga la misma version de Django, instalen los requerimientos profavorsito.

``` sh
pip install -r requirements.txt
```

--- 
### Base de datos
1. Deben de tener instalado oracle SQL Developer -> https://www.oracle.com/database/sqldeveloper/
![alt text](doc/image.png)

2. Deben de tener instalado Oracle Database 21c Express Edition (XE) -> https://www.oracle.com/database/technologies/xe-downloads.html
![alt text](doc/image-1.png)

3. Configuren las credenciales de Oracle. Desde la carpeta `rememberIt`, copien `.env.example` a `.env`:
    ``` powershell
    Copy-Item .env.example .env
    ```

    Editen `.env` y reemplacen `DB_USER` y `DB_PASSWORD` con el usuario y la contraseña de su base de datos. Ajusten también `DB_NAME`, `DB_HOST` y `DB_PORT` si su conexión Oracle usa otros valores. No compartan ni suban el archivo `.env`.

4. Creen las tablas mediante las migraciones de Django, desde la carpeta `rememberIt`:
    ``` sh
    python manage.py makemigrations

    python manage.py migrate
    ```

con esto se deberian crear todas las tablas en su DBMS