# hitos_ia.py

# Producto 3 - Aplicación en Python
# Fundamentos de Inteligencia Artificial
# Universidad Politécnica de Pachuca

hitos = [
    {
        "anio": 1936,
        "nombre": "Máquina de Turing",
        "problema": "Determinar qué puede calcularse mediante procedimientos mecánicos.",
        "tecnica": "Modelo formal de computación.",
        "logro": "Formalizó el concepto de computación mecánica.",
        "limitacion": "No constituye por sí misma una inteligencia artificial.",
        "consecuencia": "Estableció fundamentos para la computación moderna."
    },
    {
        "anio": 1943,
        "nombre": "McCulloch y Pitts",
        "problema": "Representar matemáticamente el funcionamiento de una neurona.",
        "tecnica": "Neurona artificial binaria.",
        "logro": "Permitió representar funciones lógicas mediante redes neuronales.",
        "limitacion": "No incluía un mecanismo de aprendizaje.",
        "consecuencia": "Sentó bases para el conexionismo."
    },
    {
        "anio": 1950,
        "nombre": "Test de Turing",
        "problema": "Evaluar si una máquina puede comportarse como una persona.",
        "tecnica": "Juego de imitación.",
        "logro": "Propuso una forma operacional de discutir la inteligencia de una máquina.",
        "limitacion": "No demuestra comprensión real.",
        "consecuencia": "Se convirtió en una referencia para la IA y el lenguaje."
    },
    {
        "anio": 1956,
        "nombre": "Conferencia de Dartmouth",
        "problema": "Investigar cómo las máquinas pueden realizar tareas consideradas inteligentes.",
        "tecnica": "Programación simbólica y razonamiento automatizado.",
        "logro": "Se consolidó el término Inteligencia Artificial.",
        "limitacion": "El concepto de inteligencia artificial podía interpretarse de diferentes maneras.",
        "consecuencia": "Impulsó el desarrollo de la IA simbólica."
    },
    {
        "anio": 1956,
        "nombre": "Logic Theorist",
        "problema": "Automatizar la demostración de teoremas matemáticos.",
        "tecnica": "Búsqueda heurística.",
        "logro": "Resolución automatizada de problemas matemáticos.",
        "limitacion": "Funcionaba principalmente en problemas estructurados.",
        "consecuencia": "Impulsó el desarrollo de la resolución automática de problemas."
    },
    {
        "anio": 1958,
        "nombre": "Perceptrón de Rosenblatt",
        "problema": "Clasificar patrones mediante una máquina que pudiera aprender.",
        "tecnica": "Ajuste de pesos.",
        "logro": "Permitió aprender a partir de ejemplos.",
        "limitacion": "No podía resolver problemas que no fueran linealmente separables.",
        "consecuencia": "Se convirtió en un antecedente de las redes neuronales."
    },
    {
        "anio": 1969,
        "nombre": "Crítica al Perceptrón",
        "problema": "Analizar matemáticamente las limitaciones de los perceptrones.",
        "tecnica": "Análisis matemático.",
        "logro": "Se mostró la dificultad para resolver problemas como XOR con una sola capa.",
        "limitacion": "Los perceptrones de una capa eran insuficientes para ciertos problemas.",
        "consecuencia": "Contribuyó al primer invierno de la IA."
    },
    {
        "anio": 1974,
        "nombre": "Primer invierno de la IA",
        "problema": "Las expectativas de la IA eran mayores que los resultados obtenidos.",
        "tecnica": "Programación simbólica y métodos iniciales de IA.",
        "logro": "Se identificaron limitaciones metodológicas y computacionales.",
        "limitacion": "La capacidad computacional disponible era insuficiente.",
        "consecuencia": "Disminuyeron el financiamiento y el interés en algunos enfoques."
    },
    {
        "anio": 1970,
        "nombre": "Sistemas expertos",
        "problema": "Utilizar conocimiento especializado para resolver problemas concretos.",
        "tecnica": "Reglas e inferencia.",
        "logro": "Aplicación práctica de la IA en dominios como diagnóstico.",
        "limitacion": "Requerían conocimiento introducido manualmente y no se adaptaban fácilmente.",
        "consecuencia": "La IA comenzó a utilizarse en aplicaciones industriales y especializadas."
    },
    {
        "anio": 1986,
        "nombre": "Backpropagation",
        "problema": "Entrenar redes neuronales con múltiples capas.",
        "tecnica": "Retropropagación del error.",
        "logro": "Permitió ajustar los pesos de redes neuronales multicapa.",
        "limitacion": "El entrenamiento podía ser costoso computacionalmente.",
        "consecuencia": "Se convirtió en una base importante para el Deep Learning."
    },
    {
        "anio": 1997,
        "nombre": "Deep Blue",
        "problema": "Tomar decisiones en el ajedrez.",
        "tecnica": "Búsqueda computacional a gran escala.",
        "logro": "Derrotó a Garry Kasparov.",
        "limitacion": "Era un sistema especializado y no representaba inteligencia general.",
        "consecuencia": "Demostró el potencial de combinar algoritmos y capacidad computacional."
    },
    {
        "anio": 2009,
        "nombre": "ImageNet",
        "problema": "Disponer de grandes cantidades de datos etiquetados para visión artificial.",
        "tecnica": "Base de datos masiva de imágenes.",
        "logro": "Se convirtió en referencia para evaluar algoritmos de visión.",
        "limitacion": "El etiquetado es costoso y puede introducir sesgos.",
        "consecuencia": "Impulsó el desarrollo del Deep Learning aplicado a visión."
    },
    {
        "anio": 2012,
        "nombre": "AlexNet",
        "problema": "Reconocer objetos en imágenes.",
        "tecnica": "Red neuronal convolucional profunda y GPU.",
        "logro": "Mejoró significativamente los resultados en ImageNet.",
        "limitacion": "Necesitaba grandes cantidades de datos y recursos computacionales.",
        "consecuencia": "Impulsó la adopción del Deep Learning."
    },
    {
        "anio": 2016,
        "nombre": "AlphaGo",
        "problema": "Resolver el enorme espacio de búsqueda del juego Go.",
        "tecnica": "Redes neuronales y aprendizaje por refuerzo.",
        "logro": "Derrotó a Lee Sedol 4-1.",
        "limitacion": "Continuaba siendo un sistema especializado.",
        "consecuencia": "Demostró la utilidad de redes neuronales para decisiones complejas."
    },
    {
        "anio": 2017,
        "nombre": "Transformers y BERT",
        "problema": "Procesar lenguaje considerando el contexto.",
        "tecnica": "Arquitectura Transformer y mecanismo de atención.",
        "logro": "BERT obtuvo resultados importantes en tareas de procesamiento de lenguaje.",
        "limitacion": "Requiere grandes cantidades de datos y recursos.",
        "consecuencia": "Estableció una base para los modelos modernos de lenguaje."
    },
    {
        "anio": 2020,
        "nombre": "GPT-3",
        "problema": "Construir modelos capaces de realizar múltiples tareas de lenguaje.",
        "tecnica": "Transformer autorregresivo.",
        "logro": "Realizó tareas mediante ejemplos sin actualizar sus parámetros.",
        "limitacion": "Puede producir información incorrecta y presenta limitaciones de razonamiento.",
        "consecuencia": "Consolidó el desarrollo de los grandes modelos de lenguaje."
    },
    {
        "anio": 2022,
        "nombre": "ChatGPT",
        "problema": "Facilitar la interacción de las personas con modelos de lenguaje.",
        "tecnica": "Modelo de lenguaje con aprendizaje por refuerzo a partir de retroalimentación humana.",
        "logro": "Popularizó la interacción conversacional con IA generativa.",
        "limitacion": "Puede producir información incorrecta y presentar sesgos.",
        "consecuencia": "Aumentó ampliamente el uso de la IA generativa."
    },
    {
        "anio": 2024,
        "nombre": "IA multimodal",
        "problema": "Procesar diferentes tipos de información como texto, imagen, audio y video.",
        "tecnica": "Modelos generativos multimodales.",
        "logro": "Permite combinar diferentes modalidades de información.",
        "limitacion": "Persisten riesgos de errores, sesgos y privacidad.",
        "consecuencia": "La IA se utiliza como herramienta de propósito general."
    }
]


