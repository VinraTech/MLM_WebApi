from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from registration.serializers import *

from registration.models import Customer
# Create your views here.

class CustomerApprove(APIView):
    def put(self, request):
        is_approved=request.data.get('is_approved', None)
        ids=request.data.getlist('ids')
        if not ids or is_approved is None:
            return Response({"status": "Error", "reason": 'Please provide valid Customer ID and approved flag!'}, status=status.HTTP_400_BAD_REQUEST)
        if Customer.objects.filter(id__in=ids).exists():
            Customer.objects.filter(id__in=ids).update(is_approved=is_approved.capitalize())
            return Response({'status':'Success','msg':'Customer approved successfully!'}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "Error", "reason": "Please provide valid customer id!"}, status=status.HTTP_400_BAD_REQUEST)


class CustomerUpdate(APIView):
    def put(self, request):
        pk=request.data.get('pk',None)
        if not pk or not Customer.objects.filter(id=pk).exists():
            return Response({"status": "Error", "reason": 'Please provide valid Customer ID!'}, status=status.HTTP_400_BAD_REQUEST)
        
        qs = Customer.objects.get(id=pk)
        serializer = CustomerSerializer(qs, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()

            if request.data.get('address_line_1') or request.data.get('address_line_2') or request.data.get('postal_code') or request.data.get('city') or request.data.get('country'):
                if not request.data.get('address_line_1') or not request.data.get('address_line_2') or not request.data.get('postal_code') or not request.data.get('city') or not request.data.get('country'):
                    return Response({"status":"Error", "msg":"Please provide all address details"}, status=status.HTTP_400_BAD_REQUEST)

                if not qs.addresses.filter(address_line_1=request.data.get('address_line_1'), address_line_2=request.data.get('address_line_2'), pincode=request.data.get('postal_code'), city=request.data.get('city'), country=request.data.get('country')):

                    qs.addresses.clear()
                    addrss = CustomerAddress.objects.create(address_line_1=request.data.get('address_line_1'), address_line_2=request.data.get('address_line_2'), pincode=request.data.get('postal_code'), city=request.data.get('city'), country=request.data.get('country'))
                    qs.addresses.add(addrss)

                return Response({'status':'Success','msg':'Customer updated successfully!'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'status':'Success','msg':'Customer updated successfully!'}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "Error", "reason": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)