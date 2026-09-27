from itertools import product
from grammar import Grammar

def parse_grammar(lines: list[str]) -> Grammar:
    productions: dict[str, list[tuple[str, ...]]] = {}

    for line in lines:
        lhs, rhs_text = line.split("->", 1)
        lhs = lhs.strip()
        productions.setdefault(lhs, [])

        for alternative in rhs_text.split("|"):
            alternative = alternative.strip()
            rhs = () if alternative == "ε" else tuple(alternative)

            if rhs not in productions[lhs]:
                productions[lhs].append(rhs)

    return Grammar(next(iter(productions)), productions)

def find_nullable(grammar: Grammar) -> set[str]:
    print("\n" + "=" * 72)
    print("1. SÍMBOLOS ANULABLES")
    print("=" * 72)

    nullable: set[str] = set()

    print("\nAnulables directos:")

    for lhs, rhss in grammar.productions.items():

        if () in rhss:
            nullable.add(lhs)
            print(f"  {lhs} -> ε  =>  {lhs} es anulable")

    changed = True

    while changed:
        changed = False

        for lhs, rhss in grammar.productions.items():
            if lhs in nullable:
                continue

            for rhs in rhss:
                if rhs and all(symbol in nullable for symbol in rhs):
                    nullable.add(lhs)
                    print(
                        f"  {lhs} -> {' '.join(rhs)} "
                        f"=> todos sus símbolos son anulables"
                    )
                    changed = True

                    break

    print("\nResultado:", "{" + ", ".join(sorted(nullable)) + "}")

    return nullable

def generate_epsilon_variants(rhs: tuple[str, ...], nullable: set[str]) -> list[tuple[str, ...]]:
    positions = [i for i, symbol in enumerate(rhs) if symbol in nullable]
    variants = set()

    for mask in product([False, True], repeat=len(positions)):
        remove = {positions[i] for i, bit in enumerate(mask) if bit}
        variant = tuple(symbol for i, symbol in enumerate(rhs) if i not in remove)
        variants.add(variant)

    return sorted(variants, key=lambda r: (len(r), r))

def remove_epsilon(grammar: Grammar, nullable: set[str]) -> Grammar:
    print("\n" + "=" * 72)
    print("2. ELIMINACIÓN DE PRODUCCIONES ε")
    print("=" * 72)

    result = Grammar(grammar.start)

    for lhs, rhss in grammar.productions.items():
        for rhs in rhss:
            if not rhs:
                continue

            m = sum(symbol in nullable for symbol in rhs)

            if m == 0:
                result.add_production(lhs, rhs)

                continue

            variants = generate_epsilon_variants(rhs, nullable)

            print(f"\n{lhs} -> {' '.join(rhs)}")
            print(f"  m = {m}; casos = 2^{m} = {2 ** m}")

            for variant in variants:
                text = "ε" if not variant else " ".join(variant)
                print(f"    {lhs} -> {text}")

                if variant:
                    result.add_production(lhs, variant)

    if grammar.start in nullable:
        result.add_production(grammar.start, ())

    result.print_grammar("GRAMÁTICA SIN ε")

    return result

def remove_unit_productions(grammar: Grammar) -> Grammar:
    print("\n" + "=" * 72)
    print("3. ELIMINACIÓN DE PRODUCCIONES UNITARIAS")
    print("=" * 72)

    nts = grammar.nonterminals
    closure = {A: {A} for A in nts}

    changed = True

    while changed:
        changed = False

        for A in nts:
            for rhs in grammar.productions.get(A, []):
                if len(rhs) == 1 and rhs[0] in nts:
                    before = len(closure[A])
                    closure[A] |= closure[rhs[0]]
                    changed |= len(closure[A]) > before

    result = Grammar(grammar.start)

    for A in nts:
        print(f"  {A}: {{{', '.join(sorted(closure[A]))}}}")

        for B in closure[A]:
            for rhs in grammar.productions.get(B, []):
                if len(rhs) == 1 and rhs[0] in nts:
                    continue

                result.add_production(A, rhs)

    result.print_grammar("GRAMÁTICA SIN PRODUCCIONES UNITARIAS")

    return result

def find_generating_symbols(grammar: Grammar) -> set[str]:
    generating: set[str] = set()
    nts = grammar.nonterminals

    changed = True

    while changed:
        changed = False

        for lhs, rhss in grammar.productions.items():
            if lhs in generating:
                continue

            for rhs in rhss:
                if all(symbol not in nts or symbol in generating for symbol in rhs):
                    generating.add(lhs)
                    changed = True

                    break

    return generating

def remove_non_generating(grammar: Grammar) -> Grammar:
    print("\n" + "=" * 72)
    print("4. ELIMINACIÓN DE SÍMBOLOS NO PRODUCTORES")
    print("=" * 72)

    generating = find_generating_symbols(grammar)
    non_generating = grammar.nonterminals - generating

    print("Productores:", "{" + ", ".join(sorted(generating)) + "}")
    print("No productores:", "{" + ", ".join(sorted(non_generating)) + "}")

    result = Grammar(grammar.start)

    for lhs, rhss in grammar.productions.items():
        if lhs not in generating:
            continue

        for rhs in rhss:
            if all(symbol not in grammar.nonterminals or symbol in generating for symbol in rhs):
                result.add_production(lhs, rhs)

    result.print_grammar("GRAMÁTICA SIN SÍMBOLOS NO PRODUCTORES")

    return result

def find_reachable(grammar: Grammar) -> set[str]:
    reachable = {grammar.start}
    changed = True

    while changed:
        changed = False

        for A in list(reachable):
            for rhs in grammar.productions.get(A, []):
                for symbol in rhs:
                    if symbol in grammar.nonterminals and symbol not in reachable:
                        reachable.add(symbol)
                        changed = True

    return reachable

def remove_non_reachable(grammar: Grammar) -> Grammar:
    print("\n" + "=" * 72)
    print("5. ELIMINACIÓN DE SÍMBOLOS NO ALCANZABLES")
    print("=" * 72)

    reachable = find_reachable(grammar)
    unreachable = grammar.nonterminals - reachable

    print("Alcanzables:", "{" + ", ".join(sorted(reachable)) + "}")
    print("No alcanzables:", "{" + ", ".join(sorted(unreachable)) + "}")

    result = Grammar(grammar.start)

    for lhs in reachable:
        for rhs in grammar.productions.get(lhs, []):
            if all(symbol not in grammar.nonterminals or symbol in reachable for symbol in rhs):
                result.add_production(lhs, rhs)

    result.print_grammar("GRAMÁTICA SIN SÍMBOLOS INALCANZABLES")
    
    return result