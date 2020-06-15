from core.models import Projeto, Decisor, Alternativa, Criterio, AvaliacaoCriterios, AvaliacaoAlternativas, PageView
import collections

def inclui_decisor_no_projeto(projeto, decisor):
    projeto.decisores.add(decisor)
    return


def gerar_matriz(qtd_criterios, criterios_decisor):
    ### 1 - gerar matriz base
    matriz_base = []
    for i in range(qtd_criterios):
        matriz_base.append(list(range(1,qtd_criterios+1)))

    ### 2 - posicionar zeros na matriz base
    pos_zero = 1
    for lista in matriz_base:
        lista[pos_zero-1] = 0
        pos_zero +=1

    ### 3 - gerar nova matriz com valores positivos após o zero
    # remove os elementos após o 0
    for lista in matriz_base:
        zero_p = lista.index(0)
        for i in lista[zero_p+1:]:
            lista.remove(i)

    # separa os criterios em um dicionario
    dic_ = collections.OrderedDict()
    for i in range(1,qtd_criterios+1):
        key = 'c{}'.format(i)
        dic_[key] = []

    for i in criterios_decisor:
        k = i.criterios[:2]
        dic_[k].append(i.valor)

    # completa a matriz com valores positivos
    matriz_com_positivos = completa_matriz_com_positivos(matriz_base, dic_, qtd_criterios)

    ### 4 - gerar nova matriz com valores negativos antes do zero
    matriz_final = completa_matriz_com_negativos(matriz_com_positivos, dic_, qtd_criterios, criterios_decisor)

    return matriz_final


## GERAR MATRIZES
def gerar_matriz_alt(qtd_alternativas, matriz_base, lista_avaliacao):
    '''
    Funcao que gera as matrizes das alternativas
    Recebe <tal> e retorna <tal>

    Ex.:
    INPUT
    OUTPUT

    '''
    matriz = matriz_base

    ## posiciona zeros
    # [0, 1, 2, 3]
    # [1, 0, 1, 2]
    # [1, 2, 0, 1]
    # [1, 2, 3, 0]
    pos_zero = 1
    for lista in matriz:
        lista[pos_zero-1] = 0
        pos_zero += 1

    ## remove valores apos zeros
    # [0]
    # [1, 0]
    # [1, 2, 0]
    # [1, 2, 3, 0]
    for lista in matriz:
        zero_p = lista.index(0)
        for i in lista[zero_p+1:]:
            lista.remove(i)


    ## completar com positivos
    # [0, 1, 2, 3]
    # [1, 0, 1, 3]
    # [1, 2, 0, 1]
    # [1, 2, 3, 0]

    count = 0
    while count < qtd_alternativas:
        for i in list(lista_avaliacao):
            # if len(matriz[count]) < 4:
            if len(matriz[count]) < qtd_alternativas:
                matriz[count].append(i)
                lista_avaliacao.remove(i)
        count += 1


    ## completar com negativos
    # 1) Remover os elementos antes do 0 (zero)
    # [0, 1, 2, 3]
    # [0, 1, 3]
    # [0, 1]
    # [0]
    pos_zero = 0
    c = 0
    for l in matriz:
        for i in l[:c]:
            l.remove(i)
        c += 1


    # 2) Multiplica -1 e completa as matrizes
    # [0, 1, 2, 3]
    # [-1, 0, 1, 3]
    # [-1, -2, 0, 1]
    # [-1, -3, -3, 0]
    for l in matriz:
        for i, v in enumerate(l[1:]):
            if len(matriz[i+1]) < qtd_alternativas:
                matriz[i+1].insert(0,v*-1)

    return matriz


def completa_matriz_com_positivos(matriz, dic, qtd_criterios):
    matriz_nova = []
    for i in matriz:
        l = []
        for j in dic.values():
            if len(matriz_nova) < qtd_criterios:
                l = i+j
                matriz_nova.append(l)
    return matriz_nova

def completa_matriz_com_negativos(matriz_n, dic, qtd_criterios, criterios_decisor):
    criterios = {k:v for (v, k) in enumerate(dic.keys())}

    for i in criterios_decisor:
        k=i.criterios[-2:]
        indice = criterios[k]
        el = i.valor * -1
        matriz_n[indice].insert(0, el)

    return matriz_n


def completa_matriz_com_negativos_alt(matriz_n, dic, qtd_criterios, criterios_decisor):
    criterios = {k:v for (v, k) in enumerate(dic.keys())}

    for i in criterios_decisor:
        k=i.alternativas[-2:]
        indice = criterios[k]
        el = i.valor * -1
        matriz_n[indice].insert(0, el)

    return matriz_n


