def input_temperature(temp_str: str) -> int:
    print(f"Input data is '{temp_str}'")
    temp = int(temp_str)
    print(f"Temperature is now {temp}°C\n")
    return temp


def test_temperature() -> None:
    print("=== Garden Temperature ===\n")

    try:
        input_temperature("25")
    except ValueError as e:
        print(f"Caught input_temperature error: {e}\n")

    try:
        input_temperature("abc")
    except ValueError as e:
        print(f"Caught input_temperature error: {e}\n")

    print("All tests completed program didn't crash!")


if __name__ == "__main__":
    test_temperature()
