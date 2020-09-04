import mimetypes
import os
import warnings
import zipfile
from itertools import combinations, cycle, product

import pandas as pd
from django.forms import formset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, reverse

from core.forms import (AlternativaForm, CriterioForm, DecisorForm,
                        NomeProjetoForm)
from core.models import (Alternativa, AvaliacaoAlternativas,
                         AvaliacaoCriterios, Criterio, Decisor, Projeto)

from .ElectreTri import ElectreTri
from .method import MatrizProjeto

warnings.filterwarnings('ignore')
pd.options.display.float_format = '{:,.4f}'.format


def index(request):
    template_name = 'index.html'
    projetos = Projeto.objects.all()

    if request.method == "POST":
        nome_projeto_form = NomeProjetoForm(request.POST)
        if nome_projeto_form.is_valid():
            projeto_novo = nome_projeto_form.save()

        return redirect('cadastradecisores', projeto_id=projeto_novo.id)

    else:
        nome_projeto_form = NomeProjetoForm()

    return render(request, template_name, {
        'nome_projeto_form': nome_projeto_form,
        'projetos': projetos,
    })


def metodo(request):
    template_name = 'metodo.html'

    return render(request, template_name)


def projeto(request, projeto_id):
    template_name = 'projeto.html'
    projeto = Projeto.objects.get(id=projeto_id)
    decisores = Decisor.objects.filter(projeto=projeto_id)
    alternativas = Alternativa.objects.filter(projeto=projeto_id)
    criterios = Criterio.objects.filter(projeto=projeto_id)

    return render(
        request, template_name, {
            'projeto': projeto,
            'decisores': decisores,
            'alternativas': alternativas,
            'criterios': criterios
        })


def deletarprojeto(request, projeto_id):
    redirect_page = '/'
    params_redirect = ''

    try:
        projeto = Projeto.objects.get(id=projeto_id)
        projeto.delete()
    except:
        redirect_page = 'resultado'
        params_redirect = projeto_id

    return redirect(redirect_page, projeto_id=params_redirect)


def editardados(request):
    nome = request.POST['nome']
    tipo_id = request.POST['tipoId'].split(':')
    tipo, _id = tipo_id[0], tipo_id[1]

    if tipo == 'projeto':
        projeto = Projeto.objects.get(id=_id)
        projeto.nome = _nome
        projeto.save()

    elif tipo == 'decisor':
        decisor = Decisor.objects.get(id=_id)
        decisor.nome = nome
        decisor.save()

    elif tipo == 'alternativa':
        alternativa = Alternativa.objects.get(id=_id)
        alternativa.nome = nome
        alternativa.save()

    elif tipo == 'criterio':
        criterio = Criterio.objects.get(id=_id)
        criterio.nome = nome
        criterio.save()

    return HttpResponse(nome)


def cadastradecisores(request, projeto_id):
    projeto = Projeto.objects.get(id=projeto_id)
    template_name = 'cadastra_decisores.html'
    projeto_nome = projeto.nome
    decisoresformset = formset_factory(form=DecisorForm)
    criteriosformset = formset_factory(form=CriterioForm)
    alternativasformset = formset_factory(form=AlternativaForm)

    if request.method == 'POST':
        decisor_form_set, criterios_form_set, alternativa_form_set = \
            decisoresformset(request.POST, prefix='decform'), criteriosformset(request.POST, prefix='critform'),\
            alternativasformset(request.POST, prefix='altform')
        if decisor_form_set.is_valid():
            for decisor_form in decisor_form_set:
                if decisor_form.is_valid():
                    decisor_novo = decisor_form.save()
                    decisor_novo.projeto = projeto
                    decisor_novo.save()
        if alternativa_form_set.is_valid():
            for alternativa_form in alternativa_form_set:
                if alternativa_form.is_valid():
                    nova_alternativa = alternativa_form.save()
                    nova_alternativa.projeto = projeto
                    nova_alternativa.save()
        if criterios_form_set.is_valid():
            for criterio_form in criterios_form_set:
                if criterio_form.is_valid():
                    criterio_novo = criterio_form.save()
                    criterio_novo.projeto = projeto
                    criterio_novo.save()
        return redirect('avaliarcriterios', projeto_id=projeto.id)

    else:
        decisor_form_set = decisoresformset(prefix='decform')
        criterio_form_set = criteriosformset(prefix='critform')
        alternativa_form_set = alternativasformset(prefix='altform')

    return render(
        request, template_name, {
            'decisor_form_set': decisor_form_set,
            'criterio_form_set': criterio_form_set,
            'alternativa_form_set': alternativa_form_set,
            'projeto_nome': projeto_nome,
            'projeto_id': projeto_id
        })


