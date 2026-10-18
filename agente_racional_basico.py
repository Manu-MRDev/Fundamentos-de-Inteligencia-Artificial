# agente_racional_basico.py

# Producto 3 - Aplicación en Python
# Fundamentos de Inteligencia Artificial
# Universidad Politécnica de Pachuca


class AgenteRacional:
    def __init__(self):
        self.ventilador = False
        self.historial = []
        self.desempeno = 0

    def percibir(self, temperatura):
        """El agente recibe una percepción del ambiente."""
        return {
            "temperatura": temperatura,
            "ventilador": self.ventilador
        }

    def decidir(self, percepcion):
        """El agente decide una acción según la percepción."""

        temperatura = percepcion["temperatura"]

        if temperatura >= 28:
            return "ENCENDER_VENTILADOR"

        elif temperatura <= 20:
            return "APAGAR_VENTILADOR"

        else:
            return "MANTENER_ESTADO"

    def actuar(self, accion):
        """El agente ejecuta la acción."""

        if accion == "ENCENDER_VENTILADOR":
            self.ventilador = True

        elif accion == "APAGAR_VENTILADOR":
            self.ventilador = False

        elif accion == "MANTENER_ESTADO":
            pass

    def evaluar(self, temperatura):
        """
        Evalúa el desempeño.
        El objetivo es mantener la temperatura
        dentro de un rango confortable.
        """

        if 20 <= temperatura <= 27:
            self.desempeno += 1

    def ciclo(self, temperatura):
        """Ejecuta un ciclo completo del agente."""

        percepcion = self.percibir(temperatura)
        accion = self.decidir(percepcion)

        self.actuar(accion)
        self.evaluar(temperatura)

        registro = {
            "temperatura": temperatura,
            "accion": accion,
            "ventilador": self.ventilador,
            "desempeno": self.desempeno
        }

        self.historial.append(registro)

        return registro

    def mostrar_historial(self):
        """Muestra todas las percepciones y acciones."""

        print("\n===== HISTORIAL DEL AGENTE =====")

        for i, registro in enumerate(self.historial, start=1):
            print(f"\nCiclo {i}")
            print(f"Temperatura: {registro['temperatura']} °C")
            print(f"Acción: {registro['accion']}")

            if registro["ventilador"]:
                print("Estado del ventilador: ENCENDIDO")
            else:
                print("Estado del ventilador: APAGADO")

        print("\nDesempeño total:", self.desempeno)


def main():

    agente = AgenteRacional()

    print("===== AGENTE RACIONAL BÁSICO =====")
    print("El agente controla un ventilador según la temperatura.")
    print("Escribe 'fin' para terminar.\n")

    while True:

        entrada = input("Temperatura actual en °C: ")

        if entrada.lower() == "fin":
            break

        try:
            temperatura = float(entrada)

            if temperatura < -50 or temperatura > 60:
                print("Temperatura fuera del rango permitido.")
                continue

            resultado = agente.ciclo(temperatura)

            print("\nPercepción:", temperatura, "°C")
            print("Acción seleccionada:", resultado["accion"])

            if resultado["ventilador"]:
                print("Ventilador: ENCENDIDO")
            else:
                print("Ventilador: APAGADO")

        except ValueError:
            print("Error: introduce una temperatura numérica.")

    agente.mostrar_historial()


if __name__ == "__main__":
    main()