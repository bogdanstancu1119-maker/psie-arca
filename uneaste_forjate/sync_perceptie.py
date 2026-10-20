import json

def sync_realitate_canonica():
    # Sincronizare hydraPerceptieUnica cu interfața
    reg_canonic = {'status': 'integrat', 'sursa': 'hydraPerceptieUnica'}
    with open('interface_registry.json', 'w') as f:
        json.dump(reg_canonic, f)
    return True

if __name__ == '__main__':
    sync_realitate_canonica()