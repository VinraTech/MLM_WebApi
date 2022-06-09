
from django.urls import path
# from rest_framework.authtoken import views
from .views import *

urlpatterns = [
    # path('register/', RegisterUser.as_view()),
    # path('login/', views.obtain_auth_token, name='auth-token'),
    
    path('login/', CustomObtainAuthToken.as_view(), name='auth-token'),
    path('register_customer/', RegisterCustomer.as_view()),
    path('forgot_password/', ForgotPassword.as_view(), name='forgotpassword'),
    path('reset_password/', ResetPassword.as_view(), name='resetpassword'),
]