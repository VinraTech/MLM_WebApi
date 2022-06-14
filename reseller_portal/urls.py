from django.urls import path,include
from .views import *
# from .views import send_otp
urlpatterns = [
    # path('register_reseller/', RegisterReseller.as_view()),
    # # path('forgot_password_reseller/', ForgotPasswordReseller.as_view()),
    # path('verify_otp_reseller/', VerifyOtpReseller.as_view()),
    path('DemoApi/', DemoApi.as_view()),
]