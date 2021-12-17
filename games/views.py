import datetime

import requests
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse

from secret_santa.settings import bitly_token
from .forms import (
    CreateGameForm,
    LoginUserForm,
    RegistrationForm,
    SantaCardForm,
    UpdateGameForm,
)
from .helpers import create_santa_for_user
from .models import Santa, Game, CustomUser


def index(request):
    if request.user.is_authenticated:
        return redirect(reverse_lazy('profile'))
    return render(request, 'games/index.html')


@login_required(login_url='login')
def view_profile(request):
    user = request.user
    santa = Santa.objects.get(user=user)
    customuser = CustomUser.objects.get(username=user)
    santa_games = santa.games.filter(draw_date__gte=datetime.date.today())
    coordinator_games = Game.objects.filter(coordinator=customuser)
    form = SantaCardForm(instance=santa)
    context = {
        'santa_games': santa_games,
        'coordinator_games': coordinator_games,
        'form': form
    }
    return render(request, 'games/profile.html', context=context)


class LoginUserView(LoginView):
    template_name = 'games/login.html'
    redirect_authenticated_user = True
    form_class = LoginUserForm

    def get_success_url(self):
        return reverse_lazy('profile')


class LogoutUserView(LogoutView):
    next_page = 'index'


def register_user(request):
    if request.user and request.user.is_authenticated:
        return redirect(reverse_lazy('profile'))

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            new_user = form.save()
            create_santa_for_user(
                new_user,
                form.cleaned_data['wishlist'],
                form.cleaned_data['letter_to_santa'],
            )

            new_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
            )
            login(request, new_user)
            return redirect(reverse_lazy('profile'))

        return render(request, 'games/register_user.html', {'form': form})

    form = RegistrationForm()

    return render(request, 'games/register_user.html', {'form': form})


@login_required(login_url='login')
def update_santa_card(request):
    user = request.user
    santa_card = Santa.objects.get(user=user)
    if request.method == 'POST':
        form = SantaCardForm(request.POST, instance=santa_card)
        if form.is_valid():
            form.save()
        return redirect(reverse_lazy('profile'))

    form = SantaCardForm(instance=santa_card)
    return render(request, 'games/santa_card.html', context={'form': form})


def create_bitlink(link):
    url = 'https://api-ssl.bitly.com/v4/bitlinks'
    headers = {
        'Authorization': f'Bearer {bitly_token}'
    }
    payload = {
        'long_url': link,
        'domain': 'bit.ly'
    }
    res = requests.post(url, json=payload, headers=headers)
    return res.json()['id']


@login_required(login_url='login')
def create_game(request):
    user = request.user
    if request.method == 'POST':
        form = CreateGameForm(request.POST)

        if form.is_valid():
            new_game = form.save()
            current_page_url = request.build_absolute_uri(
                reverse('invited_person_registration', args=[new_game.pk]))
            print(current_page_url)
            bitly_url = create_bitlink(current_page_url)
            new_game.url = bitly_url
            new_game.save()

            if form.cleaned_data['is_santa']:
                santa = form.cleaned_data['coordinator'].santa
                santa.games.add(new_game)

            return redirect(reverse_lazy('profile'))

        return render(request, 'games/create_game.html', {'form': form})

    form = CreateGameForm(initial={'coordinator': user})

    return render(request, 'games/create_game.html', {'form': form})


@login_required(login_url='login')
def update_game(request, pk):
    user = request.user
    game = Game.objects.get(pk=pk)

    if game.coordinator != user:
        return redirect(reverse_lazy('profile'))

    if request.method == 'POST':
        form = UpdateGameForm(request.POST, instance=game)

        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('profile'))

        return render(request, 'games/update_game.html', {'form': form})

    form = UpdateGameForm(instance=game)

    return render(request, 'games/update_game.html', {'form': form})


def greeting_page(request):
    return render(request, 'games/greeting_page.html')


@login_required(login_url='login')
def invited_person_registration(request, pk):

    game = get_object_or_404(Game, pk=pk)
    form = UpdateGameForm(instance=game)
    santa = Santa.objects.get(user=request.user)
    santa.games.add(game)
    context = {
        'game': game,
        'form': form
    }
    return render(request, 'games/invited_person_registration.html',
                  context=context)
# else:
#     print('no')
#     return render(request, 'games/register.html')
