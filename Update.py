from bs4 import BeautifulSoup
import numpy as np
import os
import controle

with open(controle.web, 'r', encoding='utf-8') as arquivo:
    pagina = arquivo.read()


soup = BeautifulSoup(pagina, 'html.parser')

users = soup.find_all('span', class_='user-name')
exercises = soup.find_all('div', class_='score-card')
exercises = [exercise.text for exercise in exercises]


total_de_exercicios = len(exercises)/len(users)
total_de_exercicios = int(total_de_exercicios)

controle.Numero_alunos = len(users)
controle.Numero_questoes = total_de_exercicios - 1


tamanho_matriz = np.sqrt(len(users))
if int(tamanho_matriz) < tamanho_matriz:
    tamanho_matriz = tamanho_matriz + 1

controle.Tamanho_matriz = int(tamanho_matriz)

controle.Nome_alunos = [usuario.text for usuario in users]

exercises = np.array(exercises).reshape(len(users), total_de_exercicios)[:,1:]

def update():
    for i in range(len(users)):
        for j in range(total_de_exercicios - 1):
            if exercises[i, j][:3] == '100':
                if controle.concluidos[users[i].text][j] == False:
                    controle.pendentes[users[i].text][j] = True

def start():
    for user in users:
        controle.pendentes[user.text] = [False for i in range(int(total_de_exercicios) - 1)]
        controle.concluidos[user.text] = [False for i in range(int(total_de_exercicios) - 1)]
    
def delete():
    os.remove(controle.web)

