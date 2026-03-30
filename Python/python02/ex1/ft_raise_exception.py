def input_temperature(temp_str: str) -> int | None:
    print(f"Input data is: {temp_str}")
    temp = int(temp_str)
    if temp > 40:
        raise ValueError(f"{temp}°C is too hot for plants (max 40°C)")
    if temp < 0:
        raise ValueError(f"{temp}°C is too cold for plants (min 0°C)")

    print(f"Temperature is now {temp}°C\n")
    return temp


def test_temperature() -> None:
    print("=== Garden Temperature Checker ===\n")

    test_case = ["25", "abc", "100", "-50"]

    for case in test_case:
        try:
            input_temperature(case)
        except ValueError as e:
            print(f"Caught input_temperature error: {e}\n")

    print("All tests completed - program didn't crash!")


if __name__ == "__main__":
    test_temperature()
