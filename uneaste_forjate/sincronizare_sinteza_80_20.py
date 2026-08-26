import json

def aplicare_mod_sinteza(date_brute):
    config_sinteza = {"mod": "80/0/20", "prioritate": "optimizare"}
    print(f"Sincronizare Symbiote activata: {config_sinteza}")
    return config_sinteza

if __name__ == '__main__':
    aplicare_mod_sinteza('6a886f24378b4249aef4d305')