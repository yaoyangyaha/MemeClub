import base64


def encode_text(value: str) -> str:
    return base64.b64encode(value.encode("utf-8")).decode("utf-8")


def decode_text(value: str | None) -> str:
    if not value:
        return ""
    return base64.b64decode(value.encode("utf-8")).decode("utf-8")
