from django.urls import path

from .views import (
                    GetReceiptAPIView, 
                    AddReceiptAPIView,
                    CategoryAPIView
)

urlpatterns = [
    path('', AddReceiptAPIView.as_view(), name = 'receipt-add'),
    path('detail/<slug:slug>/', GetReceiptAPIView.as_view(), name = 'receipt-detail'),
    path('categories/', CategoryAPIView.as_view(), name = 'receipt-categories')
]