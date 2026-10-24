"""Durable bounded controller; no automatic retry, reference use or scaling."""
from pathlib import Path
from datetime import datetime,timezone
import json
import os
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parent
BASE=Path('E:/Bendungan_Kusan/Miniforge/envs/kusan-c1/python.exe')
MODEL=Path('E:/Bendungan_Kusan/Model_Runtime/s1_smoke_cpu_20261024/venv/Scripts/python.exe')


def status(phase: str,**details) -> None:
    """Persist phase without polling machine resources or changing scientific inputs."""
    (ROOT/'STATUS.json').write_text(json.dumps({'phase':phase,'utc':datetime.now(timezone.utc).isoformat(),**details},indent=2)+'\n',encoding='utf-8')


def run(python: Path,script: str,timeout: int) -> None:
    """One bounded subprocess with retained output and no retry."""
    with (ROOT/(script+'.stdout.log')).open('w',encoding='utf-8') as out, (ROOT/(script+'.stderr.log')).open('w',encoding='utf-8') as err:
        subprocess.run([str(python),'-X','utf8',str(ROOT/script)],stdout=out,stderr=err,timeout=timeout,check=True)


def main() -> None:
    """Wait for this setup only, acquire one input, and run one inference attempt."""
    status('WAITING_FOR_ISOLATED_RUNTIME')
    deadline=time.monotonic()+7200
    while not (ROOT/'RUNTIME_READY.json').exists():
        if (ROOT/'SETUP_FAILURE.json').exists():
            raise RuntimeError('Setup failed; see SETUP_FAILURE.json')
        if time.monotonic()>deadline:
            raise TimeoutError('Two-hour setup wait ended; no automatic continuation')
        time.sleep(30)
    status('ACQUIRING_SINGLE_FROZEN_INPUT')
    run(BASE,'acquire_input.py',600)
    status('RUNNING_ONE_CPU_FOUR_FLIP_INFERENCE')
    run(MODEL,'run_inference.py',1800)
    status('TECHNICAL_SMOKE_FINISHED_REVIEW_REQUIRED',result='SMOKE_RESULT.json',no_further_work_queued=True)


if __name__=='__main__':
    try:
        main()
    except Exception as error:
        status('BOUNDED_ATTEMPT_STOPPED',error_type=type(error).__name__,reason=str(error),no_retry=True)
        raise
