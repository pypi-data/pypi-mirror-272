
def get_secret_key():
    secret_key = 'xD'

    return secret_key

mapping = {
    "a": "1",
    "b": "2",
    "c": "3",
    "d": "4",
    "e": "5",
    "f": "6",
    "g": "7",
    "h": "8",
    "i": "9",
    "j": "0",
    "k": "!",
    "l": "@",
    "m": "#",
    "n": "$",
    "o": "%",
    "p": "^",
    "q": "&",
    "r": "*",
    "s": "(",
    "t": ")",
    "u": "-",
    "v": "+",
    "w": "=",
    "x": "{",
    "y": "}",
    "z": "[",
    "0": "]",
    "1": ";",
    "2": ":",
    "3": ",",
    "4": ".",
    "5": "<",
    "6": ">",
    "7": "/",
    "8": "?",
    "9": "|",
    "$": "a",
    "@": "b",
    "#": "c",
    "!": "d",
    "&": "e",
    "^": "f",
    "?": "g",
    "-": "h",
    "{": "i",
    "}": "j",
    "[": "k",
    "]": "l",
    "¿": "m",
    "%": "n",
    "&": "o",
    "^": "p",
    "?": "q",
    "-": "r",
    "{": "s",
    "}": "t",
    "[": "u",
    "]": "v",
    "¿": "w",
    "€": "x",
    ":": "y",
    "V": "z",
    "I": "A",
    "H": "B",
    "O": "C",
    "T": "D",
    "P": "E",
    "Q": "F",
    "~": "G",
    "ñ": "H",
}

def xor_cipher(input_string, key):
    return ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(input_string, key * len(input_string)))

def encode(cadena):
    xor_cadena = xor_cipher(cadena, get_secret_key())

    nueva_cadena = ""
    for caracter in xor_cadena:
        if caracter in mapping:
            nueva_cadena += mapping[caracter]
        else:
            nueva_cadena += caracter

    return nueva_cadena

def decode(cadena):
    map_inv = {v: k for k, v in mapping.items()}
    xor_cadena = ""
    for caracter in cadena:
        if caracter in map_inv:
            xor_cadena += map_inv[caracter]
        else:
            xor_cadena += caracter

    decrypted_cadena = xor_cipher(xor_cadena, get_secret_key())

    return decrypted_cadena
