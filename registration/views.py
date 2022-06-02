

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

class RegisterUser(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = User(
                email=request.data['email'],
                # username=request.data['username'],
                username=request.data['email'],
                first_name=request.data['first_name'],
                last_name=request.data['last_name'],
            )
            user.set_password(request.data['password'])
            user.save()
            
            if 'groups' in request.data.keys():
                group=Group.objects.get(id=int(request.data['groups']))
                user.groups.add(group)
            else:
                group=Group.objects.get(name='Staff')
                user.groups.add(group)

            return Response({'status':'Success','msg':'Registration successful', 'user': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "Error", "reason": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class RegisterCustomer(APIView):
    def post(self, request):
        if request.data['password'] != request.data['confirm_password']:
            return Response({"status": "Error", 'reason':'Passwords do not match!'}, status=status.HTTP_400_BAD_REQUEST)

        user_serializer = UserSerializer(data={
            # 'username':request.data['username'],
            'username':request.data['email'],
            'email':request.data['email'], 
            'password':request.data['password'],
        })
        customer_serializer = CustomerSerializer(data={
            'nationality':request.data['nationality'],
            'gender':request.data['gender'],
            'dob':request.data['dob'],
            'mobile_no':request.data['mobile_no'],
            'full_name':request.data['full_name'],
            'email':request.data['email'],
            'city':request.data['city'],
        
        })

        
        if user_serializer.is_valid() and customer_serializer.is_valid():
            user_serializer.save()
            u = User.objects.get(id=user_serializer.data['id'])
            u.set_password(request.data['password'])
            u.save()
            customer_serializer.save(user=u)
            return Response({'status':'Success','msg':'Registration successful', 'user': user_serializer.data, 'customer':customer_serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "Error: Please Provide Valid and Unique Details"}, status=status.HTTP_400_BAD_REQUEST)
            # return Response({"status": "Error",  "user_reason":  user_serializer.errors, 'customer_reason':customer_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class ForgotPassword(APIView):
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


