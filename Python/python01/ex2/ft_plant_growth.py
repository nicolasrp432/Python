class Plant:
    def __init__(self, name: str, height: int, age: int) -> None:
        self.name = name
        self.height = height
        self.age = age

    def grow(self, amount: int) -> None:
        self.height += amount

    def age_plant(self, days: int) -> None:
        self.age += days

    def get_info(self) -> str:
        return f"{self.name}: {self.height}cm, {self.age} days old"


if __name__ == "__main__":
    rose = Plant("Rose", 25, 30)

    print("=== Day 1 ===")
    print(rose.get_info())

    for _ in range(6):
        rose.grow(1)
        rose.age_plant(1)

    print("=== Day 7 ===")
    print(rose.get_info())
    print("Growth this week: +6cm")
