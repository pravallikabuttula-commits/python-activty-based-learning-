from dataclasses import dataclass


@dataclass
class Product:
    name: str
    price: float
    quantity: int
    priority: int
    # Lower priority number = more important product


def calculate_discount(subtotal):
    """
    Discount rules:
    ₹5,000 or more  -> 15% discount
    ₹2,000 or more  -> 10% discount
    ₹1,000 or more  -> 5% discount
    Below ₹1,000    -> no discount
    """
    if subtotal >= 5000:
        return 0.15
    elif subtotal >= 2000:
        return 0.10
    elif subtotal >= 1000:
        return 0.05
    return 0


def calculate_cart(products):
    subtotal = sum(product.price * product.quantity for product in products)
    discount_rate = calculate_discount(subtotal)
    discount_amount = subtotal * discount_rate
    total = subtotal - discount_amount

    return subtotal, discount_rate, discount_amount, total


def reduce_cart_to_budget(products, budget):
    """
    Reduces low-priority products first until the basket
    total becomes less than or equal to the fixed budget.
    """
    # Create a copy so original shopping basket is not changed
    updated_products = [
        Product(p.name, p.price, p.quantity, p.priority)
        for p in products
    ]

    removed_items = []

    # Highest priority number is removed first
    products_to_reduce = sorted(
        updated_products,
        key=lambda product: product.priority,
        reverse=True
    )

    _, _, _, total = calculate_cart(updated_products)

    for product in products_to_reduce:
        while product.quantity > 0 and total > budget:
            product.quantity -= 1
            removed_items.append(product.name)

            # Recalculate because discount may change
            _, _, _, total = calculate_cart(updated_products)

        if total <= budget:
            break

    return updated_products, removed_items


def print_bill(products, budget):
    subtotal, discount_rate, discount_amount, total = calculate_cart(products)

    print("\nSHOPPING BASKET")
    print("-" * 55)
    print(f"{'Product':<18}{'Price':<12}{'Quantity':<10}{'Amount'}")
    print("-" * 55)

    for product in products:
        amount = product.price * product.quantity
        print(
            f"{product.name:<18}"
            f"₹{product.price:<11.2f}"
            f"{product.quantity:<10}"
            f"₹{amount:.2f}"
        )

    print("-" * 55)
    print(f"Subtotal:          ₹{subtotal:.2f}")
    print(f"Discount:          {discount_rate * 100:.0f}%")
    print(f"Discount Amount:   ₹{discount_amount:.2f}")
    print(f"Final Total:       ₹{total:.2f}")
    print(f"Budget:            ₹{budget:.2f}")


# Product(name, price, quantity, priority)
shopping_basket = [
    Product("Rice Bag", 700, 2, 1),       # Essential
    Product("Cooking Oil", 250, 3, 2),
    Product("Snacks", 150, 5, 4),         # Lowest priority
    Product("Soft Drinks", 80, 6, 5),     # Removed first
    Product("Shampoo", 220, 2, 3)
]

budget = 2500

print("ORIGINAL CART")
print_bill(shopping_basket, budget)

updated_basket, removed_items = reduce_cart_to_budget(
    shopping_basket,
    budget
)

print("\nUPDATED CART AFTER BUDGET CHECK")
print_bill(updated_basket, budget)

if removed_items:
    print("\nPurchases Reduced:")
    for item in set(removed_items):
        print(f"{item}: {removed_items.count(item)} unit(s) removed")
else:
    print("\nNo purchases need to be reduced.")