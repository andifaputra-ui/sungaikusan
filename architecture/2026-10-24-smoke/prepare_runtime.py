"""Approved isolated CPU setup; download wheels first, then install offline."""
from __future__ import annotations
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import venv
import zipfile
from resource_budget import Budget

ROOT = Path(__file__).resolve().parent
PREP = ROOT.parent/'NATIVE_MODEL_READINESS_20261023'
RUNTIME = Path('E:/Bendungan_Kusan/Model_Runtime/s1_smoke_cpu_20261024')
ENV = RUNTIME/'venv'
PYTHON = ENV/'Scripts/python.exe'
WHEELS = RUNTIME/'wheels'
STORAGE_LIMIT = 6*1024**3


def run(command: list[str], environment: dict[str,str]) -> None:
    """Run one setup step; halt instead of retrying silently."""
    subprocess.run(command, check=True, env=environment)


def main() -> None:
    """Resolve pinned CPU roots, preserve exact wheels/lock and frozen payloads."""
    RUNTIME.mkdir(parents=True, exist_ok=True)
    temporary = RUNTIME/'tmp'
    temporary.mkdir(exist_ok=True)
    environment = dict(os.environ, TEMP=str(temporary), TMP=str(temporary),
                       PIP_CACHE_DIR=str(RUNTIME/'pip-cache'),
                       PYTHONUTF8='1', PIP_DISABLE_PIP_VERSION_CHECK='1',
                       PIP_CONFIG_FILE=os.devnull)
    if not PYTHON.exists():
        venv.EnvBuilder(with_pip=True).create(ENV)
    WHEELS.mkdir(exist_ok=True)
    requirements = ROOT/'requirements_roots.txt'
    requirements.write_text('''torch @ https://download.pytorch.org/whl/cpu/torch-2.8.0%2Bcpu-cp312-cp312-win_amd64.whl
torchvision @ https://download.pytorch.org/whl/cpu/torchvision-0.23.0%2Bcpu-cp312-cp312-win_amd64.whl
fastai==2.8.4
numpy==2.2.6
pandas==2.3.3
rasterio==1.4.3
matplotlib==3.10.7
scipy==1.16.2
''', encoding='utf-8')
    run([str(PYTHON),str(ROOT/'metered_pip.py'),'download','--only-binary=:all:',
         '--no-cache-dir','--retries','0','--timeout','120','--index-url','https://pypi.org/simple',
         '--dest',str(WHEELS),'-r',str(requirements)], environment)
    wheel_files = sorted(WHEELS.glob('*.whl'))
    installed_upper = sum(sum(i.file_size for i in zipfile.ZipFile(p).infolist()) for p in wheel_files)
    existing = sum(p.stat().st_size for p in RUNTIME.rglob('*') if p.is_file())
    if existing + installed_upper + 512*1024**2 > STORAGE_LIMIT:
        raise RuntimeError('Offline installation would exceed approved storage envelope')
    wheel_receipts = [{'file':p.name,'bytes':p.stat().st_size,
                       'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in wheel_files]
    (ROOT/'WHEEL_RECEIPTS.json').write_text(json.dumps(wheel_receipts,indent=2)+'\n',encoding='utf-8')
    run([str(PYTHON),'-m','pip','install','--no-index','--no-deps',*[str(p) for p in wheel_files]], environment)
    run([str(PYTHON),'-m','pip','check'], environment)
    lock = subprocess.check_output([str(PYTHON),'-m','pip','freeze','--all'],env=environment,text=True,encoding='utf-8')
    (ROOT/'requirements_lock.txt').write_text(lock,encoding='utf-8')
    contract = json.loads((PREP/'FROZEN_ARTIFACT_CONTRACT.json').read_text(encoding='utf-8'))
    budget = Budget()
    results = []
    for artifact in contract['files']:
        if artifact['variant'] != 's1_only_resnet34':
            continue
        destination = RUNTIME/'model'/Path(artifact['path']).name
        url = 'https://huggingface.co/rohitm9/surfaceWaterGlobal/resolve/'+contract['HF_resolved_commit']+'/'+artifact['path']
        results.append(budget.fetch(url,destination,artifact['bytes'],artifact['expected_sha256']))
    used = sum(p.stat().st_size for p in RUNTIME.rglob('*') if p.is_file())
    if used > STORAGE_LIMIT:
        raise RuntimeError('Storage ceiling exceeded')
    (ROOT/'RUNTIME_READY.json').write_text(json.dumps({'status':'READY_FOR_INPUT_AND_INFERENCE',
        'python':str(PYTHON),'storage_bytes':used,'model_payloads':results},indent=2)+'\n',encoding='utf-8')
    print('RUNTIME_READY',used,flush=True)


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        (ROOT/'SETUP_FAILURE.json').write_text(json.dumps({'status':'SETUP_STOPPED','type':type(error).__name__,'reason':str(error)},indent=2)+'\n',encoding='utf-8')
        raise
