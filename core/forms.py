from core.models import *
from django import forms


class NomeProjetoForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = (
            'nome',
            'descricao',
        )


class DecisorForm(forms.ModelForm):
    class Meta:
        model = Decisor
        fields = ('nome', )


class ProjetoForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = ('nome', 'decisores')


class AlternativaForm(forms.ModelForm):
    class Meta:
        model = Alternativa
        fields = ('nome', )


class CriterioForm(forms.ModelForm):
    class Meta:
        model = Criterio
        fields = ('nome', )


class CriterioNumericoForm(forms.ModelForm):
    class Meta:
        model = CriterioNumerico
        fields = ('nome', 'monotonico')


class AlternativaCriterioForm(forms.ModelForm):
    class Meta:
        model = AlternativaCriterio
        fields = ('projeto', 'alternativa', 'criterio', 'nota')


class CriterioParametroForm(forms.ModelForm):
    """description"""
    class Meta:
        model = CriterioParametro
        fields = 'projeto', 'criterio', 'p', 'q', 'v'
        widgets = {
            'projeto': forms.HiddenInput(),
            # 'decisor': forms.Select(attrs={'readonly': 'readonly'}),
            # 'criterio': forms.Select(attrs={'readonly': 'readonly'})
        }


class CriterioNumericoParametroForm(forms.ModelForm):
    """description"""
    class Meta:
        model = CriterioNumericoParametro
        fields = 'projeto', 'criterio', 'p', 'q', 'v'
        widgets = {
            'projeto': forms.HiddenInput(),
            # 'decisor': forms.Select(attrs={'readonly': 'readonly'}),
            # 'criterio': forms.Select(attrs={'readonly': 'readonly'})
        }