def cadastraalternativas(request, projeto_id):
    projeto = Projeto.objects.get(id=projeto_id)
    template_name = 'cadastra_alternativas.html'
    projeto_nome = projeto.nome
    alternativas = Alternativa.objects.filter(projeto=projeto_id)
    ultima_alternativa = None

    if request.method == 'POST':
        alternativa_form = AlternativaForm(request.POST)
        if alternativa_form.is_valid():
            alternativa_nova = alternativa_form.save()
            alternativa_nova.projeto = projeto
            alternativa_nova.save()

        return redirect('cadastraalternativas', projeto_id=projeto.id)

    else:
        alternativa_form = AlternativaForm()

    return render(
        request, template_name, {
            'alternativa_form': alternativa_form,
            'alternativas': alternativas,
            'projeto_nome': projeto_nome,
            'projeto_id': projeto_id
        })


def cadastracriterios(request, projeto_id):
    projeto = Projeto.objects.get(id=projeto_id)
    template_name = 'cadastra_criterios.html'
    projeto_nome = projeto.nome
    criterios = Criterio.objects.filter(projeto=projeto_id)
    criterios_quant = criterios.filter(numerico=True)
    criterios_quali = criterios.filter(numerico=False)

    if request.method == 'POST':
        criterio_form = CriterioForm(request.POST)
        if criterio_form.is_valid():
            criterio_novo = criterio_form.save()
            criterio_novo.projeto = projeto
            criterio_novo.save()

            return redirect('cadastracriterios', projeto_id=projeto.id)

    else:
        criterio_form = CriterioForm()

    contexto = {
        'criterio_form': criterio_form,
        'criterios': criterios,
        'projeto_nome': projeto_nome,
        'projeto_id': projeto_id,
        'criterios_quali': criterios_quali,
        'criterios_quant': criterios_quant
    }

    return render(request, template_name, context=contexto)


def avaliarcriterios(request, projeto_id):
    '''
    View para avaliar os critérios cadastrados.
    '''
    template_name = 'avaliar_criterios.html'
    projeto_id = projeto_id
    projeto = Projeto.objects.get(id=projeto_id)
    decisores = Decisor.objects.filter(projeto=projeto_id)
    criterios = Criterio.objects.filter(projeto=projeto_id)
    alternativas = Alternativa.objects.filter(projeto=projeto_id)

    criterios_combinados = list(combinations(criterios, 2))

    if request.method == 'POST':
        campos = dict(request.POST)
        _ = campos.pop('csrfmiddlewaretoken')
        decisor_id = campos.pop('decisor_id')

        notas_avaliadores = dict()
        for key, value in campos.items():
            tuplas = list(zip(decisor_id, value))
            notas_avaliadores[eval(key)] = tuplas

        lista_avaliacoes = []

        for (criterioA, criterioB), avaliacoes in notas_avaliadores.items():
            for (avaliador, nota) in avaliacoes:
                decisor = Decisor.objects.get(id=int(avaliador))
                criterio1 = Criterio.objects.get(id=criterioA)
                criterio2 = Criterio.objects.get(id=criterioB)
                avaliacao = AvaliacaoCriterios(projeto=projeto,
                                               decisor=decisor,
                                               criterioA=criterio1,
                                               criterioB=criterio2,
                                               nota=int(nota))
                avaliacao.save()
                avaliacao = AvaliacaoCriterios(projeto=projeto,
                                               decisor=decisor,
                                               criterioA=criterio2,
                                               criterioB=criterio1,
                                               nota=-int(nota))
                avaliacao.save()
        if len(alternativas) > 1:
            return redirect('avaliaralternativas', projeto_id)
        else:
            return redirect('resultado', projeto_id)

    return render(
        request, template_name, {
            'campos': request,
            'decisores': decisores,
            'criterios_combinados': criterios_combinados,
            'projeto_nome': projeto.nome,
        })


