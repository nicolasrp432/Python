import sys
import typing


def recover_ancient_text() -> None:
    if len(sys.argv) != 2:
        print("Usage: ft_ancient_text.py <file>")
        return

    filename: str = sys.argv[1]

    print("=== Cyber Archives Recovery ===")
    print(f"Accessing file '{filename}'")

    try:
        file: typing.IO[typing.Any] = open(filename, 'r')
        content: str = file.read()
        print(content, end="")
        if content and not content.endswith('\n'):
            print()

        file.close()
        print(f"File '{filename}' closed.")

    except FileNotFoundError as e:
        print(f"Error opening file '{filename}': {e}")

    except PermissionError as e:
        print(f"Error opening file '{filename}': {e}")

    except Exception as e:
        print(f"Error opening file '{filename}': {e}")


if __name__ == "__main__":
    recover_ancient_text()
