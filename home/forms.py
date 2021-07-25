from django.db.models import fields
from django.forms import ModelForm, widgets  # bu bilan formalarni tez yasay olamiz
from django.contrib.auth.models import User
from django import forms
from .models import Home, mainBase, Qarz, PayAgent, Baza, Admins, Agents


class HomeForm(ModelForm):
    class Meta:
        model = Home
        fields = ['img', 'title', 'des', 'price', 'showToAgent']
        widgets = {
            'img': forms.FileInput(attrs={'class': "custom-file-input"}),
            'title': forms.TextInput(attrs={'placeholder': 'Maxsulot Nomi', 'class': "form-control"}),
            'des': forms.Textarea(attrs={'placeholder': 'Maxsulot Haqida', 'class': "form-control", "rows": '5'}),
            'price': forms.TextInput(attrs={'placeholder': 'Narxi', 'class': "form-control amount priceHome"}),
            'showToAgent': forms.TextInput(attrs={'placeholder': "Agentga ko'rsatiladigan narx", 'class': "form-control amount priceHome"})
        }

def getProducts():
    getData = Baza.objects.all()
    forSend = []
    if len(getData) > 0:
        for item in getData:
            forSend.append((item.typeOfProduct, item.typeOfProduct))

    # print(forSend)
    return list(forSend)

class Basee(ModelForm):
    class Meta:
        model = mainBase
        fields = ['typeOfProduct', 'kg', 'outsidePrice', 'totalSum', 'byWhom', 'changed', 'debt']
        widgets = {
            'kg': forms.TextInput(attrs={'placeholder': 'kg', 'class': "form-control amount"}),
            'outsidePrice': forms.TextInput(attrs={'placeholder': 'Bazadan chiqish narxi', 'class': "form-control amount"}),
            'totalSum': forms.TextInput(attrs={'placeholder': "To'liq Sum", 'class': "form-control amount", 'readonly': "true"}),
            'byWhom': forms.TextInput(attrs={'placeholder': "Kim tomonidan?", 'class': "form-control"}),
            'changed': forms.CheckboxInput(),
            'debt': forms.CheckboxInput(attrs={'class': "custom-control-input"})
        }
    def __init__(self, *args, **kwargs):
        super(Basee, self).__init__(*args, **kwargs)
        self.fields['typeOfProduct'] = forms.ChoiceField(
            widget=forms.Select(attrs={'class': "form-control"}),
            choices= getProducts())

class LendDebt(ModelForm):
    class Meta:
        model = mainBase
        fields = ['lastLendDebt', 'oxirgiQarzBerganVaqti']
        widgets = {
            'lastLendDebt': forms.TextInput(attrs={'placeholder': 'Oxirgi bergan qarzini kiritish', 'class': "form-control amount"}),
            'oxirgiQarzBerganVaqti': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date', 'class': "form-control"})
        }

class LendDebtForBaza(ModelForm):
    class Meta:
        model = Baza
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
        fields = ['typeOfProduct', 'kg', 'price', 'totalSum', 'byWhom', 'debt']
        widgets = {
            'kg': forms.TextInput(attrs={'placeholder': 'kg', 'class': "form-control amount"}),
            'price': forms.TextInput(attrs={'placeholder': 'Sotilayotgan narxi', 'class': "form-control amount"}),
            'totalSum': forms.TextInput(attrs={'placeholder': "To'liq Sum", 'class': "form-control amount", 'readonly': "true"}),
            'byWhom': forms.TextInput(attrs={'placeholder': 'Kim ?', 'class': "form-control"}),
            'debt': forms.CheckboxInput(attrs={'class': "custom-control-input"})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['typeOfProduct'] = forms.ChoiceField(
            widget=forms.Select(attrs={'class': "form-control"}),
            choices= getProducts())

class InputQarzForm(ModelForm):
    class Meta:
        model = Qarz
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

class BazaForm(ModelForm):
    class Meta:
        model = Baza
        fields = ['typeOfProduct', 'kg', 'price', 'totalSum', 'byWhom', 'debt']
        widgets = {
            'typeOfProduct': forms.TextInput(attrs={'placeholder': 'Maxsulot nomi', 'class': "form-control"}),
            'kg': forms.TextInput(attrs={'placeholder': "kg", 'class': "form-control amount"}),
            'price': forms.TextInput(attrs={'placeholder': "Narxi", 'class': "form-control amount"}),
            'totalSum': forms.TextInput(attrs={'placeholder': "To'liq summasi", 'class': "form-control amount"}), 
            'byWhom': forms.TextInput(attrs={'placeholder': "Kim ?", 'class': "form-control"}),
            'debt': forms.CheckboxInput(attrs={'class': "custom-control-input"})
        }

class AgentsForm(ModelForm):
    class Meta:
        model = Agents
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nomi', 'class': "form-control"})
        }
