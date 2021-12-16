from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from games.models import CustomUser, Game, Santa


class FormPrettifyFieldsMixin(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, obj in self.fields.items():
            obj.widget.attrs['class'] = f'form-control'
            obj.widget.attrs['id'] = name


class SantaCardForm(forms.ModelForm, FormPrettifyFieldsMixin):
    class Meta:
        model = Santa
        fields = ['wishlist', 'letter_to_santa']


class RegistrationForm(UserCreationForm, FormPrettifyFieldsMixin):
    email = forms.EmailField(required=True)
    wishlist = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3}),
        label='Список желаемого',
    )
    letter_to_santa = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3}),
        label='Письмо Санте',
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class LoginUserForm(AuthenticationForm, FormPrettifyFieldsMixin):
    pass


class CreateGameForm(forms.ModelForm, FormPrettifyFieldsMixin):
    class Meta:
        model = Game
        fields = ('name', 'coordinator', 'max_price', 'draw_date', 'gift_date')
        widgets = {
            'coordinator': forms.HiddenInput(),
        }
