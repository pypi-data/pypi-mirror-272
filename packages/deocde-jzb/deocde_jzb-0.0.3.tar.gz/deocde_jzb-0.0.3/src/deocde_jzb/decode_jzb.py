import base64
import zlib


def decode_jzb(data: bytes) -> bytes:
    mod = len(data) % 4
    if mod == 2:
        data += b"=="
    elif mod == 3:
        data += b"="
    data = base64.urlsafe_b64decode(data)
    data = zlib.decompress(data)
    return data


def test():
    data = b'eJxSqo5RykvMTY1RslKIUfJKzEuNUapVAgQAAP__TdEGrg'
    decoded_data = b'"{\\"name\\": \\"Jane\\"}"'
    assert (decode_jzb(data) == decoded_data)


if __name__ == "__main__":
    test()
