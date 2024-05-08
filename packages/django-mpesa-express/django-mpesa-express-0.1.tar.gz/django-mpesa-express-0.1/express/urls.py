from django.urls import path

from express.views import  MpesaCheckout, MpesaCallBack
urlpatterns = [
    path("checkout/", MpesaCheckout.as_view(), name="checkout"),
    path("callback/", MpesaCallBack.as_view(), name="callback"),
]