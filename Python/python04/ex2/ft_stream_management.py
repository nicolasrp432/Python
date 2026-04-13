import sys
import typing


def stream_management() -> None:
    if len(sys.argv) != 2:
        print("Usage: ft_stream_management.py <file>")
        return

    filename: str = sys.argv[1]

    print("=== Cyber Archives Recovery & Preservation ===")
    print(f"Accessing file '{filename}'")

    try:
        file: typing.IO[typing.Any] = open(filename, 'r')
        content: str = file.read()
        print(content, end="")
        if content and not content.endswith('\n'):
            print()
        file.close()
        print(f"File '{filename}' closed.")

    except Exception as e:
        print(f"[STDERR] Error opening file")
            (f"'{filename}': {e}", file=sys.stderr)"
        return

    print("Transform data:")
    transformed_lines = [line + "#" for line in content.splitlines()]
    transformed_content = "\n".join(transformed_lines)
    print(transformed_content)

    print("Enter new file name (or empty): ", end="", flush=True)

    new_filename = sys.stdin.readline().strip()

    if not new_filename:
        print("Not saving data.")
    else:
        print(f"Saving data to '{new_filename}'")
        try:
            new_file: typing.IO[typing.Any] = open(new_filename, 'w')
            new_file.write(transformed_content + '\n')
            new_file.close()

        except Exception as e:
            print(f"[STDERR] Error opening file '{new_filename}': {e}", file=sys.stderr)
            print("Data not saved.")

if __name__ == "__main__":
    stream_management()
