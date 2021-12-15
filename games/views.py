from django.http.response import HttpResponse
from django.contrib.auth.views import LoginView
from django.urls import reverse


def view_profile(request):
    return HttpResponse(f'Salut, {request.user}')


class LoginUserView(LoginView):
    template_name = 'games/login.html'

    def get_success_url(self):
        return reverse('profile')
