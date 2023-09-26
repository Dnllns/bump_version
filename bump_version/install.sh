#!/bin/sh

script_conf=bump_version.conf
bump_script=$(cat $script_conf | grep bump_script | cut -d '=' -f 2 | tr -d ' ')
installation_path=$(cat $script_conf | grep installation_path | cut -d '=' -f 2 | tr -d ' ')
post_commit_hook=$(cat $script_conf | grep post_commit_hook | cut -d '=' -f 2 | tr -d ' ')
version_file=$(cat $script_conf | grep version_file | cut -d '=' -f 2 | tr -d ' ')

# Leer la configuración desde ./bump_version.conf
if [ ! -f $bump_script_conf ]; then
    echo "Error: No se encontró el archivo de configuración 'bump_version.conf'"
    exit 1
fi

# Verificar si los archivos especificados en la configuración existen
if [ ! -f $bump_script ]; then
    echo "Error: No se encontró el script 'bump_version.py'"
    exit 1
fi

# crear carpeta para bump_version en .git/
mkdir -p $installation_path

# Crear el archivo post-commit hook
echo '#!/bin/sh' > "$post_commit_hook"
echo '' >> "$post_commit_hook"
echo '# Hook post-commit para actualizar la versión del proyecto' >> "$post_commit_hook"
echo "python bump_version/$bump_script" >> "$post_commit_hook"

# Crear el archivo de versiones (version.py) con una versión inicial
echo '__version__ = "1.0.0"' > "../$version_file"
echo '__branch__ = "master"' >> "../$version_file"

# Dar permisos de ejecución al archivo post-commit hook
chmod +x "$post_commit_hook"

# Mover el .conf y el script .py a la carpeta .git/bump_version
cp $script_conf $installation_path/$script_conf
cp $bump_script $installation_path/$bump_script

echo 'Instalación completada. Se ha creado el archivo post-commit hook y el archivo de versiones.'
