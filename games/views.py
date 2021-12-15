from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse

from games.forms import SantaCardForm


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
        return reverse('profile')


def create_santa_card(request):
    if request.method == 'POST':
        pass
    else:
        form = SantaCardForm()
        return render(request, 'games/santa_card.html', context={'form': form})
