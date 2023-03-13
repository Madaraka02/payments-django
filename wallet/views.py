from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
# from mpesapy import Mpesa
from .models import *
# from python_flutterwave import payment
from .mpesa_payments import deposit_from_mpesa, send_money_to_mpesa



def home(request):
    deposit = deposit_from_mpesa(phone=254742415221, chamaName='Iko nini', transactionType='Deposit', amount=10)
    send = send_money_to_mpesa(amount=10, Occasion='Merrygo round payout nini', phone=254742415221, Remarks='Iko nini')

    if deposit == 200:
        print(f'Deposit returned 200 OK')
    if send == 200:
        print(f'send returned 200')
   
    return render(request, 'home.html')


@csrf_exempt
def deposit(request):
    if request.method == 'POST':
        amount = float(request.POST.get('amount'))
        mpesa_number = request.POST.get('mpesa_number')
        wallet = Wallet.objects.get(user=request.user)
        mpesa = Mpesa()
        response = mpesa.stk_push(amount, mpesa_number)
        if response['ResponseCode'] == '0':
            wallet.balance += amount
            wallet.save()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@csrf_exempt
def withdraw(request):
    if request.method == 'POST':
        amount = float(request.POST.get('amount'))
        mpesa_number = request.POST.get('mpesa_number')
        wallet = Wallet.objects.get(user=request.user)
        if wallet.balance >= amount:
            mpesa = Mpesa()
            response = mpesa.b2c_payment(amount, mpesa_number)
            if response['ResponseCode'] == '0':
                wallet.balance -= amount
                wallet.save()
                return JsonResponse({'success': True})
        return JsonResponse({'success': False})
    




from django.views.generic import View
from django.http import HttpResponse
import requests
from django.conf import settings
from djmoney.money import Money
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect

class DepositView(View):
    def get(self, request):
        return render(request, 'deposit.html')

    def post(self, request):
        phone_number = request.POST['phone_number']
        amount = request.POST['amount']
        wallet = Wallet.objects.get(user=request.user)

        payload = {
            'BusinessShortCode': settings.DARAJA_SHORT_CODE,
            'Password': '',
            'Timestamp': '',
            'TransactionType': 'CustomerPayBillOnline',
            'Amount': amount,
            'PartyA': phone_number,
            'PartyB': settings.DARAJA_SHORT_CODE,
            'PhoneNumber': phone_number,
            'CallBackURL': settings.DARAJA_CALLBACK_URL,
            'AccountReference': 'Test',
            'TransactionDesc': 'Test'
        }

        response = requests.post(
            'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest',
            json=payload,
            headers={
                'Authorization': f'Bearer {self.get_access_token()}'
            }
        )

        if response.status_code == 200:
            messages.success(request, 'Deposit')

from mpesapy import Mpesa


def test_payment(request):
    mpesa = Mpesa('sandbox', '600462', 'slwclvtXAJqPbIKsNlVApOX6bg0wLrBA' , 'mcu9AwGNLb4F8SG9')
    access_token = mpesa.get_access_token()
    res_json = mpesa.lipa_na_mpesa_online(
                            Password='bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919', 
                            Timestamp='20180704203000', 
                            Amount='1', 
                            PartyA='254742415221', 
                            PartyB='174379', 
                            PhoneNumber='254742415221', 
                            CallBackURL='https://putsreq.com/C1HAyC3fEEbl2UaEu6lU', 
                            AccountReference='Test', 
                            TransactionDesc='Test')
    
    print(res_json)


