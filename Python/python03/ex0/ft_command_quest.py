import sys


def command_quest() -> None:
    print("=== Command Quest ===")

    program_name = sys.argv[0]
    total_args = len(sys.argv)
    args_received = total_args - 1

    print(f"Program name: {program_name}")

    if args_received == 0:
        print("No arguments provided!")
    else:
        print(f"Arguments received: {args_received}")

        for index, arg in enumerate(sys.argv[1:], start=1):
            print(f"Argument {index}: {arg}")

    print(f"Total arguments: {total_args}")


if __name__ == "__main__":
    command_quest()
