def extract_invoice_record(record):
    """
    Expected format:
    ProductCode | Quantity | Amount

    Example:
    P101 | 3 | 450.50
    """
    record = record.strip()

    if not record:
        return None, "Empty record"

    parts = record.split("|")

    if len(parts) != 3:
        return None, "Invalid format: record must contain 3 fields"

    product_code = parts[0].strip()
    quantity_text = parts[1].strip()
    amount_text = parts[2].strip()

    # Validate product code
    if not product_code:
        return None, "Missing product code"

    if not product_code.startswith("P"):
        return None, "Product code must start with 'P'"

    if not product_code[1:].isdigit():
        return None, "Product code must contain digits after 'P'"

    # Validate quantity
    if not quantity_text.isdigit():
        return None, "Quantity must be a whole number"

    quantity = int(quantity_text)

    if quantity <= 0:
        return None, "Quantity must be greater than zero"

    # Validate amount
    try:
        amount = float(amount_text)
    except ValueError:
        return None, "Amount must be numeric"

    if amount < 0:
        return None, "Amount cannot be negative"

    return {
        "product_code": product_code,
        "quantity": quantity,
        "amount": amount
    }, None


def process_invoice(invoice_text):
    """
    Each invoice item must be on a separate line.

    Example:
    P101 | 2 | 500.00
    P205 | 4 | 1200.50
    """
    valid_records = []
    malformed_records = []

    lines = invoice_text.strip().split("\n")

    for line_number, line in enumerate(lines, start=1):
        result, error = extract_invoice_record(line)

        if error:
            malformed_records.append({
                "line_number": line_number,
                "record": line,
                "error": error
            })
        else:
            valid_records.append(result)

    return valid_records, malformed_records


def print_invoice_report(valid_records, malformed_records):
    total_amount = 0

    print("VALID INVOICE RECORDS")
    print("-" * 55)
    print(f"{'Product Code':<15}{'Quantity':<15}{'Amount'}")
    print("-" * 55)

    for item in valid_records:
        print(
            f"{item['product_code']:<15}"
            f"{item['quantity']:<15}"
            f"₹{item['amount']:.2f}"
        )
        total_amount += item["amount"]

    print("-" * 55)
    print(f"Total Invoice Amount: ₹{total_amount:.2f}")

    print("\nMALFORMED RECORDS")
    print("-" * 55)

    if malformed_records:
        for item in malformed_records:
            print(f"Line {item['line_number']}: {item['record']}")
            print(f"Reason: {item['error']}\n")
    else:
        print("No malformed records found.")


# Sample formatted invoice string
invoice_data = """
P101 | 3 | 450.50
P205 | 2 | 1200
P301 | 5 | 875.75
PABC | 2 | 500
P401 | -3 | 650
P501 | 4 | invalid_amount
P601 | 2
| 3 | 100
"""

valid_records, malformed_records = process_invoice(invoice_data)

print_invoice_report(valid_records, malformed_records)