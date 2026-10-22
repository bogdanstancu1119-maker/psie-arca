import random

def echilibrare_organe(organe_total=212, activi=59):
    target = 3
    if activi < target:
        deficit = target - activi
        return f"Activare forțată pentru {deficit} organe din stocul inactiv"
    return "Sistem în parametri minimi de redundanță"

# Patch pentru hidratare_critica.py
print(echilibrare_organe())