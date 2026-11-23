from pprint import pprint

from business_logic import (
    calculateTicketPrice,
    validateBookingEligibility,
    evaluateEventAlerts,
)


def leer_numero(mensaje):
    """Lee un entero o decimal desde la terminal."""
    while True:
        valor = input(mensaje).strip().replace(",", ".")
        try:
            numero = float(valor)
            return int(numero) if numero.is_integer() else numero
        except ValueError:
            print("Entrada inválida. Ingresa un número.")


def leer_booleano(mensaje):
    """Lee una respuesta afirmativa o negativa."""
    while True:
        valor = input(mensaje).strip().lower()
        if valor in ("s", "si", "sí", "true", "1", "y", "yes"):
            return True
        if valor in ("n", "no", "false", "0"):
            return False
        print("Respuesta inválida. Escribe sí o no.")


def mostrar_resultado(resultado):
    print("\nResultado:")
    pprint(resultado, sort_dicts=False)
    print()


def simular_precio():
    print("\n--- CALCULATE TICKET PRICE ---")
    datos = {
        "zone": input("Zona (VIP, PREFERENCIAL, GENERAL): ").strip().upper(),
        "ticketQuantity": leer_numero("Cantidad de boletos: "),
        "daysBeforeEvent": leer_numero("Días antes del evento: "),
    }
    mostrar_resultado(calculateTicketPrice(datos))


def simular_reserva():
    print("\n--- VALIDATE BOOKING ELIGIBILITY ---")
    datos = {
        "userAge": leer_numero("Edad del usuario: "),
        "minimumAge": leer_numero("Edad mínima requerida: "),
        "requestedTickets": leer_numero("Boletos solicitados: "),
        "remainingZoneCapacity": leer_numero("Capacidad restante de la zona: "),
        "currentAttendance": leer_numero("Asistencia actual: "),
        "totalEventCapacity": leer_numero("Capacidad total del evento: "),
    }
    mostrar_resultado(validateBookingEligibility(datos))


def simular_alertas():
    print("\n--- EVALUATE EVENT ALERTS ---")
    datos = {
        "reservationAgeMinutes": leer_numero("Antigüedad de la reserva en minutos: "),
        "reservationConfirmed": leer_booleano("¿La reserva está confirmada? (s/n): "),
        "ticketsSold": leer_numero("Boletos vendidos: "),
        "totalCapacity": leer_numero("Capacidad total del evento: "),
        "daysUntilEvent": leer_numero("Días que faltan para el evento: "),
    }
    mostrar_resultado(evaluateEventAlerts(datos))


def main():
    while True:
        print("======================================")
        print(" EVENTHUB - SIMULADOR DE FUNCIONES")
        print("======================================")
        print("1. Simular cálculo del precio de boletos")
        print("2. Simular validación de reserva")
        print("3. Simular alertas del evento")
        print("0. Salir")

        opcion = input("\nSelecciona una opción: ").strip()

        try:
            if opcion == "1":
                simular_precio()
            elif opcion == "2":
                simular_reserva()
            elif opcion == "3":
                simular_alertas()
            elif opcion == "0":
                print("Simulador finalizado.")
                break
            else:
                print("Opción no válida. Intenta nuevamente.\n")
        except (KeyError, TypeError, ValueError, ZeroDivisionError) as error:
            print(f"\nLa función produjo un error con esos datos: {error}\n")


if __name__ == "__main__":
    main()
