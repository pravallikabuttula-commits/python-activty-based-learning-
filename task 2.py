from dataclasses import dataclass


@dataclass
class ElectricityBill:
    month: str
    units_consumed: int
    energy_charge: float
    fixed_charge: float
    surcharge: float
    rebate: float
    total_bill: float


def calculate_energy_charge(units):
    """
    Progressive slab rates:
    0–100 units     : ₹1.50 per unit
    101–200 units   : ₹2.50 per unit
    201–300 units   : ₹4.00 per unit
    Above 300 units : ₹6.00 per unit
    """
    charge = 0

    if units <= 100:
        charge = units * 1.50

    elif units <= 200:
        charge = (100 * 1.50) + ((units - 100) * 2.50)

    elif units <= 300:
        charge = (100 * 1.50) + (100 * 2.50) + ((units - 200) * 4.00)

    else:
        charge = (
            (100 * 1.50)
            + (100 * 2.50)
            + (100 * 4.00)
            + ((units - 300) * 6.00)
        )

    return charge


def calculate_bill(month, units, fixed_charge=100, surcharge_rate=0.05):
    energy_charge = calculate_energy_charge(units)

    # Surcharge is calculated on energy charge
    surcharge = energy_charge * surcharge_rate

    # Rebate for low usage
    rebate = 50 if units <= 100 else 0

    total_bill = energy_charge + fixed_charge + surcharge - rebate

    return ElectricityBill(
        month=month,
        units_consumed=units,
        energy_charge=energy_charge,
        fixed_charge=fixed_charge,
        surcharge=surcharge,
        rebate=rebate,
        total_bill=total_bill
    )


def find_unusual_increases(bills, percentage_limit=25):
    """
    Detect bills that increased more than percentage_limit
    compared with the previous month.
    """
    unusual_months = []

    for i in range(1, len(bills)):
        previous_bill = bills[i - 1]
        current_bill = bills[i]

        increase_percentage = (
            (current_bill.total_bill - previous_bill.total_bill)
            / previous_bill.total_bill
        ) * 100

        if increase_percentage > percentage_limit:
            unusual_months.append(
                (current_bill.month, increase_percentage)
            )

    return unusual_months


# Monthly electricity consumption data
monthly_usage = [
    ("January", 95),
    ("February", 120),
    ("March", 180),
    ("April", 350),
    ("May", 220),
    ("June", 500)
]

# Calculate each monthly bill
bills = []
for month, units in monthly_usage:
    bill = calculate_bill(month, units)
    bills.append(bill)

# Display bill comparison
print("ELECTRICITY BILL COMPARISON")
print("-" * 75)
print(f"{'Month':<12}{'Units':<10}{'Energy':<12}{'Surcharge':<12}{'Rebate':<10}{'Total Bill'}")
print("-" * 75)

for bill in bills:
    print(
        f"{bill.month:<12}"
        f"{bill.units_consumed:<10}"
        f"₹{bill.energy_charge:<11.2f}"
        f"₹{bill.surcharge:<11.2f}"
        f"₹{bill.rebate:<9.2f}"
        f"₹{bill.total_bill:.2f}"
    )

# Identify unusual increases
unusual_increases = find_unusual_increases(bills)

print("\nUNUSUAL BILL INCREASES")
print("-" * 30)

if unusual_increases:
    for month, increase in unusual_increases:
        print(f"{month}: Bill increased by {increase:.2f}%")
else:
    print("No unusual increases found.")