# Laboratorio-No.-7-Teoria-de-la-computacion
## Requisitos

- Python 3.10 o superior.
- No requiere librerías externas.

## Ejecución

Desde esta carpeta:

```bash
python main.py
```

## Operaciones

El programa realiza, en este orden:

1. Validación sintáctica mediante expresión regular.
2. Lectura e interpretación de la CFG.
3. Identificación de símbolos anulables.
4. Eliminación de producciones ε.
5. Eliminación de producciones unitarias.
6. Eliminación de símbolos no productores.
7. Eliminación de símbolos no alcanzables.
8. Conversión a Forma Normal de Chomsky.

Para una producción con `m` símbolos anulables se generan explícitamente los `2^m` casos posibles.

## Convención de entrada

- Mayúsculas: no terminales.
- Minúsculas y dígitos: terminales.
- `->`: producción.
- `|`: OR.
- `ε`: producción vacía.

Ejemplo:

```text
S -> 0A0 | 1B1 | BB
```