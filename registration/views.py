from tokenize import group

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from django.contrib.auth.models import User
from .models import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Group
#from .email import send_forgot_password_mail
from random import randrange

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

import django.contrib.auth.password_validation as validators
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from .validators import GenerateCustomerID

import uuid
import datetime 

import pytz

# class RegisterUser(APIView):
#     # authentication_classes = [TokenAuthentication]
#     # permission_classes = [IsAuthenticated]
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)

#         if serializer.is_valid():
#             user = User(
#                 email=request.data.get('email'),  
#                 username=request.data.get('email'),
#                 first_name=request.data.get('first_name'),
#                 last_name=request.data.get('last_name'),
#             )
#             user.set_password(request.data.get('password')),
#             user.save()
            
#             if 'groups' in request.data.keys():
#                 group=Group.objects.get(id=int(request.data.get('groups')))
#                 user.groups.add(group)
#             else:
#                 group=Group.objects.get(name='Staff')
#                 user.groups.add(group)

#             return Response({'status':'Success','msg':'Registration successful', 'user': serializer.data}, status=status.HTTP_200_OK)
#         else:
#             return Response({"status": "Error", "reason": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

def ValidateNewPassword(password, confirm_password=None):
    validations = dict()
    if confirm_password and password != confirm_password:
        validations['password'] = ["Passwords do not match!"]
        return validations

    try:
        validators.validate_password(password=password)
    except ValidationError as e:
        validations['password'] = e.messages
    return validations

class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user_obj = UserSerializer(User.objects.get(id=token.user_id), many=False).data
        return Response({'token': token.key, 'user': user_obj})

