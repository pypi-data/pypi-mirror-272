import base64

from typing import AnyStr, Union


def base64_decode(input: str, encoding: str = "utf-8") -> str:
    """
    Decode a base64-encoded string into a regular string.

    Args:
        input (str): The base64-encoded string to decode.
        encoding (str): The encoding to use when decoding the bytes.

    Returns:
        str: The decoded string.
    """
    decoded_bytes: bytes = base64.b64decode(input)
    return decoded_bytes.decode(encoding)