def avaliaralternativas(request, projeto_id):
    '''
    View para avaliar as alternativas cadastradas.
    '''
    template_name = 'avaliar_alternativas.html'
    projeto_id = projeto_id
    projeto = Projeto.objects.get(id=projeto_id)
    decisores = Decisor.objects.filter(projeto=projeto_id)
    criterios = Criterio.objects.filter(projeto=projeto_id, numerico=False)
    alternativas = Alternativa.objects.filter(projeto=projeto_id)

    alternativas_combinadas = list(combinations(alternativas, 2))

    if request.method == 'POST':
        campos = dict(request.POST)
        _ = campos.pop('csrfmiddlewaretoken')
        decisor_id = campos.pop('decisor_id')
        criterio_id = campos.pop('criterio_id')

        decisor_criterio = list(product(decisor_id, set(criterio_id)))

        notas_avaliadores = dict()
        for key, value in campos.items():
            tuplas = list(zip(decisor_criterio, value))
            notas_avaliadores[eval(key)] = tuplas

        for (alternativaA,
             alternativaB), avaliacoes in notas_avaliadores.items():
            for ((avaliador, criterio), nota) in avaliacoes:
                decisor = Decisor.objects.get(id=int(avaliador))
                criterio = Criterio.objects.get(id=criterio)
                alternativa1 = Alternativa.objects.get(id=int(alternativaA))
                alternativa2 = Alternativa.objects.get(id=int(alternativaB))
                avaliacao = AvaliacaoAlternativas(projeto=projeto,
                                                  decisor=decisor,
                                                  criterio=criterio,
                                                  alternativaA=alternativa1,
                                                  alternativaB=alternativa2,
                                                  nota=int(nota))
                avaliacao.save()

                avaliacao = AvaliacaoAlternativas(projeto=projeto,
                                                  decisor=decisor,
                                                  criterio=criterio,
                                                  alternativaA=alternativa2,
                                                  alternativaB=alternativa1,
                                                  nota=-int(nota))
                avaliacao.save()

        return redirect('resultado', projeto_id)

    return render(
        request, template_name, {
            'decisores': decisores,
            'alternativas_combinadas': alternativas_combinadas,
            'criterios': criterios,
            'projeto_nome': projeto.nome,
        })


def resultado(request, projeto_id):
    template_name = 'resultado.html'
    projeto = Projeto.objects.get(id=projeto_id)
    alternativas = Alternativa.objects.filter(projeto=projeto)
    matriz = MatrizProjeto(projeto)
    df_criterios = matriz.avaliacoes['criterios'].to_html()

    pesos = matriz.pesos_criterios
    pesos.sort_values(by='peso', ascending=False, inplace=True)
    pesos = pesos.to_html(index=False)

    if alternativas:
        df_alternativas = matriz.avaliacoes['alternativas'].to_html()
        pontuacao_alternativas = matriz.pontuacao_alternativas

        parametros = pd.DataFrame(None,
                                  index='p q v w'.split(),
                                  columns=matriz.pesos_criterios['Critério'])

        parametros.loc['p'] = 0.1
        parametros.loc['q'] = 0.2
        parametros.loc['v'] = 0.3
        parametros.loc['w'] = matriz.pesos_criterios['peso'].values
        parametros.index.rename('parametros')
        electre = ElectreTri(pontuacao_alternativas,
                             parametros,
                             lamb=0.75,
                             bn=3,
                             method='quantil')
        electre.renderizar()
        electre = ElectreTri(pontuacao_alternativas,
                             parametros,
                             lamb=0.75,
                             bn=3,
                             method='range')
        electre.renderizar()

        # pontuacao_alternativas.sort_values(by='pontuacao',
        # ascending=False,
        # inplace=True)
        pontuacao_alternativas = pontuacao_alternativas.to_html()

    else:
        pontuacao_alternativas = None

    return render(
        request, template_name, {
            'projeto': projeto,
            'pesos': pesos,
            'pontuacao_alternativas': pontuacao_alternativas,
            'df_alternativas': df_alternativas,
            'df_criterios': df_criterios,
        })


def download_file(request):
    fl_path = 'resultado.zip'
    filename = 'resultado.zip'

    # opening the 'Zip' in writing mode
    with zipfile.ZipFile(fl_path, 'a') as file:
        # append mode adds files to the 'Zip'
        # you have to create the files which you have to add to the 'Zip'
        file.write('resultado_range.xlsx')
        file.write('resultado_quantil.xlsx')

    fl = open(fl_path, 'rb')
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    os.remove('resultado.zip')
    os.remove('resultado_range.xlsx')
    os.remove('resultado_quantil.xlsx')
    return response
