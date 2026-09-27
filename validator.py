import re

PRODUCTION_REGEX = re.compile(
    r"^[A-Z]\s*->\s*(?:[A-Za-z0-9]+|ε)"
    r"(?:\s*\|\s*(?:[A-Za-z0-9]+|ε))*\s*$"
)

def validate_line(line: str) -> bool:
    return bool(PRODUCTION_REGEX.fullmatch(line.strip()))

def find_invalid_symbol(line: str) -> str | None:
    allowed = set(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "abcdefghijklmnopqrstuvwxyz"
        "0123456789"
        "->|ε \t"
    )

    return next((ch for ch in line if ch not in allowed), None)

def validate_file(filename: str) -> list[str]:
    print("\nVALIDACIÓN DE GRAMÁTICA")

    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()

    valid_lines = []

    for number, raw in enumerate(lines, 1):
        line = raw.strip()

        if not line:
            continue

        print(f"Línea {number}: {line}")

        if not validate_line(line):
            bad = find_invalid_symbol(line)
            print("\nERROR DE SINTAXIS")

            if bad:
                print(f"Símbolo inválido encontrado: '{bad}'")

            print(f"Línea {number}: {line}")
            print("La ejecución ha sido detenida.")

            raise ValueError(f"Producción inválida en línea {number}")

        print("     válida")
        valid_lines.append(line)

    if not valid_lines:
        raise ValueError("El archivo no contiene producciones.")

    return valid_lines