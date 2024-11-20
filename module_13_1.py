from time import sleep
import asyncio

async def start_strongman(name, power):
    print(f'Силач {name} начал соревнования.')
    for i in range(5):
        await asyncio.sleep(1 / power)
        print(f'Силач {name} поднял {i+1} шар.')
    print(f'Силач {name} закончил соревнования.')

async def start_tournament():
    st_man1 = asyncio.create_task(start_strongman('Pasha', 3))
    st_man2 = asyncio.create_task(start_strongman('Denis', 4))
    st_man3 = asyncio.create_task(start_strongman('Apollon', 5))
    await st_man1
    await st_man2
    await st_man3

asyncio.run(start_tournament())