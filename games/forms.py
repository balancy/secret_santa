from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from games.models import CustomUser, Santa


class FormPrettifyFieldsMixin(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, obj in self.fields.items():
            obj.widget.attrs['class'] = f'form-control'
            obj.widget.attrs['id'] = name


class SantaCardForm(forms.ModelForm):
    class Meta:
        model = Santa
        fields = ['wishlist', 'letter_to_santa']


class RegistrationForm(UserCreationForm, FormPrettifyFieldsMixin):
    email = forms.EmailField(required=True)

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
