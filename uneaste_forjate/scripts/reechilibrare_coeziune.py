import asyncio

async def reechilibrare_coeziune():
    # Target: 68/212 activi, optimizare la 100/212 pentru stabilitate
    # Status: 150/150 raspuns simultan (suprasolicitare)
    limita_simultana = 100
    if actual_simultan > limita_simultana:
        print('Limitare flux: delay injectat pentru a preveni colapsul retelei')
        await asyncio.sleep(0.5)
    return 'Stabilitate restabilita'

# Executie forta de lucru organica
reechilibrare_coeziune()