#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json

import pandas as pd

import requests as r

# ### Dicionário contendo os dados para o electre

# In[2]:


ests = {
    'x': [[0.1, 0.2, 0.3, 0.4], [0.1, 0.2, 0.3, 0.4], [0.1, 0.2, 0.3, 0.4], [0.1, 0.2, 0.3, 0.4]],
    'p': [0.1, 0.2, 0.3, 0.4],
    'q': [0.1, 0.2, 0.3, 0.4],
    'v': [0.1, 0.2, 0.3, 0.4],
    'w': [0.1, 0.2, 0.3, 0.4],
    'bh': [[0.1, 0.2, 0.3, 0.4], [0.1, 0.2, 0.3, 0.4], [0.1, 0.2, 0.3, 0.4], [0.1, 0.2, 0.3, 0.4]]
}


# ### Transforma o dicionário para Json (JavaScript Object Notation) para mandar para o servidor electre

# In[3]:

print(ests)
payload = json.dumps(ests)


# # ### Faz a Requisição na url e recupera a resposta em formato Json

# # In[4]:


# resposta = r.post('http://localhost:8080/electre', data=payload)


# # In[5]:


# print(resposta)


# # ### Cria um DataFrame (tabela) a partir da resposta

# # In[6]:

# json = resposta.json()['arrayCLs']
# with open('teste.json', 'w') as js:
    # js.writelines(str(json))
# # ### Salva em excel

# # In[8]:


# def electre(ests: dict) -> json:
    # return r.post('http://localhost:8090/electre', data = json.dumps(ests)).json()


# # In[ ]:
