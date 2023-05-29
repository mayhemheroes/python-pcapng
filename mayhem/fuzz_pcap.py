#!/usr/bin/env python3
import struct
import atheris
import sys
import fuzz_helpers

with atheris.instrument_imports():
    from pcapng import FileScanner

from pcapng.exceptions import TruncatedFile, BadMagic, CorruptedFile

ctr = 0
def TestOneInput(data):
    fdp = fuzz_helpers.EnhancedFuzzedDataProvider(data)
    global ctr
    ctr += 1
    try:
        with fdp.ConsumeMemoryFile(all_data=True) as f:
            scanner = FileScanner(f)
            for block in scanner:
                pass
    except (ValueError, TruncatedFile, BadMagic, CorruptedFile, OSError):
        return -1
    except struct.error:
        if ctr > 10000:
            raise
        return -1
def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
