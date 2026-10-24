"""Run pip with response-body reservations, including metadata and failed reads."""
from __future__ import annotations
import sys
import inspect
from resource_budget import Budget


def main() -> int:
    """Meter pip's vendored urllib3 raw HTTP-body reader, then invoke its CLI."""
    from pip._vendor.urllib3.response import HTTPResponse
    from pip._internal.cli.main import main as pip_main
    budget = Budget()
    original = HTTPResponse._fp_read
    supports_read1 = 'read1' in inspect.signature(original).parameters

    def read_original(response, amount, read1):
        return original(response, amount, read1=read1) if supports_read1 else original(response, amount)

    def guarded_read(self, amt=None, *, read1=False):
        if amt is None:
            pieces = []
            while True:
                budget.before_read(65536)
                block = read_original(self, 65536, read1)
                budget.after_read(len(block))
                if not block:
                    break
                pieces.append(block)
            return b''.join(pieces)
        budget.before_read(amt)
        block = read_original(self, amt, read1)
        budget.after_read(len(block))
        return block

    HTTPResponse._fp_read = guarded_read
    try:
        return pip_main(sys.argv[1:])
    finally:
        budget.save()


if __name__ == '__main__':
    raise SystemExit(main())
