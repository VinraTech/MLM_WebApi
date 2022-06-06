import email
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from registration.serializers import *
from .serializers import *
from registration.email import send_forgot_password_mail
from random import randrange
from twilio.rest import Client
def send_otp(mobile=None,otp=None):
    # account_sid='AC494b0549e21944244dc76e673cd5bdb1'
    # auth_token='74fcd6a8087731d5b94027d491899546'
    # client=Client(account_sid,auth_token)
    # message=client.messages.create(
    #                                 body=f'The otp is -{otp}',
    #                                 from_='+14405381381',
    #                                 to='+919759525301'
    #                             )
    print('Your otp is:', otp)
    print('Your mobile is:', mobile)
    return True


class RegisterReseller(APIView):
    def post(self, request):
        # if request.data['password'] != request.data['confirm_password']:
        #     return Response({"status": "Error", 'reason':'Passwords do not match!'}, status=status.HTTP_400_BAD_REQUEST)

        user_serializer = UserSerializer(data={
            'username':request.data['email'],
            'email':request.data['email'], 
            'password':request.data['password'],
        })
        reseller_serializer = ResellerSerializer(data={
            'mobile_no':request.data['mobile_no'],
            'full_name':request.data['full_name'],
        })

        user_errors = user_serializer.is_valid() 
        customer_errors = reseller_serializer.is_valid()

        if user_errors and customer_errors:
            #user_serializer.save(is_active=False)
            user_serializer.save()
            u = User.objects.get(id=user_serializer.data.get('id'))
            u.set_password(request.data.get('password'))
            u.save()
            reseller_serializer.save(user=u)
            otp = randrange(100000, 999999)
            mob_otp_send = send_otp(mobile=request.data['mobile_no'], otp=otp)
            
            return Response({'status':'Success','msg':'Registration successful', 'user': user_serializer.data, 'reseller':reseller_serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "Error: Please Provide Valid and Unique Details", "errors":dict(user_serializer.errors, **reseller_serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordReseller(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self,request):
        email = request.data.get('email', None)
        # if Reseller.objects.filter(email=email).exists():
        if Reseller.objects.filter(user__email=email).exists():
            reseller_obj = Reseller.objects.get(user__email=email)
            otp = randrange(100000, 999999)
            send_forgot_password_mail(reseller_obj.user.email, otp)

            rp_otp = ResetPasswordOTP.objects.create(user=reseller_obj.user, otp=otp)
            if ResetPasswordOTP.objects.filter(user=reseller_obj.user).exclude(id=rp_otp.id).exists():
                rp_otp_obj = ResetPasswordOTP.objects.filter(user=reseller_obj.user).exclude(id=rp_otp.id)
                for x in rp_otp_obj:
                    x.delete()
            return Response({"status": "OTP sent on email successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "Error", 'reason':'Email not registered with us!'}, status=status.HTTP_400_BAD_REQUEST)





        