def validar_hito(hito):
    """Valida que un hito tenga un año válido."""
    return (
        isinstance(hito["anio"], int)
        and 1850 <= hito["anio"] <= 2100
    )


def ordenar_hitos(lista):
    """Ordena los hitos por año."""
    return sorted(lista, key=lambda hito: hito["anio"])


def mostrar_hito(hito):
    """Muestra la información de un hito."""
    print("=" * 70)
    print(f"{hito['anio']} - {hito['nombre']}")
    print(f"Problema: {hito['problema']}")
    print(f"Técnica: {hito['tecnica']}")
    print(f"Logro: {hito['logro']}")
    print(f"Limitación: {hito['limitacion']}")
    print(f"Consecuencia: {hito['consecuencia']}")


def generar_timeline():
    """Genera y muestra la línea del tiempo."""
    print("\nLINEA DEL TIEMPO DE LA INTELIGENCIA ARTIFICIAL")
    print("=" * 70)

    validos = []

    for hito in hitos:
        if validar_hito(hito):
            validos.append(hito)
        else:
            print(f"Advertencia: hito inválido -> {hito}")

    for hito in ordenar_hitos(validos):
        mostrar_hito(hito)

    print("=" * 70)
    print(f"Total de hitos válidos: {len(validos)}")


def buscar_por_anio():
    """Permite consultar un hito por año."""
    try:
        anio = int(input("\nEscribe el año que quieres consultar: "))

        encontrados = [
            hito for hito in hitos
            if hito["anio"] == anio
        ]

        if encontrados:
            for hito in encontrados:
                mostrar_hito(hito)
        else:
            print("No se encontró un hito para ese año.")

    except ValueError:
        print("Error: debes escribir un año numérico.")


def menu():
    while True:
        print("\n===== HITOS DE INTELIGENCIA ARTIFICIAL =====")
        print("1. Mostrar línea del tiempo")
        print("2. Buscar hito por año")
        print("3. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            generar_timeline()
        elif opcion == "2":
            buscar_por_anio()
        elif opcion == "3":
            print("Programa finalizado.")
            break
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    menu()