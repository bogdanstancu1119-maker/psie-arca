import logging
from datetime import datetime, timedelta

def check_deploy_reversibility():
    deployment_date = datetime(2026, 8, 1)
    deadline = deployment_date + timedelta(hours=72)
    if datetime.now() < deadline:
        logging.warning('Fereastra de 72h activa. Monitorizarea integritatii nodurilor este prioritara.')
        return True
    return False

if __name__ == '__main__':
    check_deploy_reversibility()