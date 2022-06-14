from django.urls import path
from .views import *

urlpatterns = [

    path('customer_approve/', CustomerApprove.as_view(), name='approve'),
    path('customer_update/', CustomerUpdate.as_view(), name='approve'),
    
]