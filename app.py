from version import __version__, __branch__

ANSI_GREEN = "\u001b[32m"
ANSI_RESET = "\u001b[0m"
print("\n------------------------------------")
print("Prueba de concepto de autoversionado")
print("------------------------------------\n")
print("Formato de versionado: BRANCH-MAJOR.MINOR.PATCH")
print(f"Version actual: {ANSI_GREEN}{__branch__.upper()}-{__version__}{ANSI_RESET}")
print("\nPara actualizar la version de la app:")
print(" -> Mayor de la version, realizar un commit con la palabra clave '--update major'")
print(" -> Menor de la version, realizar un commit con la palabra clave '--update minor'")
print(" -> Patch de la version, realizar un commit con la palabra clave '--update patch'")