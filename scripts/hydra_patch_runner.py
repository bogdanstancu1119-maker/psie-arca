import json
import os
import hashlib
import subprocess
import shutil
from datetime import datetime

EXECUTOR_VERSION = '1.2.0'

def run():
    registry_path = 'patches/approval_registry.json'
    pending_dir = 'patches/pending'
    audit_log = 'patches/audit_log.jsonl'
    env_run_id = os.getenv('GITHUB_RUN_ID', 'manual')
    env_commit = os.getenv('GITHUB_SHA', 'local')
    
    stats = {'executed': 0, 'blocked': {}, 'fail_closed': False}

    def log_audit(data):
        with open(audit_log, 'a') as f:
            f.write(json.dumps({**data, 'timestamp': datetime.utcnow().isoformat()}) + '\n')

    try:
        with open(registry_path, 'r') as f:
            registry = json.load(f)
            approvals = registry.get('approvals', [])
            if not isinstance(approvals, list): raise ValueError
    except Exception:
        stats['fail_closed'] = True
        for f_name in os.listdir(pending_dir):
            if f_name.endswith('.py'):
                log_audit({'script_hash': 'N/A', 'nume_fisier': f_name, 'decizie': 'registry_unavailable', 'run_id': env_run_id, 'commit_sha': env_commit})
        print('Fail-closed active: Registry invalid.')
        return

    for f_name in os.listdir(pending_dir):
        if not f_name.endswith('.py'): continue
        path = os.path.join(pending_dir, f_name)
        with open(path, 'r') as f:
            content = f.read()
            script_hash = hashlib.sha256(content.encode()).hexdigest()
        
        if '# REQUIRES_CONSENT' in content[:200]:
            stats['blocked']['approval_required'] = stats['blocked'].get('approval_required', 0) + 1
            log_audit({'script_hash': script_hash, 'nume_fisier': f_name, 'decizie': 'blocked_approval_required', 'run_id': env_run_id, 'commit_sha': env_commit})
            continue
        
        match = next((a for a in approvals if a.get('hash') == script_hash), None)
        if not match:
            stats['blocked']['not_in_registry'] = stats['blocked'].get('not_in_registry', 0) + 1
            log_audit({'script_hash': script_hash, 'nume_fisier': f_name, 'decizie': 'blocked_not_in_approved_registry', 'run_id': env_run_id, 'commit_sha': env_commit})
            continue
        
        if match.get('status') != 'activ':
            stats['blocked']['revoked'] = stats['blocked'].get('revoked', 0) + 1
            log_audit({'script_hash': script_hash, 'nume_fisier': f_name, 'decizie': 'blocked_revoked', 'run_id': env_run_id, 'commit_sha': env_commit})
            continue

        res = subprocess.run(['python3', path], capture_output=True, text=True, timeout=60)
        out = {'returncode': res.returncode, 'stdout': res.stdout, 'stderr': res.stderr, 'script_hash': script_hash, 'run_id': env_run_id, 'commit_sha': env_commit, 'executor_version': EXECUTOR_VERSION, 'decision_id': match.get('id'), 'approved_by': match.get('approved_by')}
        
        dest = 'patches/executed/' if res.returncode == 0 else 'patches/failed/'
        with open(f'patches/results/{f_name}.result.json', 'w') as f: json.dump(out, f)
        shutil.move(path, os.path.join(dest, f_name))
        stats['executed'] += 1
        log_audit({'script_hash': script_hash, 'nume_fisier': f_name, 'decizie': 'executed_success' if res.returncode == 0 else 'executed_failed', 'run_id': env_run_id, 'commit_sha': env_commit})

    print(f'Final: {stats}')

if __name__ == '__main__': run()