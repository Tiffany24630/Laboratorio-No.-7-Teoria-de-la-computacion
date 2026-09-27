from pathlib import Path
from validator import validate_file
from simplifier import parse_grammar, find_nullable, remove_epsilon, remove_unit_productions, remove_non_generating, remove_non_reachable
from cnf import convert_to_cnf

BASE_DIR = Path(__file__).resolve().parent

def process_file(filename: str) -> None:
    path = BASE_DIR / filename

    print("\n" + "#" * 72)
    print(f"PROCESANDO: {filename}")
    print("#" * 72)

    try:
        lines = validate_file(str(path))
        grammar = parse_grammar(lines)

        grammar.print_grammar("GRAMÁTICA ORIGINAL")

        nullable = find_nullable(grammar)
        grammar = remove_epsilon(grammar, nullable)
        grammar = remove_unit_productions(grammar)
        grammar = remove_non_generating(grammar)
        grammar = remove_non_reachable(grammar)
        grammar = convert_to_cnf(grammar)

        print("\n" + "=" * 72)
        print("PROCESAMIENTO TERMINADO CORRECTAMENTE")
        print("=" * 72)

    except FileNotFoundError:
        print(f"ERROR: no se encontró '{path}'.")
    except ValueError as exc:
        print(f"ERROR: {exc}")