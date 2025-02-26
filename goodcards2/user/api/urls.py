from django.urls import path
from user.api.views import SignUpView

urlpatterns = [
    path('signup', SignUpView.signup, name='sign-up')
]