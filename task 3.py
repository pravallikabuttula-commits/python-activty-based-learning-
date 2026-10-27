from dataclasses import dataclass


@dataclass
class Patient:
    patient_id: str
    name: str
    age: int
    consultation_charge: float
    diagnostic_charge: float
    treatment_charge: float
    insurance_coverage: float
    is_senior_citizen: bool = False
    is_low_income: bool = False
    emergency_case: bool = False


def validate_patient(patient):
    """Validate billing constraints."""
    if not patient.patient_id or not patient.name:
        raise ValueError("Patient ID and name are required.")

    if patient.age < 0 or patient.age > 120:
        raise ValueError("Age must be between 0 and 120.")

    charges = [
        patient.consultation_charge,
        patient.diagnostic_charge,
        patient.treatment_charge,
        patient.insurance_coverage
    ]

    if any(charge < 0 for charge in charges):
        raise ValueError("Charges and insurance coverage cannot be negative.")


def calculate_bill(patient):
    """Calculate bill with insurance and applicable concessions."""
    validate_patient(patient)

    gross_amount = (
        patient.consultation_charge
        + patient.diagnostic_charge
        + patient.treatment_charge
    )

    # Insurance cannot exceed gross bill amount
    insurance_amount = min(patient.insurance_coverage, gross_amount)
    amount_after_insurance = gross_amount - insurance_amount

    concession_rate = 0

    # Conditional concession rules
    if patient.is_senior_citizen:
        concession_rate = max(concession_rate, 0.15)  # 15%

    if patient.is_low_income:
        concession_rate = max(concession_rate, 0.20)  # 20%

    if patient.emergency_case:
        concession_rate = max(concession_rate, 0.10)  # 10%

    concession_amount = amount_after_insurance * concession_rate
    final_payable = amount_after_insurance - concession_amount

    return {
        "gross_amount": gross_amount,
        "insurance_amount": insurance_amount,
        "concession_rate": concession_rate * 100,
        "concession_amount": concession_amount,
        "final_payable": final_payable
    }


def classify_patient(bill_details):
    """
    Payment policy classification:
    Fully Covered: Insurance pays the complete bill.
    Subsidized: A concession was granted.
    Standard: Patient pays normally.
    High Bill: Final payable amount is above ₹50,000.
    """
    if bill_details["gross_amount"] == bill_details["insurance_amount"]:
        return "Fully Covered"

    if bill_details["final_payable"] > 50000:
        return "High Bill"

    if bill_details["concession_amount"] > 0:
        return "Subsidized"

    return "Standard"


def process_patient(patient):
    bill = calculate_bill(patient)
    classification = classify_patient(bill)

    print("\nPATIENT BILL")
    print("-" * 40)
    print("Patient ID:", patient.patient_id)
    print("Patient Name:", patient.name)
    print("Classification:", classification)
    print("Gross Amount: ₹", bill["gross_amount"])
    print("Insurance Coverage: ₹", bill["insurance_amount"])
    print("Concession Rate:", bill["concession_rate"], "%")
    print("Concession Amount: ₹", bill["concession_amount"])
    print("Final Payable Amount: ₹", bill["final_payable"])


# Example patients
patients = [
    Patient(
        patient_id="P101",
        name="Anjali Sharma",
        age=68,
        consultation_charge=800,
        diagnostic_charge=4500,
        treatment_charge=25000,
        insurance_coverage=10000,
        is_senior_citizen=True
    ),
    Patient(
        patient_id="P102",
        name="Rahul Verma",
        age=35,
        consultation_charge=1000,
        diagnostic_charge=5000,
        treatment_charge=60000,
        insurance_coverage=15000,
        is_low_income=True
    ),
    Patient(
        patient_id="P103",
        name="Kiran Patel",
        age=42,
        consultation_charge=700,
        diagnostic_charge=3000,
        treatment_charge=12000,
        insurance_coverage=15700
    )
]

for patient in patients:
    process_patient(patient)