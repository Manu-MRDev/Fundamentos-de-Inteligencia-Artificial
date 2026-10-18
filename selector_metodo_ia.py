# selector_metodo_ia.py

# Producto 3 - Aplicación en Python
# Fundamentos de Inteligencia Artificial
# Universidad Politécnica de Pachuca


def mostrar_opciones():

    print("\n===== SELECTOR DE MÉTODO DE IA =====")

    print("\nTipo de datos:")
    print("1. Reglas y hechos")
    print("2. Datos tabulares")
    print("3. Imágenes")
    print("4. Texto")
    print("5. Datos multimodales")
    print("6. No definido")

    datos = input("Selecciona el tipo de datos: ")

    print("\nNivel de incertidumbre:")
    print("1. Bajo")
    print("2. Medio")
    print("3. Alto")
    print("4. No definido")

    incertidumbre = input("Selecciona el nivel de incertidumbre: ")

    print("\n¿Se necesita alta explicabilidad?")
    print("1. Sí")
    print("2. No")
    print("3. No definido")

    explicabilidad = input("Selecciona una opción: ")

    print("\nRestricciones principales:")
    print("1. Recursos limitados")
    print("2. Tiempo de respuesta")
    print("3. Privacidad")
    print("4. No definidas")

    restricciones = input("Selecciona una opción: ")

    print("\nTipo de salida:")
    print("1. Decisión")
    print("2. Clasificación")
    print("3. Predicción")
    print("4. Generación de texto")
    print("5. Generación multimodal")
    print("6. No definido")

    salida = input("Selecciona una opción: ")

    return datos, incertidumbre, explicabilidad, restricciones, salida


def seleccionar_metodo(
    datos,
    incertidumbre,
    explicabilidad,
    restricciones,
    salida
):

    advertencias = []
    razones = []

    # Comprobamos si falta información importante.

    if datos == "6":
        advertencias.append(
            "No se definió el tipo de datos."
        )

    if incertidumbre == "4":
        advertencias.append(
            "No se definió el nivel de incertidumbre."
        )

    if explicabilidad == "3":
        advertencias.append(
            "No se definió la necesidad de explicabilidad."
        )

    if restricciones == "4":
        advertencias.append(
            "No se definieron las restricciones."
        )

    if salida == "6":
        advertencias.append(
            "No se definió el tipo de salida."
        )

    # -------------------------------------------------
    # REGLAS Y HECHOS
    # -------------------------------------------------

    if datos == "1":

        if explicabilidad == "1":

            metodo = "IA simbólica"

            razones.append(
                "Los datos están representados mediante reglas y hechos."
            )

            razones.append(
                "La alta explicabilidad favorece el uso de reglas e inferencia."
            )

        else:

            metodo = "IA simbólica o enfoque híbrido"

            razones.append(
                "El problema utiliza reglas y hechos."
            )

            razones.append(
                "Un enfoque híbrido podría complementar las reglas "
                "con métodos de aprendizaje."
            )

    # -------------------------------------------------
    # IMÁGENES
    # -------------------------------------------------

    elif datos == "3":

        metodo = "Deep Learning"

        razones.append(
            "El problema utiliza imágenes como entrada."
        )

        razones.append(
            "Las redes neuronales profundas pueden aprender "
            "representaciones de características visuales."
        )

        if restricciones == "1":

            advertencias.append(
                "Los recursos limitados pueden dificultar "
                "el entrenamiento de modelos profundos."
            )

    # -------------------------------------------------
    # TEXTO
    # -------------------------------------------------

    elif datos == "4":

        if salida == "4":

            metodo = "IA generativa basada en Transformers"

            razones.append(
                "La entrada principal es texto."
            )

            razones.append(
                "La salida requerida es generación de texto."
            )

        else:

            metodo = "Machine Learning o modelos de lenguaje"

            razones.append(
                "El problema utiliza información textual."
            )

            razones.append(
                "La selección depende de si se requiere clasificación, "
                "predicción o generación."
            )

    # -------------------------------------------------
    # MULTIMODAL
    # -------------------------------------------------

    elif datos == "5":

        metodo = "IA multimodal"

        razones.append(
            "El problema combina diferentes tipos de información."
        )

        razones.append(
            "Los modelos multimodales permiten trabajar con "
            "más de una modalidad."
        )

    # -------------------------------------------------
    # DATOS TABULARES
    # -------------------------------------------------

    elif datos == "2":

        if incertidumbre == "3":

            metodo = "Machine Learning probabilístico"

            razones.append(
                "Los datos son estructurados."
            )

            razones.append(
                "Existe un nivel alto de incertidumbre."
            )

        else:

            metodo = "Machine Learning"

            razones.append(
                "Los datos están organizados de forma tabular."
            )

            razones.append(
                "Los métodos de Machine Learning pueden utilizar "
                "variables de entrada para realizar predicciones "
                "o clasificaciones."
            )

    # -------------------------------------------------
    # INFORMACIÓN INSUFICIENTE
    # -------------------------------------------------

    else:

        metodo = "Información insuficiente"

        advertencias.append(
            "No existen suficientes datos para seleccionar "
            "un método de IA de forma responsable."
        )

    return metodo, razones, advertencias


def mostrar_resultado(metodo, razones, advertencias):

    print("\n")
    print("=" * 60)
    print("RESULTADO DEL SELECTOR")
    print("=" * 60)

    print("\nMétodo recomendado preliminar:")
    print(">>>", metodo)

    print("\nRazones:")

    if razones:

        for razon in razones:
            print("-", razon)

    else:

        print("- No hay razones suficientes.")

    print("\nAdvertencias:")

    if advertencias:

        for advertencia in advertencias:
            print("!", advertencia)

    else:

        print("- No se detectaron advertencias.")

    print("\nNota:")
    print(
        "La recomendación es preliminar y debe validarse "
        "con las características reales del problema, "
        "los datos disponibles y las restricciones del sistema."
    )


def main():

    datos, incertidumbre, explicabilidad, restricciones, salida = (
        mostrar_opciones()
    )

    metodo, razones, advertencias = seleccionar_metodo(
        datos,
        incertidumbre,
        explicabilidad,
        restricciones,
        salida
    )

    mostrar_resultado(
        metodo,
        razones,
        advertencias
    )


if __name__ == "__main__":
    main()