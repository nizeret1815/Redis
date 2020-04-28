import redis
import json
import random
import time

jogadores = redis.Redis(host='localhost', port=6379, db=0)

bingo = redis.Redis(host='localhost', port=6379, db=1)

chave = ''

for i in range(0, 50):
    if i < 10:
        chave = f'0{i + 1}'
    else:
        chave = str(i)

    jogador = {
        "nome": f'user{chave}',
        "valores_cartela": [],
        "score": 0
    }

    for j in range(0, 15):
        jogador['valores_cartela'].append(random.randint(1, 99))

    jogadores.set(f'jogador{chave}', json.dumps(jogador))

for k in range(0, 100):
    if k > 0:
        bingo.rpush('pedras', k)

houve_vencedor = False

while(bingo.llen('pedras') != 0):

    if houve_vencedor:
        break

    pedra = int(bingo.rpop('pedras'))

    for i in range(0, 50):

        if houve_vencedor:
            break

        if i < 10:
            chave = f'0{i + 1}'
        else:
            chave = str(i)

        jogador = json.loads(jogadores.get(f'jogador{chave}'))

        if pedra in jogador['valores_cartela']:
            jogador['score'] = int(jogador['score']) + 1
            if int(jogador['score'] == 15):
                nome = str(jogador['nome'])
                print(f'O jogador vencedor é: {nome}')
                houve_vencedor = True
            else:
                jogadores.set(f'jogador{chave}', json.dumps(jogador))

if not houve_vencedor:
    print('Não houve vencedor!!!')


    

