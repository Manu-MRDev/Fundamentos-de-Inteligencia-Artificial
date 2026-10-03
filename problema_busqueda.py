class ProblemaBusqueda:
    def __init__(self, estados, transiciones, estado_inicial, metas):
        self.estados = estados
        self.transiciones = transiciones
        self.estado_inicial = estado_inicial
        self.metas = metas

    def validar_estado(self, estado):
        if estado not in self.estados:
            raise ValueError(
                f"Estado inválido: {estado}. "
                f"Debe pertenecer al espacio de estados."
            )
        return True

    def acciones_validas(self, estado):
        self.validar_estado(estado)

        if estado not in self.transiciones:
            return []

        return list(self.transiciones[estado].keys())

    def aplicar_transicion(self, estado, destino):
        self.validar_estado(estado)

        acciones = self.acciones_validas(estado)

        if destino not in acciones:
            raise ValueError(
                f"Transición inválida: {estado} -> {destino}. "
                f"No existe esa conexión."
            )

        return destino

    def es_meta(self, estado):
        self.validar_estado(estado)
        return estado in self.metas

    def costo(self, estado, destino):
        self.validar_estado(estado)

        if destino not in self.acciones_validas(estado):
            raise ValueError(
                f"No existe una transición válida "
                f"de {estado} hacia {destino}."
            )

        return self.transiciones[estado][destino]


# Pruebas básicas de la clase
if __name__ == "__main__":
    print("=== PRUEBAS DE LA CLASE ProblemaBusqueda ===")

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

    problema = ProblemaBusqueda(
        estados,
        transiciones,
        estado_inicial,
        metas
    )

    print("\n1. Validar estado A:")
    try:
        problema.validar_estado("A")
        print("Resultado: A es válido.")
    except ValueError as error:
        print(f"Error: {error}")

    print("\n2. Validar estado X:")
    try:
        problema.validar_estado("X")
        print("Resultado: X es válido.")
    except ValueError as error:
        print(f"Resultado esperado: {error}")

    print("\n3. Obtener acciones válidas desde A:")
    acciones = problema.acciones_validas("A")
    print(f"Acciones: {acciones}")

    print("\n4. Aplicar transición A -> B:")
    try:
        resultado = problema.aplicar_transicion("A", "B")
        print(f"Resultado: A -> {resultado}")
    except ValueError as error:
        print(f"Error: {error}")

    print("\n5. Probar transición B -> C:")
    try:
        problema.aplicar_transicion("B", "C")
        print("Resultado: transición válida.")
    except ValueError as error:
        print(f"Resultado esperado: {error}")

    print("\n6. Calcular costo A -> B:")
    try:
        costo = problema.costo("A", "B")
        print(f"Costo: {costo} minutos")
    except ValueError as error:
        print(f"Error: {error}")

    print("\n7. Comprobar si D es una meta:")
    if problema.es_meta("D"):
        print("Resultado: D es una meta.")
    else:
        print("Resultado: D no es una meta.")