class SecurePlant:
    def __init__(self, name: str) -> None:
        self.name = name
        self._height = 0
        self._age = 0
        print(f"Plant created: {self.name}")

    def get_height(self) -> int:
        return self._height

    def set_height(self, height: int) -> None:
        if height < 0:
            print(f"Invalid operation attempted: height {height}cm [REJECTED]")
            print("Security: Negative height rejected\n")
        else:
            self._height = height
            print(f"Height updated: {height}cm [OK]")

    def get_age(self) -> int:
        return self._age

    def set_age(self, age: int) -> None:
        if age < 0:
            print(f"Invalid operation attempted: age {age} days [REJECTED]")
            print("Security: Negative age rejected")
        else:
            self._age = age
            print(f"Age update: {age} days [OK]\n")

    def get_info(self) -> str:
        return (f"Current plant: {self.name}"
                f"({self._height}cm, {self._age} days)")


if __name__ == "__main__":
    print("=== Garden Security System ===")

    rose = SecurePlant("Rose")

    rose.set_height(25)
    rose.set_age(30)
    rose.set_height(-5)

    print(rose.get_info())
