from django.urls import path
from account.views import UserLoginView, UserRegistrationView, TestView
urlpatterns = [
       path('register/',UserRegistrationView.as_view(), name='register'),
       path('login/', UserLoginView.as_view(), name='login'),
       path('test/', TestView.as_view(), name='test')
]
