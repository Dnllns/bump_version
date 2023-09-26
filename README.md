# bump_version
**Hook de git para gestionar el incremento de version en un proyecto**

## Instalación

```bash
# Entrar en el directorio de instalacion
cd bump_version

# Instalar dependencias
pip install -r requirements.txt

# Instalacion del hook en el repositorio
bash install.sh
```

## Uso

A la hora de hacer el commit, añadir los siguientes flag en el mensaje de commit:

```bash
--update major   # Actualiza MAJOR.x.x
--update minor   # Actualiza x.MINOR.x
--update patch   # Actualiza x.x.PATCH
``````

## App de prueba

Se dispone de la aplicacion de prueba app.py para test.

```bash
$> python app.py

------------------------------------
Prueba de concepto de autoversionado
------------------------------------

Formato de versionado: BRANCH-MAJOR.MINOR.PATCH
Version actual: MAIN-1.1.0

Para actualizar la version de la app:
 -> Mayor de la version, realizar un commit con la palabra clave '--update major'
 -> Menor de la version, realizar un commit con la palabra clave '--update minor'
 -> Patch de la version, realizar un commit con la palabra clave '--update patch'
``````