def depositt(request):
    mpesa = Mpesa('sandbox', '600462', 'slwclvtXAJqPbIKsNlVApOX6bg0wLrBA' , 'mcu9AwGNLb4F8SG9')
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        amount = request.POST['amount']
        
        # Construct the request
        request_data = {
            'BusinessShortCode': '174379',
            'Password': 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919',
            'Timestamp': '20230304203000',
            'TransactionType': 'CustomerPayBillOnline',
            'Amount': amount,
            'PartyA': 254742415221,
            'PartyB': '174379',
            'PhoneNumber': 254742415221,
            'CallBackURL': 'https://putsreq.com/C1HAyC3fEEbl2UaEu6lU',
            'AccountReference': 'Test',
            'TransactionDesc': 'Test'
        }
        
        # Send the request
        response = mpesa.lipa_na_mpesa_online(request_data)
        
        # Handle the response
        if response['ResponseCode'] == '0':
            # Payment was successful, update the wallet balance in the database
            # wallet = Wallet.objects.get(phone_number=phone_number)
            # wallet.balance += Decimal(amount)
            # wallet.save()
            print('Money to wallet')
            return HttpResponse('Deposit successful')
        else:
            # Payment failed, return an error message
            error_message = response['ResponseDescription']
            return HttpResponse(error_message)
    else:
        return render(request, 'deposit.html')


def depo(request):
    mpesa = Mpesa(
    consumer_key='slwclvtXAJqPbIKsNlVApOX6bg0wLrBA',
    consumer_secret='mcu9AwGNLb4F8SG9',
    environment='sandbox'  # or 'production' for live environment
        )
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        amount = request.POST['amount']
        
        # Construct the request data
        request_data = {
            'BusinessShortCode': '174379',
            'Password': 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919',
            'Timestamp': '20230304203000',
            'TransactionType': 'CustomerPayBillOnline',
            'Amount': amount,
            'PartyA': phone_number,
            'PartyB': '174379',
            'PhoneNumber': phone_number,
            'CallBackURL': 'https://putsreq.com/C1HAyC3fEEbl2UaEu6lU',
            'AccountReference': 'Test vic',
            'TransactionDesc': 'Test'
        }
        
        # Send the request
        response = mpesa.lipa_na_mpesa_online('174379', request_data)
        
        # Handle the response
        if response['ResponseCode'] == '0':
            # Payment was successful, update the wallet balance in the database
            # wallet = Wallet.objects.get(phone_number=phone_number)
            # wallet.balance += Decimal(amount)
            # wallet.save()
            print('Money send to wallet')
            return HttpResponse('Deposit successful')
        else:
            # Payment failed, return an error message
            error_message = response['ResponseDescription']
            return HttpResponse(error_message)
    else:
        return render(request, 'deposit.html')





import requests
from requests.auth import HTTPBasicAuth
import json
from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword
# from .models import MpesaPayment


def getAccessToken(request):
    consumer_key = 'cHnkwYIgBbrxlgBoneczmIJFXVm0oHky'
    consumer_secret = '2nHEyWSD4VjpNh2g'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']

    return HttpResponse(validated_mpesa_access_token)


def lipa_na_mpesa_online(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        "Password": LipanaMpesaPpassword.decode_password,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": 254742415221,  # replace with your phone number to get stk push
        "PartyB": LipanaMpesaPpassword.Business_short_code,
        "PhoneNumber": 254742415221,  # replace with your phone number to get stk push
        "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
        "AccountReference": "Victor chama",
        "TransactionDesc": "Testing stk push chamas",
        "PaymentRequest": {
            "ValidationURL": "https://d744-105-29-165-226.in.ngrok.io/",
            "ConfirmationURL": "https://d744-105-29-165-226.in.ngrok.io/"
        }
    }

    response = requests.post(api_url, json=request, headers=headers)
    return HttpResponse('success')


@csrf_exempt
def register_urls(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": LipanaMpesaPpassword.Test_c2b_shortcode,
               "ResponseType": "Completed",
               "ConfirmationURL": "https://79372821.ngrok.io/api/v1/c2b/confirmation",
               "ValidationURL": "https://79372821.ngrok.io/api/v1/c2b/validation"}
    response = requests.post(api_url, json=options, headers=headers)

    return HttpResponse(response.text)


@csrf_exempt
def call_back(request):
    pass


@csrf_exempt
def validation(request):

    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))


