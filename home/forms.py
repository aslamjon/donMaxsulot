from django.forms import ModelForm  # bu bilan formalarni tez yasay olamiz
from django.contrib.auth.models import User
from django import forms
from .models import Home, mainBase, Qarz, InputQarz, PayAgent


class HomeForm(ModelForm):
    class Meta:
        model = Home
        fields = ['img', 'title', 'des', 'price']
        widgets = {
            'img': forms.FileInput(attrs={'class': "custom-file-input"}),
            'title': forms.TextInput(attrs={'placeholder': 'Maxsulot Nomi', 'class': "form-control"}),
            'des': forms.Textarea(attrs={'placeholder': 'Maxsulot Haqida', 'class': "form-control", "rows": '5'}),
            'price': forms.TextInput(attrs={'placeholder': 'Narxi', 'class': "form-control amount"})
        }


products = (
    ('Alanga vishi sort 1', 'Alanga vishi sort 1'),
    ("Naxo't", "Naxo't")
)


class Basee(ModelForm):
    class Meta:
        model = mainBase
        fields = ['typeOfProduct', 'kg', 'insidePrice', 'outsidePrice',
                  'totalSum', 'byWhom', 'changed', 'debt']
        widgets = {
            'typeOfProduct': forms.Select(attrs={'class': "form-control"}, choices=products),
            'kg': forms.TextInput(attrs={'placeholder': 'kg', 'class': "form-control amount"}),
            'insidePrice': forms.TextInput(attrs={'placeholder': 'Bazaga kirish narxi', 'class': "form-control amount"}),
            'outsidePrice': forms.TextInput(attrs={'placeholder': 'Bazadan chiqish narxi', 'class': "form-control amount"}),
            'totalSum': forms.TextInput(attrs={'placeholder': "To'liq Sum", 'class': "form-control amount", 'readonly': "true"}),
            'byWhom': forms.TextInput(attrs={'placeholder': "Kim tomonidan?", 'class': "form-control"}),
            'changed': forms.CheckboxInput(),
            'debt': forms.CheckboxInput(attrs={'class': "custom-control-input"})
        }


class LendDebt(ModelForm):
    class Meta:
        model = mainBase
        fields = ['lastLendDebt', 'oxirgiQarzBerganVaqti']
        widgets = {
            'lastLendDebt': forms.TextInput(attrs={'placeholder': 'Oxirgi bergan qarzini kiritish', 'class': "form-control amount"}),
            'oxirgiQarzBerganVaqti': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date', 'class': "form-control"})
        }


class QarzForm(ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # init is used for other fields initialization and crispy forms

    class Meta:
        model = Qarz
        fields = ['typeOfProduct', 'kg', 'orginalPrice',
                  'price', 'totalSum', 'byWhom', 'debt']
        widgets = {
            'typeOfProduct': forms.Select(attrs={'class': "form-control"}, choices=products),
            'kg': forms.TextInput(attrs={'placeholder': 'kg', 'class': "form-control amount"}),
            'orginalPrice': forms.TextInput(attrs={'placeholder': 'Yuqning asil narxi', 'class': "form-control amount"}),
            'price': forms.TextInput(attrs={'placeholder': 'Sotilayotgan narxi', 'class': "form-control amount"}),
            'totalSum': forms.TextInput(attrs={'placeholder': "To'liq Sum", 'class': "form-control amount", 'readonly': "true"}),
            'byWhom': forms.TextInput(attrs={'placeholder': 'Kim ?', 'class': "form-control"}),
            'debt': forms.CheckboxInput(attrs={'class': "custom-control-input"})
        }


class InputQarzForm(ModelForm):
    class Meta:
        model = InputQarz
        fields = ['qarzSum', 'oxirgiQarzBerganVaqti']
        widgets = {
            'qarzSum': forms.TextInput(attrs={'placeholder': 'Oxirgi bergan qarzini kiritish', 'class': "form-control amount"}),
            'oxirgiQarzBerganVaqti': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date', 'class': "form-control"}),
        }


class PayAgentForm(ModelForm):
    class Meta:
        model = PayAgent
        fields = ['who', 'payAgent']
        widgets = {
            'who': forms.TextInput(attrs={'placeholder': 'Kim?', 'class': "form-control"}),
            'payAgent': forms.TextInput(attrs={'placeholder': "Agentga to'langan summa", 'class': "form-control amount"}),
        }
