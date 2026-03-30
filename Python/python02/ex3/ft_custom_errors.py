class GardenError(Exception):
    def __init__(self, message: str = "Unknow garden error") -> None:
        super().__init__(message)


class PlantError(GardenError):
    def __init__(self, message: str = "Unknow garden error") -> None:
        super().__init__(message)


class WaterError(GardenError):
    def __init__(self, message: str = "Unknow garden error") -> None:
        super().__init__(message)


def simulate_plant_issue() -> None:
    raise PlantError("The tomato plant is wilting!")


def simulate_water_issue() -> None:
    raise WaterError("Not enough water in the tank!")


def test_custom_errors() -> None:
    print("=== Custom Garden Errors Demo ===\n")

    print("Testing PlantError...")
    try:
        simulate_plant_issue()
    except PlantError as my_error:
        print(f"Caught PlantError: {my_error}\n")

    print("Testing WaterError...")
    try:
        simulate_water_issue()
    except WaterError as my_error:
        print(f"Caught WaterError: {my_error}\n")

    print("Testing catching all garden errors...")
    try:
        simulate_plant_issue()
    except GardenError as my_error:
        print(f"Caught a garden error: {my_error}")

    try:
        simulate_water_issue()
    except GardenError as my_error:
        print(f"Caught a garden error: {my_error}\n")

    print("All custom error types work correctly!")


if __name__ == "__main__":
    test_custom_errors()
