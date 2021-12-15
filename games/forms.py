from django import forms

from games.models import Santa


class SantaCardForm(forms.ModelForm):
    class Meta:
        model = Santa
        fields = '__all__'
