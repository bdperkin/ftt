"""
Magic tests for file type detection based on file signatures and content.

Copyright (c) 2025 Brandon Perkins

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import struct
from pathlib import Path
from typing import List, Optional, Tuple

from ..types import FileType, FileTypeCategory, TestResult

# Magic number signatures: (offset, signature_bytes, description, category, mime_type)
MAGIC_SIGNATURES: List[Tuple[int, bytes, str, FileTypeCategory, Optional[str]]] = [
    # Executables
    (
        0,
        b"\x7fELF",
        "ELF executable",
        FileTypeCategory.EXECUTABLE,
        "application/x-executable",
    ),
    (
        0,
        b"MZ",
        "MS-DOS executable",
        FileTypeCategory.EXECUTABLE,
        "application/x-msdownload",
    ),
    (
        0,
        b"\xfe\xed\xfa\xce",
        "Mach-O executable (32-bit)",
        FileTypeCategory.EXECUTABLE,
        "application/x-mach-binary",
    ),
    (
        0,
        b"\xfe\xed\xfa\xcf",
        "Mach-O executable (64-bit)",
        FileTypeCategory.EXECUTABLE,
        "application/x-mach-binary",
    ),
    (
        0,
        b"\xcf\xfa\xed\xfe",
        "Mach-O executable (32-bit, reverse)",
        FileTypeCategory.EXECUTABLE,
        "application/x-mach-binary",
    ),
    (
        0,
        b"\xce\xfa\xed\xfe",
        "Mach-O executable (64-bit, reverse)",
        FileTypeCategory.EXECUTABLE,
        "application/x-mach-binary",
    ),
    # Archives and compressed files (binary data)
    (0, b"PK\x03\x04", "ZIP archive data", FileTypeCategory.DATA, "application/zip"),
    (
        0,
        b"PK\x05\x06",
        "empty ZIP archive data",
        FileTypeCategory.DATA,
        "application/zip",
    ),
    (0, b"PK\x07\x08", "ZIP archive data", FileTypeCategory.DATA, "application/zip"),
    (0, b"\x1f\x8b", "gzip compressed data", FileTypeCategory.DATA, "application/gzip"),
    (0, b"BZh", "bzip2 compressed data", FileTypeCategory.DATA, "application/x-bzip2"),
    (
        0,
        b"\xfd7zXZ\x00",
        "XZ compressed data",
        FileTypeCategory.DATA,
        "application/x-xz",
    ),
    (
        0,
        b"7z\xbc\xaf\x27\x1c",
        "7-zip archive data",
        FileTypeCategory.DATA,
        "application/x-7z-compressed",
    ),
    (
        0,
        b"Rar!\x1a\x07\x00",
        "RAR archive data",
        FileTypeCategory.DATA,
        "application/x-rar-compressed",
    ),
    (
        0,
        b"Rar!\x1a\x07\x01\x00",
        "RAR archive data",
        FileTypeCategory.DATA,
        "application/x-rar-compressed",
    ),
    # Tar archives (known to contain binary data)
    (
        257,
        b"ustar\x00",
        "POSIX tar archive",
        FileTypeCategory.DATA,
        "application/x-tar",
    ),
    (
        257,
        b"ustar  \x00",
        "GNU tar archive",
        FileTypeCategory.DATA,
        "application/x-tar",
    ),
    # Images (binary data)
    (0, b"\xff\xd8\xff", "JPEG image data", FileTypeCategory.DATA, "image/jpeg"),
    (0, b"\x89PNG\r\n\x1a\n", "PNG image data", FileTypeCategory.DATA, "image/png"),
    (0, b"GIF87a", "GIF image data", FileTypeCategory.DATA, "image/gif"),
    (0, b"GIF89a", "GIF image data", FileTypeCategory.DATA, "image/gif"),
    (0, b"BM", "BMP image data", FileTypeCategory.DATA, "image/bmp"),
    (0, b"RIFF", "RIFF data", FileTypeCategory.DATA, None),  # Could be WAV, AVI, etc.
    (8, b"WEBP", "WebP image data", FileTypeCategory.DATA, "image/webp"),
    # Audio/Video (binary data)
    (0, b"ID3", "MP3 audio data", FileTypeCategory.DATA, "audio/mpeg"),
    (0, b"\xff\xfb", "MP3 audio data", FileTypeCategory.DATA, "audio/mpeg"),
    (0, b"\xff\xf3", "MP3 audio data", FileTypeCategory.DATA, "audio/mpeg"),
    (0, b"\xff\xf2", "MP3 audio data", FileTypeCategory.DATA, "audio/mpeg"),
    (0, b"OggS", "Ogg data", FileTypeCategory.DATA, "application/ogg"),
    (4, b"ftyp", "MP4 video data", FileTypeCategory.DATA, "video/mp4"),
    # Documents (binary data)
    (0, b"%PDF", "PDF document data", FileTypeCategory.DATA, "application/pdf"),
    (
        0,
        b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1",
        "Microsoft Office document data",
        FileTypeCategory.DATA,
        "application/msword",
    ),
    (
        0,
        b"PK\x03\x04\x14\x00\x06\x00",
        "Microsoft Office Open XML document data",
        FileTypeCategory.DATA,
        "application/vnd.openxmlformats",
    ),
    # Core files (known to contain binary data)
    (
        0,
        b"\x7fELF",
        "ELF core file data",
        FileTypeCategory.DATA,
        "application/x-coredump",
    ),  # Will be refined by ELF parser
    # Other binary formats
    (
        0,
        b"\x00\x00\x01\x00",
        "Windows icon image data",
        FileTypeCategory.DATA,
        "image/x-icon",
    ),
    (
        0,
        b"\x00\x00\x02\x00",
        "Windows cursor image data",
        FileTypeCategory.DATA,
        "image/x-icon",
    ),
    (
        0,
        b"\x42\x5a\x68",
        "bzip2 compressed data",
        FileTypeCategory.DATA,
        "application/x-bzip2",
    ),
]

# Text file indicators
TEXT_INDICATORS = [
    b"#!/bin/sh",
    b"#!/bin/bash",
    b"#!/usr/bin/env",
    b"<?xml",
    b"<!DOCTYPE",
    b"<html",
    b"<HTML",
]


def test_magic(filepath: Path) -> TestResult:
    """
    Perform magic-based tests on a file by examining file signatures.

    Args:
        filepath: Path to the file to test

    Returns:
        TestResult indicating success or failure
    """
    try:
        # Read the first 1024 bytes to check for magic signatures
        with open(filepath, "rb") as f:
            header = f.read(1024)

        if not header:
            # Empty file was already handled by filesystem tests
            return TestResult(success=False)

        # Check for magic signatures
        for offset, signature, description, category, mime_type in MAGIC_SIGNATURES:
            if len(header) > offset + len(signature):
                if header[offset : offset + len(signature)] == signature:
                    # Special handling for ELF files to detect core dumps
                    if signature == b"\x7fELF" and len(header) >= 16:
                        elf_type = struct.unpack("<H", header[16:18])[0]
                        if elf_type == 4:  # ET_CORE
                            file_type = FileType(
                                category=FileTypeCategory.DATA,
                                description="ELF core file data",
                                mime_type="application/x-coredump",
                            )
                        else:
                            file_type = FileType(
                                category=category,
                                description=description,
                                mime_type=mime_type,
                            )
                    else:
                        file_type = FileType(
                            category=category,
                            description=description,
                            mime_type=mime_type,
                        )
                    return TestResult.success_result(file_type)

        # Check for text file indicators (shebangs, XML declarations, etc.)
        for indicator in TEXT_INDICATORS:
            if header.startswith(indicator) or header.startswith(indicator.lower()):
                if indicator.startswith(b"#!"):
                    # Script file
                    script_type = _detect_script_type(header)
                    file_type = FileType(
                        category=FileTypeCategory.TEXT,
                        description=f"{script_type} script text",
                        mime_type="text/plain",
                    )
                else:
                    # Markup file
                    markup_type = _detect_markup_type(header)
                    file_type = FileType(
                        category=FileTypeCategory.TEXT,
                        description=f"{markup_type} text",
                        mime_type="text/plain",
                    )
                return TestResult.success_result(file_type)

        # Check if file appears to be binary or text by examining content
        if _is_binary_content(header):
            file_type = FileType(category=FileTypeCategory.DATA, description="data")
            return TestResult.success_result(file_type)

        # If we get here, magic tests didn't conclusively identify the file
        return TestResult(success=False)

    except PermissionError:
        return TestResult.failure_result(f"Permission denied: {filepath}")
    except OSError as e:
        return TestResult.failure_result(f"OS error: {e}")
    except Exception as e:
        return TestResult.failure_result(f"Unexpected error: {e}")


def _detect_script_type(header: bytes) -> str:
    """Detect the type of script from shebang line."""
    header_str = header.decode("utf-8", errors="ignore")
    first_line = header_str.split("\n")[0].lower()

    if "python" in first_line:
        return "Python"
    elif "bash" in first_line:
        return "Bash"
    elif "sh" in first_line:
        return "shell"
    elif "perl" in first_line:
        return "Perl"
    elif "ruby" in first_line:
        return "Ruby"
    elif "node" in first_line or "javascript" in first_line:
        return "Node.js"
    else:
        return "script"


def _detect_markup_type(header: bytes) -> str:
    """Detect the type of markup from file content."""
    header_str = header.decode("utf-8", errors="ignore").lower()

    if "<?xml" in header_str:
        return "XML"
    elif "<!doctype html" in header_str or "<html" in header_str:
        return "HTML"
    else:
        return "markup"


def _is_binary_content(data: bytes) -> bool:
    """
    Determine if the given data appears to be binary.

    Uses heuristics similar to the Unix file command.
    """
    if not data:
        return False

    # Check for null bytes (strong indicator of binary data)
    if b"\x00" in data:
        return True

    # Count non-printable characters
    printable_chars = 0
    control_chars = 0

    for byte in data:
        if 32 <= byte <= 126:  # Printable ASCII
            printable_chars += 1
        elif byte in (9, 10, 13):  # Tab, LF, CR
            printable_chars += 1
        else:
            control_chars += 1

    total_chars = len(data)
    if total_chars == 0:
        return False

    # If more than 30% of characters are non-printable, consider it binary
    non_printable_ratio = control_chars / total_chars
    return non_printable_ratio > 0.30