@csrf_exempt
def confirmation(request):
    mpesa_body =request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)

    payment = MpesaPayment(
        first_name=mpesa_payment['FirstName'],
        last_name=mpesa_payment['LastName'],
        middle_name=mpesa_payment['MiddleName'],
        description=mpesa_payment['TransID'],
        phone_number=mpesa_payment['MSISDN'],
        amount=mpesa_payment['TransAmount'],
        reference=mpesa_payment['BillRefNumber'],
        organization_balance=mpesa_payment['OrgAccountBalance'],
        type=mpesa_payment['TransactionType'],

    )
    payment.save()

    print(mpesa_payment['MSISDN'], mpesa_payment['TransID'], mpesa_payment['BillRefNumber'], mpesa_payment['OrgAccountBalance'], mpesa_payment['TransactionType'])

    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }

    return JsonResponse(dict(context))


def flutter_payment(request):
    payment.token = 'FLWSECK_TEST-3ecf25c848c3c56ae67d47181c8c8ee8-X'

    mpesa_trans_details = payment.trigger_mpesa_payment(tx_ref="qwertyuio", amount=1, currency='KES', 
                                                    email='victormadaraka@gmail.com', phone_number='254742415221', 
                                                    full_name='Victor madaraka')
    print(mpesa_trans_details)
    return HttpResponse(mpesa_trans_details)


# @require_POST
@csrf_exempt
def webhook(request):
    secret_hash = '"Victor02."'
    signature = request.headers.get("verifi-hash")
    if signature == None or (signature != secret_hash):
        # This request isn't from Flutterwave; discard
        return HttpResponse(status=401)
    payload = request.body
    # It's a good idea to log all received events.
    print(payload)
    # Do something (that doesn't take too long) with the payload
    return HttpResponse(status=200)



def validate_payment(request):
    # Extract the validation data from the request
    validation_data = json.loads(request.body)
    transaction_id = validation_data["TransID"]
    amount = validation_data["TransAmount"]
    phone_number = validation_data["MSISDN"]
    reference = validation_data["BillRefNumber"]
    timestamp = validation_data["TransTime"]
    
    # Process the validation request and return a response
    # You can perform any necessary validation logic here
    return HttpResponse(json.dumps({"ResultCode": 0, "ResultDesc": "Accepted"}))

def confirm_payment(request):
    # Extract the confirmation data from the request
    confirmation_data = json.loads(request.body)
    transaction_id = confirmation_data["TransID"]
    amount = confirmation_data["TransAmount"]
    phone_number = confirmation_data["MSISDN"]
    reference = confirmation_data["BillRefNumber"]
    timestamp = confirmation_data["TransTime"]
    result_code = confirmation_data["ResultCode"]
    
    # Process the confirmation request and return a response
    # You can perform any necessary processing logic here
    if result_code == 0:
        # Payment successful
        return HttpResponse(json.dumps({"ResultCode": 0, "ResultDesc": "Accepted"}))
    else:
        # Payment failed
        return HttpResponse(json.dumps({"ResultCode": 1, "ResultDesc": "Rejected"}))
    


def b2c_payment():
    # Define the endpoint URL
    endpoint = "https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest"
    
    # Define the request headers
    headers = {
        "Authorization": "Bearer {{YOUR_ACCESS_TOKEN}}",
        "Content-Type": "application/json"
    }
    
    # Define the request body
    payload = {
        "InitiatorName": "{{YOUR_INITIATOR_NAME}}",
        "SecurityCredential": "{{YOUR_SECURITY_CREDENTIAL}}",
        "CommandID": "BusinessPayment",
        "Amount": "{{AMOUNT}}",
        "PartyA": "{{PARTY_A}}",
        "PartyB": "{{PARTY_B}}",
        "Remarks": "{{REMARKS}}",
        "QueueTimeOutURL": "{{QUEUE_TIMEOUT_URL}}",
        "ResultURL": "{{RESULT_URL}}",
        "Occasion": "{{OCCASION}}"
    }
    
    # Convert the payload to a JSON string
    payload = json.dumps(payload)
    
    # Send the request to the endpoint
    response = requests.post(endpoint, headers=headers, data=payload)
    
    # Print the response content
    print(response.content)