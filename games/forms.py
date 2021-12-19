from datetime import date, timedelta

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

from games.models import CustomUser, Game, Santa, Exclusion


class FormPrettifyFieldsMixin(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, obj in self.fields.items():
            obj.widget.attrs['class'] = f'form-control'
            obj.widget.attrs['id'] = name


class SantaCardForm(forms.ModelForm, FormPrettifyFieldsMixin):
    class Meta:
        model = Santa
        fields = ('wishlist', 'letter_to_santa')


class UpdateUserForm(forms.ModelForm, FormPrettifyFieldsMixin):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name')


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
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class LoginUserForm(AuthenticationForm, FormPrettifyFieldsMixin):
    class Meta:
        fields = ('username', 'password')


class CreateGameForm(forms.ModelForm, FormPrettifyFieldsMixin):
    is_santa = forms.BooleanField(
        required=False,
        label='Тоже являюсь участником игры',
    )

    class Meta:
        model = Game
        fields = ('name', 'coordinator', 'max_price', 'draw_date', 'gift_date')
        widgets = {
            'coordinator': forms.HiddenInput(),
            'draw_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'value': date.today() + timedelta(weeks=1),
                },
                format=('%Y-%m-%d'),
            ),
            'gift_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'value': date.today() + timedelta(weeks=2),
                },
                format=('%Y-%m-%d'),
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        draw_date = cleaned_data.get('draw_date')
        gift_date = cleaned_data.get('gift_date')

        if draw_date and gift_date:
            if draw_date <= date.today():
                raise forms.ValidationError(
                    _('Дата жеребьевки должна быть позже сегодняшнего дня')
                )

        if gift_date <= draw_date:
            raise forms.ValidationError(
                _('Дата отправки подарка должна быть позже даты жеребьевки')
            )

        return cleaned_data


class UpdateGameForm(forms.ModelForm, FormPrettifyFieldsMixin):
    class Meta:
        model = Game
        fields = ('name', 'max_price', 'draw_date', 'gift_date')
        widgets = {
            'draw_date': forms.DateInput(
                attrs={'type': 'date'},
                format=('%Y-%m-%d'),
            ),
            'gift_date': forms.DateInput(
                attrs={'type': 'date'},
                format=('%Y-%m-%d'),
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        draw_date = cleaned_data.get('draw_date')
        gift_date = cleaned_data.get('gift_date')

        if draw_date and gift_date:
            if draw_date <= date.today():
                raise forms.ValidationError(
                    _('Дата жеребьевки должна быть позже сегодняшнего дня')
                )

        if gift_date <= draw_date:
            raise forms.ValidationError(
                _('Дата отправки подарка должна быть позже даты жеребьевки')
            )

        return cleaned_data


class ExclusionsForm(forms.ModelForm, FormPrettifyFieldsMixin):
    class Meta:
        model = Exclusion
        fields = ('game', 'giver', 'receiver')
        widgets = {
            'game': forms.HiddenInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        giver = cleaned_data.get('giver')
        receiver = cleaned_data.get('receiver')

        if giver == receiver:
            raise forms.ValidationError(
                _('Даритель и получатель не должны совпадать!')
            )

        return cleaned_data
