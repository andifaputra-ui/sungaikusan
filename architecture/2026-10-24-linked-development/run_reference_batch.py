"""One bounded reference acquisition worker; no automatic retries or inference."""
from pathlib import Path
import subprocess
import json
from datetime import datetime,timezone

ROOT=Path(__file__).resolve().parent


def main() -> None:
    """Supervise a maximum60-minute serial batch and retain timeout/failure."""
    with (ROOT/'reference_batch.stdout.log').open('w',encoding='utf-8') as out, (ROOT/'reference_batch.stderr.log').open('w',encoding='utf-8') as err:
        try:
            subprocess.run(['E:/Bendungan_Kusan/Miniforge/envs/kusan-c1/python.exe','-X','utf8',
                str(ROOT/'acquire_frozen_references.py')],stdout=out,stderr=err,timeout=3600,check=True)
        except (subprocess.TimeoutExpired,subprocess.CalledProcessError) as error:
            (ROOT/'REFERENCE_BATCH_STOP.json').write_text(json.dumps({'phase':'BOUNDED_REFERENCE_BATCH_STOPPED',
                'error_type':type(error).__name__,'utc':datetime.now(timezone.utc).isoformat(),
                'partial_receipts_and_budget_preserved':True,'no_automatic_retry':True},indent=2)+'\n',encoding='utf-8')
            raise


if __name__=='__main__':
    main()
