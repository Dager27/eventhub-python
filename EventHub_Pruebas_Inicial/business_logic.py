import math


BASE_PRICES = {
    "VIP": 100,
    "PREFERENCIAL": 75,
    "GENERAL": 50,
}

SERVICE_FEE = 5
MAX_TICKETS_PER_TRANSACTION = 10
RESERVATION_HOLD_MINUTES = 15


def _round2(value):
    """Replica Math.round(value * 100) / 100 de JavaScript."""
    return math.floor(value * 100 + 0.5) / 100


def _is_integer_number(value):
    """Replica Number.isInteger() para los valores usados por el sistema."""
    if isinstance(value, bool):
        return False
    if isinstance(value, int):
        return True
    if isinstance(value, float):
        return value.is_integer()
    return False


def calculateTicketPrice(input_data):
    zone = input_data["zone"]
    ticket_quantity = input_data["ticketQuantity"]
    days_before_event = input_data["daysBeforeEvent"]

    def empty_result(message):
        return {
            "valid": False,
            "basePrice": BASE_PRICES.get(zone, 0),
            "quantity": ticket_quantity,
            "subtotal": 0,
            "volumeDiscountPercentage": 0,
            "volumeDiscountAmount": 0,
            "earlyBookingDiscountPercentage": 0,
            "earlyBookingDiscountAmount": 0,
            "serviceFee": 0,
            "total": 0,
            "message": message,
        }

    if not _is_integer_number(ticket_quantity):
        return empty_result(
            "La cantidad de boletos debe ser un número entero."
        )

    if ticket_quantity < 1:
        return empty_result("Debe seleccionar al menos 1 boleto.")

    if ticket_quantity > MAX_TICKETS_PER_TRANSACTION:
        return empty_result(
            "Una transacción no puede superar los 10 boletos."
        )

    base_price = BASE_PRICES.get(zone)

    if base_price is None:
        return empty_result("La zona seleccionada no es válida.")

    subtotal = base_price * ticket_quantity

    volume_discount_percentage = 0

    if ticket_quantity >= 9:
        volume_discount_percentage = 18
    elif ticket_quantity >= 5:
        volume_discount_percentage = 10
    else:
        volume_discount_percentage = 0

    volume_discount_amount = _round2(
        subtotal * (volume_discount_percentage / 100)
    )

    early_booking_discount_percentage = 0

    if days_before_event > 15:
        early_booking_discount_percentage = 5

    early_booking_discount_amount = _round2(
        subtotal * (early_booking_discount_percentage / 100)
    )

    total = _round2(
        subtotal
        - volume_discount_amount
        - early_booking_discount_amount
        + SERVICE_FEE
    )

    message = "Precio calculado correctamente."

    if (
        volume_discount_percentage > 0
        and early_booking_discount_percentage > 0
    ):
        message = (
            "Descuento por volumen y descuento por compra "
            "anticipada aplicados."
        )
    elif volume_discount_percentage > 0:
        message = "Descuento por volumen aplicado."
    elif early_booking_discount_percentage > 0:
        message = "Descuento por compra anticipada aplicado."

    return {
        "valid": True,
        "basePrice": base_price,
        "quantity": ticket_quantity,
        "subtotal": _round2(subtotal),
        "volumeDiscountPercentage": volume_discount_percentage,
        "volumeDiscountAmount": volume_discount_amount,
        "earlyBookingDiscountPercentage": (
            early_booking_discount_percentage
        ),
        "earlyBookingDiscountAmount": early_booking_discount_amount,
        "serviceFee": SERVICE_FEE,
        "total": total,
        "message": message,
    }


def validateBookingEligibility(input_data):
    user_age = input_data["userAge"]
    minimum_age = input_data["minimumAge"]
    requested_tickets = input_data["requestedTickets"]
    remaining_zone_capacity = input_data["remainingZoneCapacity"]
    current_attendance = input_data["currentAttendance"]
    total_event_capacity = input_data["totalEventCapacity"]

    errors = []

    if requested_tickets < 1:
        errors.append(
            "La cantidad de boletos solicitada debe ser al menos 1."
        )

    if remaining_zone_capacity < 0:
        errors.append(
            "La capacidad restante de la zona no puede ser negativa."
        )

    if current_attendance < 0:
        errors.append("La asistencia actual no puede ser negativa.")

    if total_event_capacity <= 0:
        errors.append(
            "La capacidad total del evento debe ser mayor que 0."
        )

    if user_age < 0:
        errors.append("La edad del usuario no puede ser negativa.")

    if len(errors) > 0:
        return {
            "eligible": False,
            "occupancyPercentage": 0,
            "lastSeatsMode": False,
            "reason": "Los datos suministrados no son válidos.",
            "errors": errors,
        }

    occupancy_percentage = _round2(
        (current_attendance / total_event_capacity) * 100
    )

    last_seats_mode = occupancy_percentage > 90

    if user_age < minimum_age:
        return {
            "eligible": False,
            "occupancyPercentage": occupancy_percentage,
            "lastSeatsMode": last_seats_mode,
            "reason": (
                "El usuario no cumple con la edad mínima requerida."
            ),
            "errors": errors,
        }

    if requested_tickets > remaining_zone_capacity:
        return {
            "eligible": False,
            "occupancyPercentage": occupancy_percentage,
            "lastSeatsMode": last_seats_mode,
            "reason": (
                "No existen suficientes cupos disponibles en esta zona."
            ),
            "errors": errors,
        }

    if last_seats_mode and requested_tickets > 2:
        return {
            "eligible": False,
            "occupancyPercentage": occupancy_percentage,
            "lastSeatsMode": last_seats_mode,
            "reason": (
                "La ocupación supera el 90%. Solo pueden reservarse "
                "máximo 2 boletos."
            ),
            "errors": errors,
        }

    return {
        "eligible": True,
        "occupancyPercentage": occupancy_percentage,
        "lastSeatsMode": last_seats_mode,
        "reason": (
            "La reserva cumple con todas las reglas de negocio."
        ),
        "errors": errors,
    }


def evaluateEventAlerts(input_data):
    reservation_age_minutes = input_data["reservationAgeMinutes"]
    reservation_confirmed = input_data["reservationConfirmed"]
    tickets_sold = input_data["ticketsSold"]
    total_capacity = input_data["totalCapacity"]
    days_until_event = input_data["daysUntilEvent"]

    alerts = []

    reservation_expired = False

    if (
        not reservation_confirmed
        and reservation_age_minutes >= RESERVATION_HOLD_MINUTES
    ):
        reservation_expired = True
        alerts.append(
            "La reserva temporal ha expirado y los cupos deben liberarse."
        )

    occupancy_percentage = 0

    if total_capacity > 0:
        occupancy_percentage = _round2(
            (tickets_sold / total_capacity) * 100
        )

    critical_occupancy = False

    if occupancy_percentage >= 85:
        critical_occupancy = True
        alerts.append(
            "El evento ha alcanzado una ocupación crítica."
        )

    special_discount = False

    if days_until_event <= 3 and occupancy_percentage < 30:
        special_discount = True
        alerts.append(
            "Se recomienda activar el descuento especial por baja ocupación."
        )

    return {
        "reservationExpired": reservation_expired,
        "criticalOccupancy": critical_occupancy,
        "specialDiscount": special_discount,
        "occupancyPercentage": occupancy_percentage,
        "alerts": alerts,
    }
