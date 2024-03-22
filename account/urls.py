from django.urls import path
from account.views import UserLoginView, UserRegistrationView, ProfileView, UserEmailOTPLoginView, UserEmailOTPView
urlpatterns = [
       path('register/',UserRegistrationView.as_view(), name='register'),
       path('login/', UserLoginView.as_view(), name='login'),
       path('profile/', ProfileView.as_view(), name='view_profile'),
       path('otp/send/', UserEmailOTPView.as_view(), name='send_otp'),
       path('otp/login/', UserEmailOTPLoginView.as_view(), name='login_with_otp'),
]
