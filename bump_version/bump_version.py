import semver
import subprocess
import sys
import re
import configparser

def read_keywords():
    # Obtener las palabras clave desde el archivo bump_version.conf
    config = configparser.ConfigParser()
    config.read('bump_version/bump_version.conf')
    
    # Get keywords section
    keywords = config['update_keys']
    files = config['files']

    return {
        "key": keywords.get('key', fallback="--update"),
        "major_key": keywords.get('major', fallback="major"),
        "minor_key": keywords.get('minor', fallback="minor"),
        "patch_key": keywords.get('patch', fallback="patch"),
        "version_file": files.get('version_file', fallback="version.py")
    }

def read_commit_message():
    # Obtener el mensaje de commit desde el archivo .git/COMMIT_EDITMSG
    with open('.git/COMMIT_EDITMSG', 'r') as file:
        commit_msg = file.read()

    # Eliminar líneas que comienzan con '#' y espacios en blanco al inicio y al final de cada línea
    commit_msg = "\n".join(line.strip() for line in commit_msg.splitlines() if not line.strip().startswith("#"))
    
    return commit_msg

def find_version_bump_keyword(commit_msg):

    # Obtener las palabras clave desde el archivo bump_version.conf
    keywords = read_keywords()
    
    # Definir un patrón para buscar la palabra clave
    keyword_pattern = re.compile(rf'{keywords["key"]} ({keywords["major_key"]}|{keywords["minor_key"]}|{keywords["patch_key"]})')

    # Buscar la palabra clave en el mensaje de commit
    match = keyword_pattern.search(commit_msg)

    # Si se encuentra la palabra clave, devolver la parte de la versión indicada
    if match:
        return match.group(1)
    else:
        return None

def read_current_version():
    # Leer la versión actual desde el archivo 'version.py'
    keywords = read_keywords()
    with open(keywords["version_file"], 'r') as file:
        version_line = file.readline()
        current_version = re.search(r'"(.+)"', version_line).group(1)
    
    return current_version

def update_version_and_commit(mode, current_version):
    current_version_info = semver.VersionInfo.parse(current_version)

    # Incrementar la parte de la versión indicada
    if mode == "major":
        new_version_info = current_version_info.bump_major()
    elif mode == "minor":
        new_version_info = current_version_info.bump_minor()
    elif mode == "patch":
        new_version_info = current_version_info.bump_patch()

    new_version = str(new_version_info)

    # Obtener el nombre de la rama actual
    branch = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], stdout=subprocess.PIPE).stdout.decode("utf-8").strip()

    # Escribir la nueva versión en el archivo 'version.py'
    keywords = read_keywords()
    with open(keywords["version_file"], 'w') as file:
        file.write(
            f'__version__ = "{new_version}"\n' +
            f'__branch__ = "{branch}"\n'
        )

    return new_version, branch

def amend_commit_message(commit_msg, branch, new_version):
    # Reemplazar la palabra clave por la nueva versión en el mensaje de commit
    keywords = read_keywords()
    keyword_pattern = re.compile(rf'{keywords["key"]} ({keywords["major_key"]}|{keywords["minor_key"]}|{keywords["patch_key"]})')
    new_commit_msg = keyword_pattern.sub(f"Version: {branch.upper()}-{new_version}", commit_msg)

    # Modificar el mensaje del último commit mediante el comando 'git commit --amend'
    subprocess.run(["git", "commit", "--amend", "-m", new_commit_msg])

def main():
    commit_msg = read_commit_message()
    mode = find_version_bump_keyword(commit_msg)

    if mode is None:
        sys.exit(0)

    current_version = read_current_version()
    new_version, branch = update_version_and_commit(mode, current_version)
    amend_commit_message(commit_msg, branch, new_version)

    # Imprimir la nueva versión
    ANSI_GREEN = "\033[92m"
    ANSI_RESET = "\033[0m"
    print(f"{ANSI_GREEN}La versión se ha actualizado: {current_version} -> {new_version}{ANSI_RESET}")

if __name__ == "__main__":
    main()

    