import os
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

def run_runner():
    dirs = ['patches/pending', 'patches/executed', 'patches/failed', 'patches/results']
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)
    
    pending = list(Path('patches/pending').glob('*.py'))
    summary = {'total': len(pending), 'success': 0, 'failed': 0, 'consent_needed': 0}
    
    for script in pending:
        with open(script, 'r') as f:
            content = f.read(200)
            if '# REQUIRES_CONSENT' in content[:200]:
                summary['consent_needed'] += 1
                continue

        try:
            res = subprocess.run([sys.executable, str(script)], capture_output=True, text=True, timeout=60)
            result_data = {'stdout': res.stdout, 'stderr': res.stderr, 'returncode': res.returncode, 'timestamp': str(datetime.utcnow())}
            with open(f'patches/results/{script.name}.result.json', 'w') as f:
                json.dump(result_data, f)
            
            if res.returncode == 0:
                script.rename(f'patches/executed/{script.name}')
                summary['success'] += 1
            else:
                script.rename(f'patches/failed/{script.name}')
                summary['failed'] += 1
        except Exception as e:
            summary['failed'] += 1
            with open(f'patches/results/{script.name}.error.txt', 'w') as f:
                f.write(str(e))
            script.rename(f'patches/failed/{script.name}')

    print(f"Rezumat: {summary}")

if __name__ == '__main__':
    run_runner()