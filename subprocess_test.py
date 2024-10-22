# main_script.py
import subprocess

# Comando para ejecutar el otro script
command = ["python", "main.py"]

# Ejecutar el otro script
result = subprocess.run(command, capture_output=True, text=True)

# Mostrar la salida del otro script
print("main.py:")
print(result.stdout)

# Mostrar los errores del otro script (si los hay)
if result.stderr:
    print("Errores del other_script.py:")
    print(result.stderr)
