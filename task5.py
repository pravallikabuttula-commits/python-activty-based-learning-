from dataclasses import dataclass


@dataclass
class Passenger:
    name: str
    age: int
    distance_km: int
    travel_class: str
    cancelled: bool = False
    cancellation_time: int = 0  # Hours before departure


def calculate_base_fare(distance):
    """
    Distance slabs:
    First 100 km       -> ₹1.00/km
    Next 200 km        -> ₹0.80/km
    Above 300 km       -> ₹0.60/km
    """
    if distance <= 100:
        return distance * 1.00

    elif distance <= 300:
        return (100 * 1.00) + ((distance - 100) * 0.80)

    else:
        return (100 * 1.00) + (200 * 0.80) + ((distance - 300) * 0.60)


def get_class_multiplier(travel_class):
    class_rates = {
        "Sleeper": 1.0,
        "AC 3 Tier": 1.8,
        "AC 2 Tier": 2.5,
        "First Class": 3.5
    }

    if travel_class not in class_rates:
        raise ValueError("Invalid travel class.")

    return class_rates[travel_class]


def get_age_concession(age):
    """
    Children below 12 years -> 50% concession
    Senior citizens 60+    -> 30% concession
    Others                 -> No concession
    """
    if age < 12:
        return 0.50
    elif age >= 60:
        return 0.30
    return 0.0


def calculate_cancellation_penalty(total_fare, hours_before_departure):
    """
    Cancellation penalties:
    More than 48 hours before departure -> 10%
    24 to 48 hours before departure     -> 25%
    Less than 24 hours before departure -> 50%
    """
    if hours_before_departure > 48:
        return total_fare * 0.10
    elif hours_before_departure >= 24:
        return total_fare * 0.25
    else:
        return total_fare * 0.50


def calculate_passenger_fare(passenger, reservation_fee=40):
    if passenger.age < 0:
        raise ValueError("Age cannot be negative.")

    if passenger.distance_km <= 0:
        raise ValueError("Distance must be greater than zero.")

    base_fare = calculate_base_fare(passenger.distance_km)

    # Apply travel class multiplier
    class_fare = base_fare * get_class_multiplier(passenger.travel_class)

    # Apply age concession
    concession_rate = get_age_concession(passenger.age)
    concession_amount = class_fare * concession_rate

    # Add reservation fee after concession
    total_fare = class_fare - concession_amount + reservation_fee

    cancellation_penalty = 0
    refund_amount = 0

    if passenger.cancelled:
        cancellation_penalty = calculate_cancellation_penalty(
            total_fare,
            passenger.cancellation_time
        )
        refund_amount = total_fare - cancellation_penalty

    return {
        "name": passenger.name,
        "base_fare": base_fare,
        "class_fare": class_fare,
        "concession_amount": concession_amount,
        "reservation_fee": reservation_fee,
        "total_fare": total_fare,
        "cancelled": passenger.cancelled,
        "cancellation_penalty": cancellation_penalty,
        "refund_amount": refund_amount
    }


# Multiple passengers
passengers = [
    Passenger("Arjun", 25, 450, "Sleeper"),
    Passenger("Meera", 65, 450, "AC 3 Tier"),
    Passenger("Riya", 10, 180, "Sleeper"),
    Passenger("Kabir", 35, 600, "AC 2 Tier", cancelled=True, cancellation_time=20)
]

print("RAILWAY FARE AND RESERVATION DETAILS")
print("-" * 65)

total_booking_amount = 0

for passenger in passengers:
    bill = calculate_passenger_fare(passenger)
    total_booking_amount += bill["total_fare"]

    print(f"\nPassenger: {bill['name']}")
    print(f"Base Fare: ₹{bill['base_fare']:.2f}")
    print(f"Fare After Class Rate: ₹{bill['class_fare']:.2f}")
    print(f"Age Concession: ₹{bill['concession_amount']:.2f}")
    print(f"Reservation Fee: ₹{bill['reservation_fee']:.2f}")
    print(f"Booked Fare: ₹{bill['total_fare']:.2f}")

    if bill["cancelled"]:
        print("Status: Cancelled")
        print(f"Cancellation Penalty: ₹{bill['cancellation_penalty']:.2f}")
        print(f"Refund Amount: ₹{bill['refund_amount']:.2f}")
    else:
        print("Status: Confirmed")

print("\n" + "-" * 65)
print(f"Total Booking Amount: ₹{total_booking_amount:.2f}")