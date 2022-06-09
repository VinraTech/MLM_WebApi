from lib2to3.pgen2 import token
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
from .email import send_forgot_password_mail
from random import randrange



from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user_obj = UserSerializer(User.objects.get(id=token.user_id), many=False).data
        return Response({'token': token.key, 'user': user_obj})

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


class RegisterCustomer(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        # if request.data.get('password') != request.data.get('confirm_password'):
        #     return Response({"status": "Error", 'reason':'Passwords do not match!'}, status=status.HTTP_400_BAD_REQUEST)
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
            user_serializer.save()
            u = User.objects.get(id=user_serializer.data.get('id'))
            u.set_password(request.data.get('password'))
            u.save()
            customer_serializer.save(user=u)
            return Response({'status':'Success','msg':'Registration successful', 'user': user_serializer.data, 'customer':customer_serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "Error: Please Provide Valid and Unique Details", "errors":dict(user_serializer.errors, **customer_serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)




class ForgotPassword(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self,request):
        email = request.data.get('email', None)
        if Customer.objects.filter(email=email).exists():
            customer_obj = Customer.objects.get(email=email)
            otp = randrange(100000, 999999)
            send_forgot_password_mail(customer_obj.email, otp)

            rp_otp = ResetPasswordOTP.objects.create(user=customer_obj.user, otp=otp)
            if ResetPasswordOTP.objects.filter(user=customer_obj.user).exclude(id=rp_otp.id).exists():
                rp_otp_obj = ResetPasswordOTP.objects.filter(user=customer_obj.user).exclude(id=rp_otp.id)
                for x in rp_otp_obj:
                    x.delete()
            return Response({"status": "OTP sent on email successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "Error", 'reason':'Email not registered!'}, status=status.HTTP_400_BAD_REQUEST)


class ResetPassword(APIView):
    authentication_classes = []
    permission_classes = []
    
    def post(self, request):
        otp = request.data.get('otp', None)
        password = request.data.get('password', None)
        confirm_password = request.data.get('confirm_password', None)
        user = request.data.get('username', None)
        if user:
            user = User.objects.get(username=user)
        
        if not otp or not user or not password or not confirm_password:
            return Response({'status':'Error', 'reason':'Please provide all fields!'})

        if password != confirm_password:
            return Response({'status':'Error', 'reason':'Passwords do not match!'})

        if ResetPasswordOTP.objects.filter(user=user, otp=otp).exists():
            user.set_password(password)
            user.save()
            ResetPasswordOTP.objects.filter(user=user, otp=otp).last().delete()
            return Response({'status':'Success','reason':'Password changed successfully!'}, status=status.HTTP_200_OK)
        else:
            return Response({'status':'Error', 'reason':'Please enter correct OTP!'}, status=status.HTTP_400_BAD_REQUEST)


