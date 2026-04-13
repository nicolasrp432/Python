def secure_archive(filename: str, action: str = "read", content: str = "") -> tuple[bool, str]:
    if action == "read":
        try:
            with open(filename, 'r') as file:
                data = file.read()
            return (True, data)

        except Exception as e:
            return (False, str(e))

    elif action == "write":
        try:
            with open(filename, 'w') as file:
                file.write(content)
            return (True, "Content successfully written to file")

        except Exception as e:
            return (False, str(e))

    else:
        return (False, f"Invalid action: '{action}'")


def main() -> None:
    print("=== Cyber Archives Security ===")

    print("Using 'secure_archive' to read from a nonexistent file:")
    print(secure_archive('/not/existing/file', 'read'))

    print("Using 'secure_archive' to read from an inaccessible file:")
    print(secure_archive('/etc/shadow', 'read'))

    print("Using 'secure_archive' to read from a regular file:")
    print(secure_archive('ancient_fragment.txt', 'read'))

    print("Using 'secure_archive' to write previous content to a new file:")
    print(secure_archive('new_archive.txt', 'write', 'Este es el nuevo conocimiento archivado.\n'))


if __name__ == "__main__":
    main()
