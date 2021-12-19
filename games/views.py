import datetime
import random

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse

from .forms import (
    CreateGameForm,
    LoginUserForm,
    RegistrationForm,
    SantaCardForm,
    UpdateGameForm,
    UpdateUserForm,
    ExclusionsForm,
)
from .helpers import (
    create_bitlink,
    create_santa_for_user,
    hash_value,
    is_hash_correct,
)
from .models import Santa, Game, Exclusion


def index(request):
    santas = [santa for santa in Santa.objects.all()]
    random.shuffle(santas)
    context = {'santas': santas[:3]}
    return render(request, 'games/index.html', context=context)


@login_required(login_url='login')
def view_profile(request):
    user = request.user
    santa = user.santa
    santa_games = santa.games.filter(draw_date__gte=datetime.date.today())
    coordinator_games = user.games.all()

    context = {
        'user': user,
        'santa_games': santa_games,
        'coordinator_games': coordinator_games,
        'santa': santa,
    }
    return render(request, 'games/profile.html', context=context)


def login_user(request):
    if request.user and request.user.is_authenticated:
        return redirect(reverse_lazy('profile'))

    if request.method == 'POST':
        form = LoginUserForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get('password')

            new_user = authenticate(username=username, password=password)
            login(request, new_user)

            if not Santa.objects.filter(user=new_user).first():
                create_santa_for_user(new_user)

            if game_pk := request.session.get('game_pk'):
                santa = new_user.santa
                game = Game.objects.get(pk=game_pk)
                santa.games.add(game)

            return redirect(reverse_lazy('profile'))

        return render(request, 'games/login.html', context={'form': form})

    form = LoginUserForm()
    return render(request, 'games/login.html', context={'form': form})


class LogoutUserView(LogoutView):
    next_page = 'index'


def invite_user(request, hashed_pk=None):
    if is_hash_correct(hashed_pk):
        _, pk = hashed_pk.split('_')
        game = Game.objects.filter(pk=pk).first()

        request.session['game_pk'] = pk
    else:
        game = None

    return render(
        request, 'games/invite_user.html', {'game': game, 'user': request.user}
    )


@login_required(login_url='login')
def enter_game(request):
    santa = request.user.santa
    game = Game.objects.get(pk=request.session['game_pk'])
    santa.games.add(game)

    return redirect(reverse_lazy('profile'))


def register_user(request):
    if request.user and request.user.is_authenticated:
        return redirect(reverse_lazy('profile'))

    game_pk = request.session.get('game_pk')

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

            if game_pk:
                santa = request.user.santa
                game = Game.objects.get(pk=game_pk)
                santa.games.add(game)

            return redirect(reverse_lazy('profile'))

        return render(
            request,
            'games/register_user.html',
            {'form': form, 'is_invited': game_pk},
        )

    form = RegistrationForm()

    return render(
        request,
        'games/register_user.html',
        {'form': form, 'is_invited': game_pk},
    )


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


@login_required(login_url='login')
def update_user(request):
    user = request.user
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
        return redirect(reverse_lazy('profile'))

    form = UpdateUserForm(instance=user)
    return render(request, 'games/update_user.html', context={'form': form})


@login_required(login_url='login')
def create_game(request):
    user = request.user
    if request.method == 'POST':
        form = CreateGameForm(request.POST)
        if form.is_valid():
            new_game = form.save()

            invite_url = request.build_absolute_uri(
                reverse('invite_user', args=[hash_value(new_game.pk)])
            )
            new_game.url = create_bitlink(invite_url)
            new_game.save()

            if form.cleaned_data['is_santa']:
                santa = form.cleaned_data['coordinator'].santa
                santa.games.add(new_game)

            return redirect(reverse_lazy('profile'))

        return render(request, 'games/create_game.html', {'form': form})

    form = CreateGameForm(initial={'coordinator': user})

    return render(request, 'games/create_game.html', {'form': form})


@login_required(login_url='login')
def show_game(request, pk):
    game = Game.objects.filter(pk=pk).first()

    if not game:
        redirect(reverse_lazy('profile'))

    return render(request, 'games/show_game.html', {'game': game})


@login_required(login_url='login')
def update_game(request, pk):
    user = request.user
    game = Game.objects.filter(pk=pk).first()

    if not game:
        redirect(reverse_lazy('profile'))

    if game.coordinator != user:
        return redirect(reverse_lazy('profile'))

    santas = Santa.objects.filter(games=game)
    exclusions = Exclusion.objects.filter(game=game)

    if request.method == 'POST':
        form = UpdateGameForm(request.POST, instance=game)

        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('profile'))

        return render(
            request,
            'games/update_game.html',
            {'form': form, 'santas': santas, 'game': game},
        )

    form = UpdateGameForm(instance=game)

    return render(
        request,
        'games/update_game.html',
        {
            'form': form,
            'santas': santas,
            'game': game,
            'exclusions': exclusions,
        },
    )


@login_required(login_url='login')
def exclusions(request, pk):
    game = Game.objects.filter(pk=pk).first()
    santas = Santa.objects.filter(games=game)

    if not game:
        return redirect(reverse_lazy('update_game', kwargs={'pk': pk}))

    if request.method == 'POST':
        form = ExclusionsForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect(reverse_lazy('update_game', kwargs={'pk': pk}))

        return render(
            request,
            'games/exclusions.html',
            {'form': form, 'santas': santas},
        )

    form = ExclusionsForm(initial={'game': game})

    return render(
        request,
        'games/exclusions.html',
        {
            'form': form,
            'santas': santas,
        },
    )


@login_required(login_url='login')
def remove_santa_from_game(request, game_pk, santa_pk):
    user = request.user
    game = Game.objects.get(pk=game_pk)

    if game.coordinator != user:
        return redirect(reverse_lazy('profile'))

    santa = Santa.objects.get(pk=santa_pk)
    santa.games.remove(game)

    return redirect(reverse_lazy('update_game', kwargs={'pk': game_pk}))


@login_required(login_url='login')
def remove_exclusion_from_game(request, game_pk, exclusion_pk):
    exclusion = Exclusion.objects.get(pk=exclusion_pk)
    exclusion.delete()

    return redirect(reverse_lazy('update_game', kwargs={'pk': game_pk}))


def greeting_page(request):
    return render(request, 'games/greeting_page.html')


def congrat_page(request):
    return render(request, 'games/congrat_page.html')
