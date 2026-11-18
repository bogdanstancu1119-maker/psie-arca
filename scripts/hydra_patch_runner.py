import os
import hashlib
import json
import subprocess
import shutil
from datetime import datetime

EXECUTOR_VERSION = '1.1.0'

def run():
    dirs = ['patches/pending', 'patches/results', 'patches/executed', 'patches/failed']
    for d in dirs: os.makedirs(d, exist_ok=True)
    stats = {'executed': 0, 'blocked': 0, 'failed': 0}
    run_id = os.environ.get('GITHUB_RUN_ID', 'local')
    commit_sha = os.environ.get('GITHUB_SHA', 'unknown')

    for filename in os.listdir('patches/pending'):
        if not filename.endswith('.py'): continue
        path = os.path.join('patches/pending', filename)
        with open(path, 'r') as f: content = f.read()
        
        script_hash = hashlib.sha256(content.encode()).hexdigest()
        meta = {'script_hash': script_hash, 'run_id': run_id, 'commit_sha': commit_sha, 'executor_version': EXECUTOR_VERSION, 'timestamp': datetime.utcnow().isoformat()}
        
        if '# REQUIRES_CONSENT' in content[:200]:
            meta['status'] = 'blocked: approval_required'
            with open(f'patches/results/{filename}.result.json', 'w') as f: json.dump(meta, f)
            stats['blocked'] += 1
            continue
            
        res = subprocess.run(['python3', path], capture_output=True, text=True, timeout=60)
        meta.update({'status': 'executed: success' if res.returncode == 0 else 'executed: failed', 'stdout': res.stdout, 'stderr': res.stderr, 'returncode': res.returncode})
        
        with open(f'patches/results/{filename}.result.json', 'w') as f: json.dump(meta, f)
        dest = 'patches/executed' if res.returncode == 0 else 'patches/failed'
        shutil.move(path, os.path.join(dest, filename))
        stats['executed' if res.returncode == 0 else 'failed'] += 1

    print(f"Final Report: Executed: {stats['executed']}, Blocked: {stats['blocked']}, Failed: {stats['failed']}")

if __name__ == '__main__': run()