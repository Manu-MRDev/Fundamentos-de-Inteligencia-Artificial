from problema_busqueda import ProblemaBusqueda


def crear_problema():
    estados = {"A", "B", "C", "D"}

    transiciones = {
        "A": {
            "B": 2,
            "C": 1
        },
        "B": {
            "A": 2,
            "D": 2
        },
        "C": {
            "B": 1,
            "D": 5
        },
        "D": {}
    }

    estado_inicial = "A"
    metas = {"D"}

    return ProblemaBusqueda(
        estados,
        transiciones,
        estado_inicial,
        metas
    )


def probar_transiciones(problema):
    print("=== PRUEBAS DEL MODELO ===")

    print("\n1. Validar estado A:")
    try:
        problema.validar_estado("A")
        print("Resultado: A es un estado válido.")
    except ValueError as error:
        print(error)

    print("\n2. Validar estado X:")
    try:
        problema.validar_estado("X")
        print("Resultado: X es válido.")
    except ValueError as error:
        print(f"Resultado esperado: {error}")

    print("\n3. Probar ruta A -> B -> D:")
    try:
        problema.aplicar_transicion("A", "B")
        problema.aplicar_transicion("B", "D")

        costo = (
            problema.costo("A", "B")
            + problema.costo("B", "D")
        )

        print("Ruta válida: A -> B -> D")
        print(f"Costo total: {costo} minutos")
    except ValueError as error:
        print(error)

    print("\n4. Probar movimiento B -> C:")
    try:
        problema.aplicar_transicion("B", "C")
        print("Movimiento válido.")
    except ValueError as error:
        print(f"Resultado esperado: {error}")

    print("\n5. Comprobar si D es una meta:")
    if problema.es_meta("D"):
        print("D es una meta.")
    else:
        print("D no es una meta.")


if __name__ == "__main__":
    problema = crear_problema()
    probar_transiciones(problema)
