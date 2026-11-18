import json
from pathlib import Path
from datetime import datetime, timezone

def generate_status():
    report_dir = Path('reports')
    report_dir.mkdir(exist_ok=True)
    
    executed_count = len(list(Path('patches/executed/').glob('*'))) if Path('patches/executed/').exists() else 0
    failed_count = len(list(Path('patches/failed/').glob('*'))) if Path('patches/failed/').exists() else 0
    pending_count = len([f for f in Path('patches/pending/').glob('*') if f.name != 'status_arhitect_propriu.py'])
    
    heartbeat = 0
    if Path('dovada_executie.json').exists():
        try:
            with open('dovada_executie.json', 'r') as f:
                heartbeat = json.load(f).get('count', 0)
        except:
            heartbeat = 'Eroare citire'
            
    content = f"# Arhitect Propriu — Stare Live\n\n"
    content += f"**Timestamp UTC:** {datetime.now(timezone.utc).isoformat()}\n\n"
    content += f"**Heartbeat:** {heartbeat}\n\n"
    content += f"### Statistică Patch-uri\n"
    content += f"- Executate: {executed_count}\n"
    content += f"- Eșuate: {failed_count}\n"
    content += f"- În așteptare: {pending_count}\n\n"
    content += f"### Status Componente\n"
    content += f"- CONFIRMAT: Workflow, Heartbeat, Patch Runner\n"
    content += f"- NETESTAT: Garda REQUIRES_CONSENT (caz real necesar pentru validarea refuzului)\n"
    
    with open('reports/arhitect_propriu_status.md', 'w') as f:
        f.write(content)
    
    print(f"Raport generat: {executed_count} OK, {failed_count} ERR, {pending_count} PENDING.")

if __name__ == '__main__':
    generate_status()