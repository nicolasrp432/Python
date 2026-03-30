import math


def get_player_pos() -> tuple[float, float, float]:
    while True:
        user_input = input("Enter new coordiate as floats in format 'x,y,z': ")
        parts = user_input.split(',')

        if len(parts) != 3:
            print("Invalid syntax")
            continue

        try:
            x = float(parts[0].strip())
            y = float(parts[1].strip())
            z = float(parts[2].strip())
            return(x, y, z)

        except ValueError as e:
            for part in parts:
                try:
                    float(part.strip())
                except ValueError as err:
                    print(f"Error on parameter '{part.strip()}': {err}")
                    break


def coordiate_system() -> None:
    print("=== Game Coordinate System ===")

    print("Get a first set of coordinates")
    coord1 = get_player_pos()

    print(f"Got a first tuple: {coord1}")
    print(f"It includes: X={coord1[0]}, Y={coord1[1]}, Z={coord1[2]}")

    dist_center = math.sqrt(coord1[0]**2 + coord1[1]**2 + coord1[2]**2)
    print(f"Distance to center: {round(dist_center, 4)}")

    print("Get a second set of coordinates")
    coord2 = get_player_pos()

    dx = coord2[0] - coord1[0]
    dy = coord2[1] - coord1[1]
    dz = coord2[2] - coord1[2]
    dist_between = math.sqrt(dx**2 + dy**2 + dz**2)

    print(f"Distance between the 2 sets of coordinates: {round(dist_between, 4)}")


if __name__ == "__main__":
    coordiate_system()
