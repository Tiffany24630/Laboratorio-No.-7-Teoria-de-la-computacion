from pathlib import Path
from validator import validate_file
from simplifier import parse_grammar, find_nullable, remove_epsilon, remove_unit_productions, remove_non_generating, remove_non_reachable
from cnf import convert_to_cnf
from process import process_file

print("=" * 72)
print("SIMPLIFICADOR DE GRAMÁTICAS LIBRES DE CONTEXTO")
print("=" * 72)
print("\n1. gramatica1.txt")
print("2. gramatica2.txt")
print("3. gramatica3.txt")
print("4. Procesar las tres")

option = input("\nSeleccione una opción: ").strip()

files = {
    "1": ["gramatica1.txt"],
    "2": ["gramatica2.txt"],
    "3": ["gramatica3.txt"],
    "4": ["gramatica1.txt", "gramatica2.txt", "gramatica3.txt"],
}

if option not in files:
    print("Opción inválida.")
    exit()

for filename in files[option]:
    process_file(filename)