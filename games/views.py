from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import RegistrationForm, SantaCardForm


def index(request):
    return render(request, 'games/index.html')


@login_required(login_url='login')
def view_profile(request):
    user = request.user
    return render(request, 'games/profile.html')


class LoginUserView(LoginView):
    template_name = 'games/login.html'
    redirect_authenticated_user = True

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
            new_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
            )
            login(request, new_user)
            return redirect(reverse_lazy('profile'))

        return render(request, 'games/register_user.html', {'form': form})

    form = RegistrationForm()

    return render(request, 'games/register_user.html', {'form': form})


def create_santa_card(request):
    if request.method == 'POST':
        pass
    else:
        form = SantaCardForm()
        return render(request, 'games/santa_card.html', context={'form': form})
