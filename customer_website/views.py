from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from registration.models import *
from registration.serializers import *
import json

class ProductImageAPI(APIView):
    def get(self, request, pk=None):
        qs = ProductImages.objects.get(id=pk)
        serializer = ProductImagesSerializer(qs, many=False)
        return Response(serializer.data)

class CustomerAddressAPI(APIView):
    def get(self, request, pk=None):
        many = False
        if pk and CustomerAddress.objects.filter(id=pk).exists():
            qs = CustomerAddress.objects.get(id=pk)
        else:
            many = True
            if not request.data.get('customer') or not Customer.objects.filter(id=request.data.get('customer')).exists():
                return Response({"status": "Error", "reason": 'Please provide valid Customer ID!'}, status=status.HTTP_400_BAD_REQUEST)

            qs = Customer.objects.get(id=request.data.get('customer')).addresses.all()

        serializer = CustomerAddressSerializer(qs, many=many)
        return Response(serializer.data)

    def post(self, request):
        customer_id = request.data.get('customer')
        if not customer_id or not Customer.objects.filter(id=customer_id).exists():
            return Response({"status": "Error", "reason": 'Please provide valid Customer ID!'}, status=status.HTTP_400_BAD_REQUEST)

        customer = Customer.objects.get(id=customer_id)

        serializer = CustomerAddressSerializer(data={
            'is_primary':request.data.get('is_primary', False),
            'address_line_1':request.data.get('address_line_1'),
            'address_line_2':request.data.get('address_line_2'),
            'city':request.data.get('city'),
            'state':request.data.get('state'),
            'pincode':request.data.get('pincode'),
            'mobile_no':request.data.get('mobile_no'),
        })

        if serializer.is_valid():
            add_obj = serializer.save()
            customer.addresses.add(add_obj)
            return Response({'status':'Success','msg':'Customer address successfully added', 'data':serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "Error", "reason": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk=None):
        if not pk or not CustomerAddress.objects.filter(id=pk).exists():
            return Response({"status": "Error", "reason": 'Please provide valid Address ID!'}, status=status.HTTP_400_BAD_REQUEST)
        
        qs = CustomerAddress.objects.get(id=pk)

        serializer = CustomerAddressSerializer(qs, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'status':'Success','msg':'Customer address Updated successfully!', 'data':serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "Error", "reason": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if not pk or not CustomerAddress.objects.filter(id=pk).exists():
            return Response({"status": "Error", "reason": 'Please provide valid Address ID!'}, status=status.HTTP_400_BAD_REQUEST)
        
        CustomerAddress.objects.get(id=pk).delete()
        return Response({'status':'Success','msg':'Customer address Deleted successfully!'}, status=status.HTTP_200_OK)

class ProductsAPI(APIView):
    def get(self, request, pk=None):
        if pk:
            qs = Product.objects.filter(id=pk)
        else:
            qs = Product.objects.all()

        serializer = ProductSerializer(qs, many=True, context={'request':request})
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data={
            'product_id':request.data.get('product_id'),
            'name':request.data.get('name'),
            'category':request.data.get('category'),
            'description':request.data.get('description'),
            'price':request.data.get('price'),
            'discounted_price':request.data.get('discounted_price'),
        })
        

        if serializer.is_valid():
            product = serializer.save()

            if request.data.getlist('colors'):
                for x in request.data.getlist('colors'):
                    if ProductColors.objects.filter(color_name=x).exists():
                        pc = ProductColors.objects.filter(color_name=x).first()
                    else:
                        pc = ProductColors.objects.create(color_name=x)
                    product.colors.add(pc)

            if request.FILES.getlist('images'):
                for x in request.FILES.getlist('images'):
                    product.images.add(ProductImages.objects.create(image=x))

            return Response({'status':'Success','msg':'Product successfully added'}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "Error", "reason": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        if not pk or not Product.objects.filter(id=pk).exists():
            return Response({"status": "Error", "reason": 'Please provide valid Product ID!'}, status=status.HTTP_400_BAD_REQUEST)
        
        qs = Product.objects.get(id=pk)

        serializer = ProductSerializer(qs, data=request.data, partial=True)
        
        if serializer.is_valid():
            product = serializer.save()

            if request.data.getlist('colors'):
                product.colors.clear()
                for x in request.data.getlist('colors'):
                    if ProductColors.objects.filter(color_name=x).exists():
                        pI = ProductColors.objects.filter(color_name=x).first()
                    else:
                        pI = ProductColors.objects.create(color_name=x)
                    product.colors.add(pI)

            if request.FILES.getlist('images'):
                product.images.clear()
                for x in request.FILES.getlist('images'):
                    product.images.add(ProductImages.objects.create(image=x))

            return Response({'status':'Success','msg':'Product updated successfully!'}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "Error", "reason": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None):
        if not pk or not Product.objects.filter(id=pk).exists():
            return Response({"status": "Error", "reason": 'Please provide valid Product ID!'}, status=status.HTTP_400_BAD_REQUEST)
        
        Product.objects.get(id=pk).delete()
        return Response({'status':'Success','msg':'Product Deleted successfully!'}, status=status.HTTP_200_OK)

class CartAPI(APIView):
    def get(self, request, pk=None):
        if not pk:
            return Response({"status": "Error", "reason": 'Please provide User ID!'}, status=status.HTTP_400_BAD_REQUEST)

        if not Cart.objects.filter(user__id=pk).exists():
            return Response({"status": "Error", "reason": 'No Items in Cart!'}, status=status.HTTP_200_OK)
        
        qs = Cart.objects.filter(user__id=pk)
        serializer = CartSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'Success','msg':'Product aaded to cart!', 'data':serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "Error", "reason": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)