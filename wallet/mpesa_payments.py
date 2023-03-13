import requests
from requests.auth import HTTPBasicAuth
import json
from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword
from .models import MpesaPayment
from django.http import HttpResponse


def getAccessToken():
    consumer_key = 'cHnkwYIgBbrxlgBoneczmIJFXVm0oHky'
    consumer_secret = '2nHEyWSD4VjpNh2g'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']

    return HttpResponse(validated_mpesa_access_token)


def deposit_from_mpesa(phone, chamaName, transactionType, amount):
    print('called')
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}

    print(access_token)

    request = {
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        "Password": LipanaMpesaPpassword.decode_password,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(amount),
        "PartyA": phone,  # replace with your phone number to get stk push
        "PartyB": LipanaMpesaPpassword.Business_short_code,
        "PhoneNumber": phone,  # replace with your phone number to get stk push
        "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
        "AccountReference": f"Payment to {chamaName}",
        "TransactionDesc": f"{transactionType}",
        # "PaymentRequest": {
        #     "ValidationURL": "{{YOUR_VALIDATION_URL}}",
        #     "ConfirmationURL": "{{YOUR_CONFIRMATION_URL}}"
        # }
    }

    response = requests.post(api_url, json=request, headers=headers)
    # return HttpResponse(response)
    print(response.text.encode('utf8'))
    return response.status_code



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
    


def send_money_to_mpesa(amount, Occasion, phone, Remarks ):
    # Define the endpoint URL
    endpoint = "https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest"
    
    access_token = MpesaAccessToken.validated_mpesa_access_token
    # Define the request headers
    headers = {
        "Authorization": "Bearer %s" % access_token,
        "Content-Type": "application/json"
    }
    
    # Define the request body
    payload = {
        "InitiatorName": "testapi",
        "SecurityCredential": "CNh1FhRavuUujo/35hnbBOzovuWbbYTRXXHLsFWH84gDRhKlZyNDXv4am8WDLfdd6d/biqCNZ7V8WRY1ijilAOyhTqhQYhF/ZpC18xOuMHzcDeV5Jj18r32dyZX9XrtrdYQ0huKUant+tyUDtvODzaiRsZ+NZZQ9pTdRNsUHMq2zZwD2YbLGTDGCsV0t4RF63T5pa4ERGWC/W1B4SrXGV1CRM5/Pkg9W8FEgb4O0HkU8pLMCjNqosdh4t/9+Q6m7k9PND+j4autkjblmEtpOw8NaaDs/2x4nhlRmjHWhbLm5c7meJDbWOea8DfwClap8BxEdFwVwhkBusSx6of76bg==",
        "CommandID": "BusinessPayment",
        "Amount": amount,
        "PartyA": "600997",
        "PartyB": phone,
        "Remarks": Remarks,
        "QueueTimeOutURL": "https://d744-105-29-165-226.in.ngrok.io",
        "ResultURL": "https://d744-105-29-165-226.in.ngrok.io",
        "Occasion": Occasion

        # "InitiatorName": "{{YOUR_INITIATOR_NAME}}", The username of the M-Pesa B2C account API operator. NOTE: the access channel for this operator myst be API and the account must be in active status.	
        # "SecurityCredential": "{{YOUR_SECURITY_CREDENTIAL}}", This is the value obtained after encrypting the API initiator password. The process for encrypting the initiator password had been described under docs and an online encryption process is available under get test credential.	
        # "CommandID": "BusinessPayment", SalaryPayment, BusinessPayment, PromotionPayment
        # "Amount": "{{AMOUNT}}",
        # "PartyA": "{{PARTY_A}}", This is the B2C organization shortcode from which the money is to be sent.	
        # "PartyB": "{{PARTY_B}}", This is the customer mobile number  to receive the amount. - The number should have the country code (254) without the plus sign.	
        # "Remarks": "{{REMARKS}}", Any additional information to be associated with the transaction.	
        # "QueueTimeOutURL": "{{QUEUE_TIMEOUT_URL}}", This is the URL to be specified in your request that will be used by API Proxy to send notification incase the payment request is timed out while awaiting processing in the queue. 	
        # "ResultURL": "{{RESULT_URL}}", This is the URL to be specified in your request that will be used by M-Pesa to send notification upon processing of the payment request.	
        # "Occasion": "{{OCCASION}}" Any additional information to be associated with the transaction.	
    }
    # QueueTimeOutURL :https://mydomain.com/b2c/queue
    # ResultURL :https://mydomain.com/b2c/result
    
    # Convert the payload to a JSON string
    payload = json.dumps(payload)
    
    # Send the request to the endpoint
    response = requests.post(endpoint, headers=headers, data=payload)
    
    # Print the response content


    print(HttpResponse(response.status_code))
    return response.status_code
