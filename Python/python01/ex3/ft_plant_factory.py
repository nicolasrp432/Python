class Plant:
    def __init__(self, name: str, height: int, age: int) -> None:
        self.name = name
        self.height = height
        self.age = age


if __name__ == "__main__":
    print("=== Plant Factory Output ===")

    plants = [
        Plant("Rose", 25, 30),
        Plant("Oak", 200, 365),
        Plant("Cactus", 5, 90),
        Plant("Sunflowe", 80, 45),
        Plant("Fern", 15, 120)
    ]

    for plant in plants:
        print(f"Created: {plant.name} ({plant.height}cm, {plant.age} days)")

    print(f"\nTotal plants created: {len(plants)}")
