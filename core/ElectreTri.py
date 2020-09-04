#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: electre_tri.py
Author: Alexandre Castro
Email: im.alexandre07@gmail.com
Github: https://www.github.com/im-alexandre
Description: Implementação do electre_tri em python
"""
import warnings
# +
from itertools import product

import numpy as np
import pandas as pd

warnings.filterwarnings('ignore')


class ElectreTri():
    """ Calcula as matrizes de concordância, discordância e credibilidade,
    self.dados as alternativas e os parametros"""

    def __init__(self, entrada, parametros, lamb, bn, method='quantil'):
        self.entrada = entrada
        self.parametros = parametros
        self.lamb = lamb
        self.bn = bn
        self.method = method

    def _escalona(self, coluna):
        escala = (max(coluna) - min(coluna)) / (self.bn)
        coluna_escalonada = np.arange(min(coluna), max(coluna), escala)[1:]
        return coluna_escalonada

    def pessimista(self, row):
        """docstring for pessimista"""
        if row['cred(b,x)'] >= self.lamb and row['cred(x,b)'] >= self.lamb:
            return 'x > b'
        elif row['cred(b,x)'] >= self.lamb and row['cred(x,b)'] < self.lamb:
            return 'x < b'
        elif row['cred(b,x)'] < self.lamb and row['cred(x,b)'] >= self.lamb:
            return 'x > b'
        else:
            return 'x < b'

    def otimista(self, row):
        """docstring for pessimista"""
        if row['cred(b,x)'] >= self.lamb and row['cred(x,b)'] >= self.lamb:
            return 'x > b'
        elif row['cred(b,x)'] >= self.lamb and row['cred(x,b)'] < self.lamb:
            return 'x < b'
        elif row['cred(b,x)'] < self.lamb and row['cred(x,b)'] >= self.lamb:
            return 'x > b'
        else:
            return 'x > b'

    def credibilidade(self, row: pd.Series) -> float:
        """
        Calcula a matriz de credibilidade, dada uma matriz de concordância ou
        discordância
        """
        concordancia = row.values[-1]
        discordancias = row.values[:-1]
        discordancias = discordancias[discordancias > concordancia]
        if len(discordancias) > 0:
            lista = (1 - discordancias) / (1 - concordancia)
            credibilidade = concordancia * (lista.cumprod())
            return credibilidade[-1]
        else:
            credibilidade = concordancia
            return credibilidade

    def discordancia(self, serie: pd.Series, xi: str, bh: pd.Series) -> float:
        """
        Calcula a dicordância entre a classe e a alternativa (ou vice-versa),
        dada uma série com os atributos da alternativa, os critérios e as
        fronteiras de classe em cada critério
        """
        diferenca = serie[bh] - serie[xi]
        if diferenca < serie['p']:
            return 0
        elif diferenca > serie['v']:
            return 1
        elif serie['p'] <= diferenca < serie['v']:
            resposta = (-serie['p'] + diferenca) / (serie['v'] - serie['p'])
            return resposta

    def concordancia_parcial(self, serie, xi, bh, w):
        diferenca = serie[bh] - serie[xi]
        if diferenca >= serie['p']:
            return 0
        elif diferenca < serie['q']:
            return 1
        elif serie['q'] <= diferenca < serie['p']:
            resposta = ((serie['p'] - diferenca) * serie['w']) / (serie['p'] -
                                                                  serie['q'])
            pesos = w.sum()
            return resposta / pesos

    def renderizar(self, ):
        """docstring for renderizar"""
        alternativas = list(self.entrada.index)

        if self.method == 'quantil':
            self.cla_df = pd.DataFrame(
                self.entrada.quantile(q=np.arange(0, 1, 1 / (self.bn - 1)),
                                      interpolation='lower'))
            self.cla = [f'b{i}' for i in range(1, self.cla_df.shape[0] + 1)]
            self.cla_df.index = self.cla

        elif self.method == 'range':
            self.cla_df = self.entrada.apply(self._escalona)
            print(self.cla_df)
            self.cla = [f'b{i}' for i in range(1, self.cla_df.shape[0] + 1)]
            self.cla_df.index = self.cla

        self.dados = pd.concat(
            [self.entrada, self.cla_df, self.parametros],
            axis=0,
        )
        self.index = pd.MultiIndex.from_product(
            [alternativas, self.cla], names=['alternativa', 'classe'])
        self.df = pd.DataFrame(None,
                               index=self.index,
                               columns=self.entrada.columns)

        self.df_concordancia_x_b = self.df.copy()
        self.df_concordancia_b_x = self.df.copy()
        self.df_discordancia_x_b = self.df.copy()
        self.df_discordancia_b_x = self.df.copy()
        for a, c in self.df.index:
            self.df.at[(a, c)] = self.dados.loc[c] - self.dados.loc[a]

        for (x, b), g in product(self.df_concordancia_b_x.index,
                                 self.df_concordancia_b_x.columns):
            self.df_concordancia_x_b.at[(x, b), g] = self.concordancia_parcial(
                self.dados[g], xi=x, bh=b, w=self.dados.loc['w'])
            self.df_concordancia_b_x.at[(x, b), g] = self.concordancia_parcial(
                self.dados[g], xi=b, bh=x, w=self.dados.loc['w'])

        for (x, b), g in product(self.df_discordancia_x_b.index,
                                 self.df_discordancia_x_b.columns):
            self.df_discordancia_x_b.at[(x, b),
                                        g] = self.discordancia(self.dados[g],
                                                               xi=x,
                                                               bh=b)

        for (x, b), g in product(self.df_discordancia_b_x.index,
                                 self.df_discordancia_b_x.columns):
            self.df_discordancia_b_x.at[(x, b),
                                        g] = self.discordancia(self.dados[g],
                                                               xi=b,
                                                               bh=x)

        self.df_concordancia_x_b['c(x,b)'] = self.df_concordancia_x_b.apply(
            np.mean, axis=1)
        self.df_concordancia_b_x['c(b,x)'] = self.df_concordancia_b_x.apply(
            np.mean, axis=1)

        self.df_credibilidade_b_x = pd.concat(
            [self.df_discordancia_b_x, self.df_concordancia_b_x['c(b,x)']],
            axis=1)
        self.df_credibilidade_b_x[
            'cred(b,x)'] = self.df_credibilidade_b_x.apply(self.credibilidade,
                                                           axis=1)

        self.df_credibilidade_x_b = pd.concat(
            [self.df_discordancia_x_b, self.df_concordancia_x_b['c(x,b)']],
            axis=1)
        self.df_credibilidade_x_b[
            'cred(x,b)'] = self.df_credibilidade_x_b.apply(self.credibilidade,
                                                           axis=1)

        ordenacao = pd.concat([self.entrada, self.cla_df])

        self.credibilidade_df = pd.concat([
            self.df_credibilidade_x_b['cred(x,b)'],
            self.df_credibilidade_b_x['cred(b,x)']
        ],
            axis=1)

        self.credibilidade_df['pesimista'] = self.credibilidade_df.apply(
            self.pessimista, axis=1)

        self.credibilidade_df['otimista'] = self.credibilidade_df.apply(
            self.otimista, axis=1)

        self.credibilidade_df['lambda'] = self.lamb

        tab = pd.ExcelWriter(f'resultado_{self.method}.xlsx')
        self.cla_df.to_excel(tab, 'bhs')
        self.parametros.to_excel(tab, 'parametros')
        self.df_concordancia_x_b.to_excel(tab, 'concordancia_x_b')
        self.df_concordancia_b_x.to_excel(tab, 'concordancia_b_x')
        self.df_discordancia_b_x.to_excel(tab, 'discordancia_b_x')
        self.df_discordancia_x_b.to_excel(tab, 'discordancia_x_b')
        self.df_credibilidade_b_x.to_excel(tab, 'credibilidade_b_x')
        self.df_credibilidade_x_b.to_excel(tab, 'credibilidade_x_b')
        self.credibilidade_df.to_excel(tab, 'classificações')

        tab.save()


if __name__ == '__main__':
    entrada = pd.read_excel('electre.xlsx', sheet_name='alternativas')
    parametros = pd.read_excel('electre.xlsx', sheet_name='parametros')
    ElectreTri(entrada, parametros, 0.75).renderizar()
