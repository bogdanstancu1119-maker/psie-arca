import json, os, glob, datetime
from pathlib import Path

def generate_report():
    os.makedirs('reports', exist_ok=True)
    files = glob.glob('patches/results/*.result.json')
    stats = {'success': 0, 'failed': 0, 'blocked': 0}
    results_data = []
    for f in files:
        try:
            with open(f, 'r') as jf:
                data = json.load(jf)
                status = data.get('status', '')
                if status == 'executed: success': stats['success'] += 1
                elif status == 'executed: failed': stats['failed'] += 1
                elif status == 'blocked: approval_required': stats['blocked'] += 1
                results_data.append(data)
        except: continue
    heartbeat = 0
    if os.path.exists('dovada_executie.json'):
        with open('dovada_executie.json', 'r') as df:
            d = json.load(df)
            heartbeat = d.get('contor', 0)
    consent = 'CONFIRMATĂ' if stats['blocked'] > 0 else 'NETESTAT'
    timestamp = datetime.datetime.utcnow().isoformat()
    report = '# Hydra Status Report\n'
    report += 'Timestamp: ' + timestamp + '\n'
    report += 'Heartbeat: ' + str(heartbeat) + '\n\n'
    report += '## Statistici\n- Success: ' + str(stats['success']) + '\n'
    report += '- Failed: ' + str(stats['failed']) + '\n'
    report += '- Blocked: ' + str(stats['blocked']) + '\n\n'
    report += 'REQUIRES_CONSENT: ' + consent + '\n\n'
    report += '## Recente\n'
    for item in sorted(results_data, key=lambda x: x.get('timestamp', ''), reverse=True)[:10]:
        report += '- ID: ' + str(item.get('run_id', 'N/A')) + ' | SHA: ' + str(item.get('commit_sha', '')[:12]) + '\n'
    with open('reports/arhitect_propriu_status.md', 'w') as f:
        f.write(report)
    print('Raport generat: reports/arhitect_propriu_status.md')

if __name__ == '__main__':
    generate_report()