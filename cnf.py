from grammar import Grammar

def convert_to_cnf(grammar: Grammar) -> Grammar:
    print("\n6. FORMA NORMAL DE CHOMSKY (CNF)")

    start = grammar.start
    start_in_rhs = any(
        start in rhs

        for rhss in grammar.productions.values()

        for rhs in rhss
    )

    working = grammar.copy()

    if start_in_rhs:
        new_start = _fresh_symbol(working, "S0")
        temp = Grammar(new_start)

        for rhs in working.productions[start]:
            if rhs:
                temp.add_production(new_start, rhs)

        for lhs, rhss in working.productions.items():
            for rhs in rhss:
                if lhs == start and not rhs:
                    continue

                temp.add_production(lhs, rhs)

        if any(not rhs for rhs in working.productions[start]):
            temp.add_production(new_start, ())

        working = temp
        start = new_start

    result = Grammar(start)
    terminal_vars: dict[str, str] = {}

    for lhs, rhss in working.productions.items():
        for rhs in rhss:
            if len(rhs) <= 1:
                result.add_production(lhs, rhs)

                continue

            converted = []

            for symbol in rhs:
                if symbol in working.nonterminals:
                    converted.append(symbol)

                else:
                    if symbol not in terminal_vars:
                        used_names = set(working.productions) | set(terminal_vars.values())
                        var = _fresh_name(used_names, "T")
                        terminal_vars[symbol] = var
                        result.add_production(var, (symbol,))

                    converted.append(terminal_vars[symbol])

            result.add_production(lhs, tuple(converted))

    final = Grammar(result.start)
    used = set(result.productions)

    for lhs, rhss in result.productions.items():
        for rhs in rhss:
            if len(rhs) <= 2:
                final.add_production(lhs, rhs)

                continue

            symbols = list(rhs)
            current = lhs

            while len(symbols) > 2:
                fresh = _fresh_name(used, "X")
                used.add(fresh)
                final.add_production(current, (symbols[0], fresh))
                current = fresh
                symbols = symbols[1:]

            final.add_production(current, tuple(symbols))

    final.print_grammar("GRAMÁTICA FINAL EN CNF")

    return final

def _fresh_name(used: set[str], prefix: str) -> str:
    i = 0

    while True:
        candidate = prefix if i == 0 else f"{prefix}{i}"

        if candidate not in used:
            return candidate
        
        i += 1

def _fresh_symbol(grammar: Grammar, prefix: str) -> str:
    return _fresh_name(grammar.nonterminals, prefix)