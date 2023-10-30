import sys
import itertools

from peekable import peekable
from decimal import Decimal

def ignore_ws(code: peekable):
    while code and code.peek() in ' \n\r\t':
        next(code)

from decimal import Decimal

def convert_token(input_str: str) -> Decimal | bool | None | str:
    try:
        # return Decimal(input_str)
        try:
            return int(input_str)
        except:
            return float(input_str)
    except:
        if input_str in ['true', 'false']:
            return input_str.lower() == 'true'
        elif input_str == 'null':
            return None
        elif len(input_str) >= 2 and all(input_str[i] in "'\"" for i in (0,-1)):
            return input_str[1:-1]
        else:
            return input_str


def parse_token(code: peekable):
    # A token is always a string. Here a token is the jon code for a raw value or a key of an object
    # It will include quotes if the jon contains quotes
    # Backslashes are in the output only for quoted values, not for other values
    # Unquoted values stop at any character in ' {[]},:' unless preceded by a backslash
    # Quotes are only treated as special at the beginning or the end of the jon code

    token = ''
    escape = False
    quote = ''

    if code.peek() in "'\"":
        quote = next(code)
        token += quote

    while code:
        if escape:
            # decoding the escape is handled either
            # right after the escape char is found
            # (when str is not quoted) or at the return
            token += next(code)
            escape = False
        elif quote:
            c = next(code)
            token += c
            if c == '\\':
                escape = True
            elif c == quote:
                break
        else:
            c = code.peek()
            if c in ' \t\r\n{[]},:':
                break
            elif c == '\\':
                escape = True
                next(code)
                c = code.peek()
                if not quote and c in ' {[]},:':
                    token += next(code)
                else:
                    token += '\\'
            else:
                token += next(code)

    if quote:
        return token
    else:
        return token.encode().decode('unicode-escape')

def parse_array(code: peekable):
    if not code:
        return []
    if code.peek() == "[":
        next(code)
    ignore_ws(code)
    values = []
    while code:
        value = parse(code, in_array=True)
        values.append(value)
        ignore_ws(code)
        if code and code.peek() == ",":
            next(code)
            ignore_ws(code)
        if code and code.peek() == "]":
            next(code)
            break
    return values

def parse_obj_entry(code: peekable):
    key = convert_token(parse_token(code))
    ignore_ws(code)
    if code and code.peek() == ":":
        next(code)
    value = parse(code, in_obj=True)
    return key, value

def parse_obj(code: peekable):
    if not code:
        return {}
    if code.peek() == "{":
        next(code)
        proper_obj = True
    else:
        proper_obj = False
    obj = {}
    while code:
        ignore_ws(code)
        if code.peek() == "}":
            next(code)
            break
        key, value = parse_obj_entry(code)
        obj[key] = value
        ignore_ws(code)
        if code:
            if code.peek() == "}":
                next(code)
                break
            elif code.peek() == ",":
                next(code)
                continue
            elif not proper_obj or code.peek() in "[]{:":
                break
    return obj

def parse(code: peekable, in_array=False, in_obj=False):
    ignore_ws(code)
    if code.peek() == '{':
        return parse_obj(code)
    elif code.peek() == '[':
        return parse_array(code)
    token = parse_token(code)
    ignore_ws(code)
    if not code:
        return convert_token(token)
    if code.peek() == ":":
        code.prepend(*token)
        obj = parse_obj(code)
        ignore_ws(code)
        if code and not in_array:
            return [obj, *parse_array(code)]
        else:
            return obj
    else:
        if in_array or in_obj:
            return convert_token(token)
        else:
            return [token, *parse_array(code)]

def loads(code_str: str):
    code = peekable(code_str)
    return parse(code)

