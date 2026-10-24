"""Single-process conservative response-body accounting for the approved smoke."""
from __future__ import annotations
import json
import hashlib
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
STATE = ROOT / 'RESOURCE_BUDGET.json'
LIMIT = 2 * 1024**3


class Budget:
    """Reserve blocks before reads; never refund partial or failed transfers."""
    def __init__(self, state: Path = STATE) -> None:
        self.path = state
        self.data = json.loads(state.read_text(encoding='utf-8')) if state.exists() else {
            'limit_bytes': LIMIT, 'charged_bytes': 8*1024**2,
            'received_metered_bytes': 0,
            'unmetered_metadata_reserve_bytes': 8*1024**2,
            'accounting': 'Conservative response-body reservations; excludes transport headers/TLS overhead. Metadata API calls covered by a declared reserve, not exact metering.'}
        self.credit = 0
        self.save()

    def save(self) -> None:
        """Atomically persist cumulative charges before reading network bytes."""
        temporary = self.path.with_suffix('.tmp')
        temporary.write_text(json.dumps(self.data, indent=2)+'\n', encoding='utf-8')
        temporary.replace(self.path)

    def before_read(self, amount: int) -> None:
        """Fail closed if the next bounded read cannot be reserved."""
        if amount < 0:
            raise ValueError('Negative read reservation')
        if amount > self.credit:
            reserve = max(1024**2, amount-self.credit)
            if self.data['charged_bytes'] + reserve > self.data['limit_bytes']:
                raise RuntimeError('Approved cumulative transfer ceiling reached')
            self.data['charged_bytes'] += reserve
            self.credit += reserve
            self.save()

    def after_read(self, received: int) -> None:
        """Record actual bytes within already persisted conservative credit."""
        if received > self.credit:
            raise RuntimeError('Unreserved network read')
        self.credit -= received
        self.data['received_metered_bytes'] += received

    def fetch(self, url: str, destination: Path, expected_size: int,
              expected_sha256: str) -> dict:
        """Fetch one bounded artifact; retain charged partial reads on failure."""
        if destination.exists():
            digest = hashlib.sha256(destination.read_bytes()).hexdigest()
            if destination.stat().st_size == expected_size and digest == expected_sha256:
                return {'path':str(destination), 'status':'VERIFIED_EXISTING', 'sha256':digest}
            raise RuntimeError('Existing artifact differs; refusing overwrite')
        destination.parent.mkdir(parents=True, exist_ok=True)
        part = destination.with_suffix(destination.suffix+'.part')
        if part.exists():
            raise RuntimeError('Partial artifact retained; no implicit retry/reset')
        count = 0
        digest = hashlib.sha256()
        try:
            with urlopen(Request(url, headers={'User-Agent':'Kusan-bounded-smoke/1'}), timeout=120) as response, part.open('xb') as output:
                declared = response.headers.get('Content-Length')
                if declared and int(declared) != expected_size:
                    raise RuntimeError('Unexpected declared payload size')
                while True:
                    amount = min(1024**2, expected_size-count+1)
                    self.before_read(amount)
                    chunk = response.read(amount)
                    self.after_read(len(chunk))
                    if not chunk:
                        break
                    count += len(chunk)
                    if count > expected_size:
                        raise RuntimeError('Artifact exceeds frozen byte count')
                    digest.update(chunk)
                    output.write(chunk)
            if count != expected_size or digest.hexdigest() != expected_sha256:
                raise RuntimeError('Payload size/digest failed')
            part.replace(destination)
            return {'path':str(destination), 'status':'VERIFIED_DOWNLOAD', 'bytes':count, 'sha256':digest.hexdigest()}
        finally:
            self.save()

    def fetch_bounded(self, url: str, destination: Path, maximum: int) -> dict:
        """Fetch one newly generated input, retaining its digest without a guessed size."""
        if destination.exists() or destination.with_suffix('.part').exists():
            raise RuntimeError('Input/partial exists; no automatic replacement')
        part = destination.with_suffix('.part')
        received = 0
        digest = hashlib.sha256()
        try:
            with urlopen(url, timeout=240) as response, part.open('xb') as output:
                declared = response.headers.get('Content-Length')
                if declared and int(declared)>maximum:
                    raise RuntimeError('Input exceeds its transfer bound')
                while True:
                    amount = min(1024**2, maximum-received+1)
                    self.before_read(amount)
                    block = response.read(amount)
                    self.after_read(len(block))
                    if not block:
                        break
                    received += len(block)
                    if received>maximum:
                        raise RuntimeError('Input exceeds its transfer bound')
                    digest.update(block)
                    output.write(block)
            part.replace(destination)
            return {'bytes':received,'sha256':digest.hexdigest(),'maximum_bytes':maximum}
        finally:
            self.save()
