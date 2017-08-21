def tokenize(expr):
    """
    Parse a string expression into a set of tokens that can be used as a path
    into a Python datastructure.
    """
    tokens = []
    escape = False
    cur_token = ''

    for c in expr:
        if escape == True:
            cur_token += c
            escape = False
        else:
            if c == '\\':
                # Next char will be escaped
                escape = True
                continue
            elif c == '[':
                # Next token is of type index (list)
                if len(cur_token) > 0:
                    tokens.append(cur_token)
                    cur_token = ''
            elif c == ']':
                # End of index token. Next token defaults to a key (dict)
                if len(cur_token) > 0:
                    tokens.append(int(cur_token))
                    cur_token = ''
            elif c == '.':
                # End of key token. Next token defaults to a key (dict)
                if len(cur_token) > 0:
                    tokens.append(cur_token)
                    cur_token = ''
            else:
                # Append char to token name
                cur_token += c
    if len(cur_token) > 0:
        tokens.append(cur_token)

    return tokens
