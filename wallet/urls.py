from django.urls import path
from .views import *

urlpatterns = [
    path('pay/', test_payment ),
    path('', home ),
    

    path('deposit/', depo, name='deposit' ),

    path('online/lipa/', lipa_na_mpesa_online, name='lipa_na_mpesa'),

    # register, confirmation, validation and callback urls
    path('c2b/register/', register_urls, name="register_mpesa_validation"),
    path('c2b/confirmation/', confirmation, name="confirmation"),
    path('c2b/validation/', validation, name="validation"),
    path('c2b/callback/', call_back, name="call_back"),

    path('flutt/', flutter_payment, name='flutter_payment')

]