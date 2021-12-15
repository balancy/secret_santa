from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse


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


class LogoutUserView(LogoutView):
    next_page = 'index'
