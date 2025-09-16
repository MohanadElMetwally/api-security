def to_snakecase(name: str) -> str:
    """Convert a string from camelCase or PascalCase to snake_case without regex."""
    if not name:
        return name

    result = [name[0].lower()]

    for i in range(1, len(name)):
        char = name[i]
        prev_char = name[i - 1]

        if char.islower():
            result.append(char)
            continue

        if prev_char.islower() or (
            prev_char.isupper() and i + 1 < len(name) and name[i + 1].islower()
        ):
            result.append("_")

        result.append(char.lower())

    return "".join(result)