def normalizar(lista_elementos):
    lista_final_normalizada = []
    lista_dos_somados = []
    lista_normalizada = []
    lista_sem_zero = []
    for elemento in lista_elementos:
        soma = sum(elemento)
        lista_dos_somados.append(soma)


    '''
    Calcula o menor e o maior elementos antes de entrar no loop (só realiza a
    operação uma vez'''
    maior , menor = max(lista_dos_somados), min(lista_dos_somados)
    for elemento_da_soma in lista_dos_somados:
        if maior == menor:
            regular = 0
        else:
            regular = ((elemento_da_soma - menor)/(maior - menor))
        lista_normalizada.append(regular)

    for i in lista_normalizada:
        # >>>>> aqui que cria a lista
        # print('>>>>>>>>>>>>>>>')
        # print('i in lista_normalizada =>', i)
        # print('>>>>>>>>>>>>>>>')
        if i > 0:
            lista_sem_zero.append(i)



    for elemento_normalizado in lista_normalizada:
        menor_zero = 0
        if elemento_normalizado > 0:
            lista_final_normalizada.append(elemento_normalizado)
        else:
            try:
                """
                Tenta encontrar um mínimo não nulo.
                """
                # >>>>> erro aqui
                # min() arg is an empty sequence
                # print('>>>>>>>>>>>>>>>')
                # print('lista_sem_zero =>', lista_sem_zero)
                # print('>>>>>>>>>>>>>>>')
                menor_zero = min(lista_sem_zero)*0.01
            except ValueError:
                """
                Caso não encontre, forma uma lista de zeros.
                Se uma matriz só possuir zeros, a normalização vai retornar
                zero
                """
                menor_zero = 0

            lista_final_normalizada.append(menor_zero)
    # print(lista_final_normalizada)
    return lista_final_normalizada


def separa_elementos(lista_elementos, idx):
    '''
    Funcao que separa lista de listas pelo indice.

    Ex.:
    INPUT:
    lista_de_listas = [
        [0.3333, 1, 2, 3],
        [0.3333, 1, 2, 3],
        [0.3333, 1, 2, 3]
    ]

    separa_elementos(lista_de_listas, 0)

    OUTPUT:
    [0.33333, 0.33333, 0.33333]
    '''
    lista_separada = []
    for l in lista_elementos:
        lista_separada.append(l[idx])
    return lista_separada


def peso_criterios(lista_elementos):
    num_elementos = len(lista_elementos[0])

    soma_pesos = []
    for idx in range(num_elementos):
        lista_temp = []
        lista_temp = separa_elementos(lista_elementos, idx)
        soma_pesos.append(sum(lista_temp))

    return soma_pesos


def gerar_combinacoes_criterios(criterios):
    '''
    Funcao que gera combinacoes de criterios e alternativas
    de acordo os criterios e alternativas cadastrados

    Recebe uma lista com os codigos dos criterios (Queryset)
    [c1, c2, c3, c4]

    Retorna uma lista de tuplas
    [(c1, c2), (c1,c3) ('c1', 'c4')]

    -------

    Recebe uma lista com os codigos das alternativas (Queryset)
    [a1, a2, a3, a4]

    Retorna uma lista de tuplas
    [(a1, a2), (a1,a3) ('a1', 'a4')]
    '''
    from itertools import product

    criterios_keys = criterios
    genComb = product(criterios_keys, repeat=2)

    combinacoes = []
    for subset in genComb:
        l = list(subset)
        l.reverse()
        subset_reversed = tuple(l)

        if not subset[0] == subset[1]:
            if subset not in combinacoes  and subset_reversed not in combinacoes:
                combinacoes.append(subset)

    return combinacoes


def normalizar_alternativas(lista_elementos):
    lista_dos_somados = []
    lista_normalizada = []

    for elemento in lista_elementos:
        soma = sum(elemento)
        lista_dos_somados.append(soma)

    for elemento_da_soma in lista_dos_somados:
        maior , menor = max(lista_dos_somados), min(lista_dos_somados)
        if maior == menor :
            regular = 0
        else:
            regular = ((elemento_da_soma - menor)/(maior - menor))

        lista_normalizada.append(regular)

    return lista_normalizada


def separa_alternativas(criterio, lista_elementos, idx):
    num_el = len(lista_elementos[0])
    lista_separada = []

    if idx < num_el:
        for item in lista_elementos:
            lista_separada.append(item[idx])
    return lista_separada


def soma_alternativa_por_criterio(lista_elementos):
    num_elementos = len(lista_elementos[0]) -1
    lista_somada = []
    i = 0
    while i <= num_elementos:
        soma = sum([item[i] for item in lista_elementos])
        i =  i+ 1
        lista_somada.append(soma)
    return lista_somada


def separa_primeiros_elementos(lista_elementos, idx):
    lista_separada = []
    lista_separada = lista_elementos[idx]

    return lista_separada


def multiplicar_pelo_peso(lista_primeiros_elementos ,lista_pesos):
    lista_multi = []
    for numint, peso in enumerate(lista_pesos):

        multi = peso * lista_primeiros_elementos[numint]
        lista_multi.append(multi)

    return lista_multi


def multiplica_final(lista_elementos, lista_pesos):
    num_elementos = len(lista_elementos[0])

    lista_somada = []
    i = 0
    while i < num_elementos:
        lista_primeiros_elementos = []
        lista_primeiros_elementos = [item[i] for item in lista_elementos]
        lista_multi = []

        for numint, peso in enumerate(lista_pesos):
            multi = peso * lista_primeiros_elementos[numint]
            lista_multi.append(multi)

        i =  i + 1
        lista_somada.append(sum(lista_multi))
    return lista_somada


def registra_pageview():
    pageviews = PageView.objects.all()

    if pageviews:
        pageview = pageviews.get(id=1)
        pageview.views += 1
    else:
        pageview = PageView()
        pageview.views = 1
    pageview.save()

    return pageview.views
