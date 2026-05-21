def get_total(costs: dict, items: list, tax: float) -> float:
    subtotal = sum(costs[item] for item in items if item in costs)
    total = subtotal + subtotal * tax
    return round(total, 2)


if __name__ == "__main__":
    costs = {'socks': 5, 'shoes': 60, 'sweater': 30}
    print(get_total(costs, ['socks', 'shoes'], 0.09))   # 70.85
    print(get_total(costs, ['sweater', 'ghost'], 0.1))  # 33.0
