import sys


def inventory_master() -> None:
    print("=== Inventory System Analysis ===")

    inventory: dict[str, int] = {}

    for arg in sys.argv[1:]:
        parts = arg.split(':')

        if len(parts) != 2:
            print(f"Error - invalid parameter '{arg}'")
            continue

        item_name = parts[0]
        qty_str = parts[1]

        if item_name in inventory:
            print(f"Redundant item '{item_name}' - discarding")
            continue

        try:
            qty = int(qty_str)
            inventory[item_name] = qty
        except ValueError as e:
            print(f"Quantity error for '{item_name}': {e}")

    print(f"\nGot inventory: {inventory}")

    item_list = list(inventory.keys())
    print(f"Item list: {item_list}")

    total_qty = sum(inventory.values())
    print(f"Total quantity of the {len(inventory)} items: {total_qty}")

    if total_qty > 0:
        most_item = ""
        most_qty = -1
        least_item = ""
        least_qty = float('inf')

        for item in inventory.keys():
            qty = inventory[item]

            percentage = (qty / total_qty) * 100
            print(f"Item {item} represents {round(percentage, 1)}%")

            if qty > most_qty:
                most_qty = qty
                most_item = item

            if qty < least_qty:
                least_qty = qty
                least_item = item

        print(f"Item most abundant: {most_item} with quantity {most_qty}")
        print(f"Item least abundant: {least_item} with quantity {least_qty}")

        inventory.update({'magic_item': 1})
        print(f"Updated inventory: {inventory}")


if __name__ == "__main__":
    inventory_master()
