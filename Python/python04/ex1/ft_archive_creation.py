import sys
import typing


def ft_archive_creation() -> None:
    if len(sys.argv) != 2:
        print("Usage: ft_archive_creation.py <file>")
        return

    filename: str = sys.argv[1]

    print("=== Cyber Archives Recovery & Preservaion ===")
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
        return
    except PermissionError as e:
        print(f"Error opening file '{filename}': {e}")
        return
    except PermissionError as e:
        print(f"Error opening file '{filename}': {e}")
        return

    print("Transform data:")
    transformed_lines = [line + "#" for line in content.splitlines()]
    transformed_content = "\n".join(transformed_lines)
    print(transformed_content)

    new_filename = input("Enter new file name (or empty):")

    if not new_filename.strip():
        print("Not saving data.")
    else:
        print(f"Saving data to '{new_filename}'")
        try:
            new_file: typing.IO[typing.Any] = open(new_filename, 'w')
            new_file.write(transformed_content + '\n')
            new_file.close
            print(f"Data saved in file '{new_filename}'.")

        except Exception as e:
            print(f"Error saving file '{new_filename}': {e}")


if __name__ == "__main__":
    ft_archive_creation()
