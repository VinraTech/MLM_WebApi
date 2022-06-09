import email
import re
from django.conf import settings
from django.http import HttpResponse
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
    def get(self, request):
        is_approved = request.GET.get('is_approved', None)

        if is_approved not in ['True', 'False', 'true', 'false', None]:
            return Response({'status':'Error', 'msg':'Please send correct filter value!'})
    
        if is_approved is not None:
            ia = is_approved.capitalize()
            qs = Reseller.objects.filter(is_approved=ia)
        else:
            qs = Reseller.objects.all()
        
        serializer = ResellerSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        # if request.data['password'] != request.data['confirm_password']:
        #     return Response({"status": "Error", 'reason':'Passwords do not match!'}, status=status.HTTP_400_BAD_REQUEST)

        fullname = request.data.get('full_name')
        firstname = fullname.strip().split(' ')[0]
        lastname = ' '.join((fullname + ' ').split(' ')[1:]).strip()

        user_serializer = UserSerializer(data={
            'username':request.data.get('email'),
            'email':request.data.get('email'), 
            'password':request.data.get('password'),
            'first_name':firstname,
            'last_name':lastname,
        })
        reseller_serializer = ResellerSerializer(data={
            'mobile_no':request.data.get('mobile_no'),
            'full_name':request.data.get('full_name'),
        })

        user_errors = user_serializer.is_valid() 
        customer_errors = reseller_serializer.is_valid()

        if user_errors and customer_errors:
            user_serializer.save(is_active=False)
            u = User.objects.get(id=user_serializer.data.get('id'))
            psw = request.data.get('password')
            u.set_password(psw)
            u.save()
            reseller_serializer.save(user=u)
            otp = randrange(100000, 999999)
            mob_otp_send = send_otp(mobile=request.data.get('mobile_no'), otp=otp)
            rp_otp = ResetPasswordOTP.objects.create(user=u,otp=otp)
            if ResetPasswordOTP.objects.filter(user=u).exclude(id=rp_otp.id).exists():
                rp_otp_obj = ResetPasswordOTP.objects.filter(user=u).exclude(id=rp_otp.id)
                for x in rp_otp_obj:
                    x.delete()
            
            return Response({'status':'Success','msg':'Otp sent on mobile successfully!', 'user': user_serializer.data, 'reseller':reseller_serializer.data}, status=status.HTTP_200_OK)
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

class VerifyOtpReseller(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self,request):
        if ResetPasswordOTP.objects.filter(user__username=request.data.get('username')).exists():
            rp_otp_obj = ResetPasswordOTP.objects.get(user__username=request.data.get('username'))
            print('real_otp:',rp_otp_obj.otp)
            print('provided_otp',request.data.get('otp'))
            if int(rp_otp_obj.otp) == int(request.data.get('otp')):
                reseller_obj = Reseller.objects.get(user__username=request.data.get('username'))
                reseller_obj.user.is_active = True
                reseller_obj.user.save()
                return Response({"status": "Success", 'reason':'Otp verified successfully!'}, status=status.HTTP_200_OK)
            else:
                return Response({'status':'Please enter correct otp!'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"status": "Error", 'reason':'Please enter correct username!'}, status=status.HTTP_400_BAD_REQUEST)