class RegisterCustomer(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        is_approved = request.GET.get('is_approved', None)

        if is_approved not in ['True', 'False', 'true', 'false', None]:
            return Response({'status':'Error', 'msg':'Please send correct filter value!'})
    
        if is_approved is not None:
            ia = is_approved.capitalize()
            qs = Customer.objects.filter(is_approved=ia)
            serializer = CustomerSerializer(qs, many=True)
        else:
            qs = Customer.objects.all()
            serializer = CustomerSerializer(qs, many=True)

        if request.GET.get('id'):
            if Customer.objects.filter(id=request.GET.get('id')).exists():
                qs = Customer.objects.get(id=request.GET.get('id'))
                serializer = CustomerSerializer(qs, many=False)
            else:
                return Response({"status":"Error","reason":"Please Provide valid id!"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.data)

    def post(self, request):
        errors = ValidateNewPassword(request.data.get('password'), request.data.get('confirm_password'))

        if errors:
            return Response({"status": "Error", "errors":errors}, status=status.HTTP_400_BAD_REQUEST)

        if not request.data.get('full_name'):
            return Response({'status':'Error','reason':'Please Enter fullname!'})
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
        customer_serializer = CustomerSerializer(data={
            'customer_id':GenerateCustomerID(),
            'nationality':request.data.get('nationality'),
            'gender':request.data.get('gender'),
            'dob':request.data.get('dob'),
            'mobile_no':request.data.get('mobile_no'),
            'full_name':request.data.get('full_name'),
            'email':request.data.get('email'),
            'city':request.data.get('city')
        })

        user_errors = user_serializer.is_valid()
        customer_errors = customer_serializer.is_valid()

        if user_errors and customer_errors:
            user_serializer.save(is_active=False)
            u = User.objects.get(id=user_serializer.data.get('id'))
            u.set_password(request.data.get('password'))
            u.save()
            customer_serializer.save(user=u)
            otp = randrange(100000, 999999)
            # mob_otp_send = send_otp(mobile=request.data.get('mobile_no'), otp=otp)
            rp_otp = ResetPasswordOTP.objects.create(user=u,otp=otp)
            if ResetPasswordOTP.objects.filter(user=u).exclude(id=rp_otp.id).exists():
                rp_otp_obj = ResetPasswordOTP.objects.filter(user=u).exclude(id=rp_otp.id)
                for x in rp_otp_obj:
                    x.delete()
            return Response({'status':'Success','msg':'Otp send successful', 'user': user_serializer.data, 'customer':customer_serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "Error: Please Provide Valid and Unique Details", "errors":dict(user_serializer.errors, **customer_serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)

class VerifyOtpCustomer(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self,request):
        if ResetPasswordOTP.objects.filter(user__username=request.data.get('username')).exists():
            rp_otp_obj = ResetPasswordOTP.objects.get(user__username=request.data.get('username'))
            if int(rp_otp_obj.otp) == int(request.data.get('otp')):
                customer_obj = Customer.objects.get(user__username=request.data.get('username'))
                customer_obj.user.is_active = True
                customer_obj.user.save()
                if User.objects.filter(username=request.data.get('username')).exists:
                    user_obj = User.objects.filter(username=request.data.get('username')).first()
                    user_obj = UserSerializer(user_obj, many=False).data
                    return Response({"status": "Success", 'reason':'Otp verified successfully!','user': user_obj}, status=status.HTTP_200_OK)
                else:
                    return Response({"status": "Success", 'reason':'Otp verified successfully!'}, status=status.HTTP_200_OK)
            else:
                return Response({'status':'Please enter correct otp!'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"status": "Error", 'reason':'Please enter correct username!'}, status=status.HTTP_400_BAD_REQUEST)

class ForgotPassword(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self,request):
        email = request.data.get('email', None)
        if Customer.objects.filter(email=email).exists():
            customer_obj = Customer.objects.get(email=email)
            token = uuid.uuid4()
            # send_forgot_password_mail(customer_obj.email, token)

            expired_time = datetime.datetime.now() + datetime.timedelta(hours=24)
            rp_obj = ResetPasswordOTP.objects.create(user=customer_obj.user, token=token, expired_on=expired_time)
            if ResetPasswordOTP.objects.filter(user=customer_obj.user).exclude(id=rp_obj.id).exists():
                rp_obj = ResetPasswordOTP.objects.filter(user=customer_obj.user).exclude(id=rp_obj.id)
                for x in rp_obj:
                    x.delete()
            return Response({"status": "Link sent on email successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "Error", 'reason':'Email not registered!'}, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordToken(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self,request,token=None):
        if ResetPasswordOTP.objects.filter(token=token).exists():
            rp_obj = ResetPasswordOTP.objects.filter(token=token).first()
            utc_now = pytz.UTC.localize(datetime.datetime.now())

            if rp_obj.expired_on > utc_now:
                serializer = UserSerializer(rp_obj.user, many=False)
                return Response(serializer.data)
            else:
                return Response({'status':'Error','msg':'Token Expired!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status':'Error','msg':'Token Expired!'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):

        password = request.data.get('password', None)
        confirm_password = request.data.get('confirm_password', None)
        user = request.data.get('username', None)

        if user:
            user = User.objects.get(username=user)
        
        if not user or not password or not confirm_password:
            return Response({'status':'Error', 'reason':'Please provide all fields!'})

        if password != confirm_password:
            return Response({'status':'Error', 'reason':'Passwords do not match!'})

        if ResetPasswordOTP.objects.filter(user=user).exists():
            user.set_password(password)
            user.save()
            ResetPasswordOTP.objects.filter(user=user).last().delete()
            return Response({'status':'Success','reason':'Password changed successfully!'}, status=status.HTTP_200_OK)
        else:
            return Response({'status':'Error', 'reason':'Please enter correct username!'}, status=status.HTTP_400_BAD_REQUEST)

class ChangePassword(APIView):
    def post(self, request):
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        confirm_new_password = request.data.get('confirm_new_password')
        username = request.data.get('username')

        if not username or not current_password or not new_password or not confirm_new_password:
            return Response({'status':'Error', 'reason':'Please provide all fields!'})

        pwd_errors = ValidateNewPassword(new_password, confirm_new_password)
        if pwd_errors:
            return Response({"status": "Error", "errors":pwd_errors}, status=status.HTTP_400_BAD_REQUEST)

        if not User.objects.filter(username=username).exists():
            return Response({'status':'Error', 'reason':'User with this username do not exists!'})

        user = User.objects.get(username=username)

        if not check_password(current_password, user.password):
            return Response({"status": "Error", "errors":'Current Password is incorrect!'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({'status':'Success', 'msg':'Password changed Successfully!'}, status=status.HTTP_200_OK)
