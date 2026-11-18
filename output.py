
def count_tokens(tokens):
    """Total number of tokens."""
    return len(tokens)


def format_token(token):
    """Format a token as <TYPE, line, lexeme>."""
    ttype, line, lexeme = token
    return f"<{ttype}, {line}, {lexeme}>"


def build_symbol_table(tokens):
    """Each identifier with the line where it first appears."""
    table = {}

    for ttype, line, lexeme in tokens:
        if ttype == "IDENTIFIER" and lexeme not in table:
            table[lexeme] = line

    return table
