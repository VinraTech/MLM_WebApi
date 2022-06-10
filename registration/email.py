
from django.core.mail import send_mail
from django.conf import settings


def send_forgot_password_mail(email,token):
    subject = 'Forgot password email'
    message = f'Hi, The link to reset your password is http://127.0.0.1:8000/reset_pass_link/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject, message, email_from, recipient_list)
    return True

# def send_otp(mobile=None,otp=None):
#     # account_sid='AC494b0549e21944244dc76e673cd5bdb1'
#     # auth_token='74fcd6a8087731d5b94027d491899546'
#     # client=Client(account_sid,auth_token)
#     # message=client.messages.create(
#     #                                 body=f'The otp is -{otp}',
#     #                                 from_='+14405381381',
#     #                                 to='+919759525301'
#     #                             )
#     print('Your otp is:', otp)
#     print('Your mobile is:', mobile)

#     return True