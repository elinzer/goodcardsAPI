from django.urls import path
from user.api.views import SignUpView, LoginView

urlpatterns = [
    path('signup', SignUpView.signup, name='sign-up'),
    path('login', LoginView.login, name='login')
]