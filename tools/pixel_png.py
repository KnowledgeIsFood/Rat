"""Minimal 8-bit RGBA PNG read/write using only the standard library."""

from __future__ import annotations

import struct
import zlib
from pathlib import Path

_PNG_SIG = b"\x89PNG\r\n\x1a\n"


def write_rgba_png(path: Path, width: int, height: int, pixels: list[list[tuple[int, int, int, int]]]) -> None:
    if len(pixels) != height or any(len(row) != width for row in pixels):
        raise ValueError("pixels must be height rows of width RGBA tuples")
    raw = bytearray()
    for row in pixels:
        raw.append(0)  # filter 0: None
        for r, g, b, a in row:
            raw.extend((r, g, b, a))
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(
        _PNG_SIG
        + _chunk(b"IHDR", ihdr)
        + _chunk(b"IDAT", zlib.compress(bytes(raw), 9))
        + _chunk(b"IEND", b"")
    )


def read_rgba_png(path: Path) -> tuple[int, int, list[list[tuple[int, int, int, int]]]]:
    data = path.read_bytes()
    if not data.startswith(_PNG_SIG):
        raise ValueError(f"{path} is not a PNG")
    pos = len(_PNG_SIG)
    width = height = None
    idat = bytearray()
    while pos < len(data):
        length = struct.unpack(">I", data[pos : pos + 4])[0]
        tag = data[pos + 4 : pos + 8]
        chunk = data[pos + 8 : pos + 8 + length]
        crc = struct.unpack(">I", data[pos + 8 + length : pos + 12 + length])[0]
        if zlib.crc32(tag + chunk) & 0xFFFFFFFF != crc:
            raise ValueError(f"bad CRC in {tag!r}")
        pos += 12 + length
        if tag == b"IHDR":
            width, height, bit_depth, color_type, compression, filt, interlace = struct.unpack(
                ">IIBBBBB", chunk
            )
            if (bit_depth, color_type, compression, filt, interlace) != (8, 6, 0, 0, 0):
                raise ValueError("only 8-bit RGBA non-interlaced PNG is supported")
        elif tag == b"IDAT":
            idat.extend(chunk)
        elif tag == b"IEND":
            break
    if width is None or height is None:
        raise ValueError("missing IHDR")
    raw = zlib.decompress(bytes(idat))
    stride = width * 4
    pixels: list[list[tuple[int, int, int, int]]] = []
    src = 0
    prev = bytes(stride)
    for _ in range(height):
        filter_type = raw[src]
        scan = bytearray(raw[src + 1 : src + 1 + stride])
        src += 1 + stride
        _paeth_unfilter(filter_type, scan, prev)
        prev = bytes(scan)
        row = []
        for x in range(0, stride, 4):
            row.append((scan[x], scan[x + 1], scan[x + 2], scan[x + 3]))
        pixels.append(row)
    return width, height, pixels


def nn_scale(
    pixels: list[list[tuple[int, int, int, int]]], scale: int
) -> list[list[tuple[int, int, int, int]]]:
    out: list[list[tuple[int, int, int, int]]] = []
    for row in pixels:
        scaled_row = [px for px in row for _ in range(scale)]
        for _ in range(scale):
            out.append(list(scaled_row))
    return out


def _chunk(tag: bytes, data: bytes) -> bytes:
    return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)


def _paeth(a: int, b: int, c: int) -> int:
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    if pb <= pc:
        return b
    return c


def _paeth_unfilter(filter_type: int, scan: bytearray, prev: bytes) -> None:
    stride = len(scan)
    bpp = 4
    if filter_type == 0:
        return
    if filter_type == 1:
        for i in range(stride):
            left = scan[i - bpp] if i >= bpp else 0
            scan[i] = (scan[i] + left) & 255
        return
    if filter_type == 2:
        for i in range(stride):
            scan[i] = (scan[i] + prev[i]) & 255
        return
    if filter_type == 3:
        for i in range(stride):
            left = scan[i - bpp] if i >= bpp else 0
            scan[i] = (scan[i] + ((left + prev[i]) // 2)) & 255
        return
    if filter_type == 4:
        for i in range(stride):
            left = scan[i - bpp] if i >= bpp else 0
            up_left = prev[i - bpp] if i >= bpp else 0
            scan[i] = (scan[i] + _paeth(left, prev[i], up_left)) & 255
        return
    raise ValueError(f"unsupported PNG filter {filter_type}")
