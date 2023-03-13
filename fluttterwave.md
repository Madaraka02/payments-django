create a wallet
    method: 'POST'
    url: 'https://api.flutterwave.com/v3/payout-subaccounts'
    authorization: 'Bearer FLUTTERWAVE_SECRET_KEY '
        payload : {
                "account_name": "Test name",
                "email": "testchama@gmail.com",
                "mobilenumber": "254756158673",
                "country": "KE"
                }


Check wallet balance
    method: 'GET'
    url: 'https://api.flutterwave.com/v3/payout-subaccounts/PSA8102E196849106427/balances?currency=KES'
    authorization: 'Bearer FLUTTERWAVE_SECRET_KEY '


Initiate mpesa charge (deposit to wallet)
    method: 'POST'
    url: 'https://api.flutterwave.com/v3/charges?type=mpesa'
    authorization: 'Bearer FLUTTERWAVE_SECRET_KEY '
        payload : {
                "phone_number": "254742415221",
                "amount": 10,
                "currency": "KES",
                "email": "i@need.money",
                "tx_ref": "BJUYU399fcd43"  unique
                }

Chech transaction status
    method: 'GET'
    url: 'https://api.flutterwave.com/v3/transactions/4194960/verify'
    authorization: 'Bearer FLUTTERWAVE_SECRET_KEY '


Transfer money to mpesa (withdraw from wallet)
    method: 'POST'
    url: 'https://api.flutterwave.com/v3/charges?type=mpesa'
    authorization: 'Bearer FLUTTERWAVE_SECRET_KEY '
        payload : {
                    "account_bank": "MPS",
                    "account_number": "254742415221",
                    "amount": 10,
                    "currency": "KES",
                    "beneficiary_name": "Carol Wanjiru",
                    "meta": {
                        "sender": "Madaraka victor",
                        "sender_country": "KE",
                        "mobile_number": "254742415221"
                    }
                    }


        payload2 : {
                    "account_bank": "MPS",
                    "account_number": "{{MPESA_ACCOUNT_NUMBER}}",
                    "amount": "50",
                    "narration": "Transfer to M-Pesa",
                    "currency": "KES",
                    "beneficiary_name": "{{MPESA_ACCOUNT_NAME}}",
                    "reference": "{{UNIQUE_REFERENCE}}",
                    "callback_url": "https://your-callback-url.com"
                }

Get transfer rates
    method: 'GET'
    url: 'https://api.flutterwave.com/v3/transfers/rates?amount=100&destination_currency=KES&source_currency=KES'
    authorization: 'Bearer FLUTTERWAVE_SECRET_KEY '


Bulk transfers
    method: 'POST'
    url: 'https://api.flutterwave.com/v3/bulk-transfers'
    authorization: 'Bearer FLUTTERWAVE_SECRET_KEY'
        payload:  {"bulk_data": [
        {
            "bank_code": "FNB",
            "account_number": "0031625807099",
            "amount": 1900,
            "currency": "ZAR",
            "narration": "Test transfer to F4B Developers",
            "reference": "bulk_Transfers_0019_PMCK",
            "meta": [
                {
                "first_name": "F4B",
                "last_name": "Developers",
                "email": "developers@flutterwavego.com",
                "mobile_number": "+23457558595",
                "recipient_address": "234 Kings road, Cape Town"
                }
            ]
        },
        {
            "bank_code": "FNB",
            "account_number": "0031625807099",
            "amount": 3200,
            "currency": "ZAR",
            "narration": "Test transfer to Support",
            "reference": "bulk_Transfers_0020_PMCK",
            "meta": [
                {
                "first_name": "Flutterwave",
                "last_name": "Support",
                "email": "support@flutterwavego.com",
                "mobile_number": "+23457558595",
                "recipient_address": "234 Kings road, Cape Town"
                }
            ]
        },
        {
            "bank_code": "FNB",
            "account_number": "0031625807099",
            "amount": 6950,
            "currency": "ZAR",
            "narration": "Test transfer to Flutterwave Developers",
            "reference": "bulk_Transfers_0021_PMCK",
            "meta": [
                {
                "first_name": "Flutterwave",
                "last_name": "Developers",
                "email": "developers@flutterwavego.com",
                "mobile_number": "+23457558595",
                "recipient_address": "234 Kings road, Cape Town"
                }
            ]
        },
        {
            "bank_code": "FNB",
            "account_number": "0031625807099",
            "amount": 1500,
            "currency": "ZAR",
            "narration": "Test transfer to Wavers",
            "reference": "bulk_Transfers_0022_PMCK",
            "meta": [
                {
                "first_name": "Wavers",
                "last_name": "N/A",
                "email": "hi@flutterwavego.com",
                "mobile_number": "+23457558595",
                "recipient_address": "234 Kings road, Cape Town"
                }
            ]
        }
    ]
    }
