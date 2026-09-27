from dataclasses import dataclass, field

@dataclass
class Grammar:
    start: str
    productions: dict[str, list[tuple[str, ...]]] = field(default_factory=dict)

    def add_production(self, lhs: str, rhs: tuple[str, ...]) -> None:
        self.productions.setdefault(lhs, [])
        
        if rhs not in self.productions[lhs]:
            self.productions[lhs].append(rhs)

    @property
    def nonterminals(self) -> set[str]:
        return set(self.productions)

    def copy(self) -> "Grammar":
        return Grammar(
            self.start,
            {lhs: list(rhss) for lhs, rhss in self.productions.items()},
        )

    def print_grammar(self, title: str | None = None) -> None:
        if title:
            print()
            print(title)

        for lhs, alternatives in self.productions.items():
            rendered = ["ε" if not rhs else " ".join(rhs) for rhs in alternatives]
            print(f"{lhs} -> {' | '.join(rendered)}")