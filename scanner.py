
import re

keywords = {
    "analysis", "end", "load", "from", "with",
    "let", "keep", "where", "sort", "by",
    "asc", "desc", "show", "plot", "bar",
    "line", "if", "then", "otherwise", "done",
    "number", "text"
}


def is_identifier(word):
    pattern = r"[A-Za-z][A-Za-z0-9_]*"
    if len(word) > 16:
        return False
    return re.fullmatch(pattern, word) is not None


def normalize_identifier(word):
    return word.lower()


def recognize_word(word):
    word = normalize_identifier(word)

    if not is_identifier(word):
        return "INVALID"

    if word in keywords:
        return "KEYWORD"

    return "IDENTIFIER"


def is_number(value):
    pattern = r"[0-9]{1,10}(\.[0-9]+)?"
    return re.fullmatch(pattern, value) is not None


def is_string(value):
    pattern = r'"[^"\n]*"'
    return re.fullmatch(pattern, value) is not None


def is_operator(value):
    operators = {
        "==", "!=", "<=", ">=",
        "=", "+", "-", "*", "/",
        "<", ">"
    }
    return value in operators


def is_delimiter(value):
    delimiters = {"(", ")", ",", "."}
    return value in delimiters


def remove_comment(line):
    in_string = False

    for i in range(len(line)):
        if line[i] == '"':
            in_string = not in_string

        if line[i] == "#" and not in_string:
            return line[:i]

    return line


def scan(code):
    tokens = []
    errors = []
    lines = code.split("\n")

    for line_number, line in enumerate(lines, start=1):
        line = remove_comment(line)
        i = 0

        while i < len(line):

            if line[i].isspace():
                i += 1
                continue

            # Identifiers and keywords
            if line[i].isalpha():
                word = ""

                while i < len(line) and (line[i].isalnum() or line[i] == "_"):
                    word += line[i]
                    i += 1

                if len(word) > 16:
                    errors.append((line_number, "Identifier too long", word))
                else:
                    token_type = recognize_word(word)
                    if token_type == "INVALID":
                        errors.append((line_number, "Unknown symbol", word))
                    else:
                        tokens.append((token_type, line_number, word.lower()))

            # Numbers
            elif line[i].isdigit():
                number = ""

                while i < len(line):
                    if line[i].isalnum() or line[i] == "_":
                        number += line[i]
                        i += 1

                    elif line[i] == ".":
                        if i + 1 < len(line) and line[i + 1].isdigit():
                            number += line[i]
                            i += 1
                        elif "." in number:
                            number += line[i]
                            i += 1
                        else:
                            break

                    else:
                        break

                if is_number(number):
                    tokens.append(("NUMBER", line_number, number))
                else:
                    errors.append((line_number, "Malformed number", number))

            # Text
            elif line[i] == '"':
                value = '"'
                i += 1

                while i < len(line) and line[i] != '"':
                    value += line[i]
                    i += 1

                if i < len(line):
                    value += '"'
                    i += 1

                    if is_string(value):
                        tokens.append(("TEXT", line_number, value))
                else:
                    errors.append((line_number, "Unclosed string", value))

            # Operators (longest match first)
            elif i + 1 < len(line) and is_operator(line[i:i+2]):
                tokens.append(("OPERATOR", line_number, line[i:i+2]))
                i += 2

            elif is_operator(line[i]):
                tokens.append(("OPERATOR", line_number, line[i]))
                i += 1

            # Delimiters
            elif is_delimiter(line[i]):
                tokens.append(("DELIMITER", line_number, line[i]))
                i += 1

            # Unknown symbols
            else:
                errors.append((line_number, "Unknown symbol", line[i]))
                i += 1

    return tokens, errors