bulk_data :
An array of objects containing the transfer charge data. This array contains the same payload you would passed to create a single transfer with multiple different values.

Wallet to wallet transfer 

They make use of the create transfer endpoint, with the key difference being that account_bank is always "flutterwave", while account_number is the merchant's ID.


    method: 'POST'
    url: 'https://api.flutterwave.com/v3/transfers'
    authorization: 'Bearer FLUTTERWAVE_SECRET_KEY'
        payload: {
                account_bank: "flutterwave",
                account_number: "99992069",
                amount: 500,
                currency: "NGN",
                debit_currency: "NGN"
            }


Create A Virtual Card
    method: 'POST'
    url: 'https://api.flutterwave.com/v3/virtual-cards'
    authorization: 'Bearer FLUTTERWAVE_SECRET_KEY'
        payload: {
                "currency": "USD",
                "amount":5,
                "debit_currency": "NGN",
                "billing_name": "Example User.",
                "billing_address": "333, Fremont Street",
                "billing_city": "San Francisco",
                "billing_state": "CA",
                "billing_postal_code": "94105",
                "billing_country": "US",
                "first_name": "Example",
                "last_name": "User",
                "date_of_birth": "1996/12/30",
                "email": "userg@example.com",
                "phone": "07030000000",
                "title": "MR",
                "gender": "M",
                "callback_url": "https://webhook.site/b67965fa-e57c-4dda-84ce-0f8d6739b8a5"
            }


Fund A Virtual Card

    method: 'POST'
    url: 'https://api.flutterwave.com/v3/virtual-cards/:id/fund'
    authorization: 'Bearer FLUTTERWAVE_SECRET_KEY'
        payload: {
            'debit_currency':'',
            'amount':'' 
        }

Withdraw From A Virtual Card
    method: 'POST'
    url: 'https://api.flutterwave.com/v3/virtual-cards/:id/withdraw'
    authorization: 'Bearer FLUTTERWAVE_SECRET_KEY'
        payload: {
            'amount':'' 
        }


Block/Unblock Virtual Card
    method: 'POST'
    url: 'https://api.flutterwave.com/v3/virtual-cards/:id/status/:status_action'
    authorization: 'Bearer FLUTTERWAVE_SECRET_KEY'

status_action 
This is the action you want to perform on the virtual card. Can be block or unblock


Terminate A Virtual Card

    method: 'POST'
    url: 'https://api.flutterwave.com/v3/virtual-cards/:id/terminate'
    authorization: 'Bearer FLUTTERWAVE_SECRET_KEY'
        payload: {
            'amount':'' 
        }

Get A Virtuals Card's Transactions

    method: 'GET'
    url: 'https://api.flutterwave.com/v3/virtual-cards/:id/transactions'
    authorization: 'Bearer FLUTTERWAVE_SECRET_KEY'
        payload: {
            'amount':'' 
        }
        
QUERY PARAMS
from string
This is the start date of the transaction request period

to string
This is the end date of the transaction request period

index int
Pass 0 if you want to start from the beginning

size int
Specify how many transactions you want to retrieve in a single call        

