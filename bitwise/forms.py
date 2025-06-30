from django import forms

class NumberForm(forms.Form):
    a = forms.FloatField()
    b = forms.FloatField()
    c = forms.FloatField()
    d = forms.FloatField()
    e = forms.FloatField()