
# Django DPO Gateway

Django DPO Gateway is a Django app for integrating DPO payment gateway.
Detailed documentation is in the "docs" directory.

## Quick start

1. Add `django_dpo` to your INSTALLED_APPS setting like this::

```python 

    INSTALLED_APPS = [
        ...,
        "django_dpo",
    ]

```

2. Include DPO Settings in your project `settings.py` like this::

```python
	
	DPO_END_POINT = "https://secure.3gdirectpay.com/API/v6/"
	DPO_PAYMENT_URL = "https://secure.3gdirectpay.com/payv2.php"
	DPO_COMPANY_TOKEN = "<your-company-token-from-dpo>"
	DPO_PAYMENT_CURRENCY = "<preferred currency>"
	DPO_PAYMENT_TIME_LIMIT = 5
	DPO_SERVICE_TYPE = 5525 

```


## DPO Gateway Usage


### Create Token

```python

from django.shortcuts import resolve_url
from django_dpo import DPOGateway


def create_token(request):

    invoice_number = request.POST.get('invoice_number')
    amount = request.POST.get('amount')
    description = request.POST.get('description')

    redirect_url= request.build_absolute_uri(resolve_url('payment_url'))
    back_url = request.build_absolute_uri(resolve_url('back_url'))

    gateway = DPOGateway()

    gateway.set_redirect_url(redirect_url)
    gateway.set_back_url(back_url)

    response = gateway.create_token(
        company_ref=invoice_number,
        amount=float(amount),
        description=description
    )
    transaction_token = response.TransToken

    return gateway.make_payment(transaction_token)

```


### Verify Token

```python

from django.http import HttpResponseBadRequest
from django.contrib import messages
from django.shortcuts import redirect,reverse
from django_dpo import DPOGateway

def verify_payment(request):

    if not request.GET.get('TransID') and not request.GET.get('companyRef'):
        return HttpResponseBadRequest()
        
    transaction_token = request.GET.get('TransID')
    invoice_number = request.GET.get('PnrID')

    gateway = DPOGateway()

    response = gateway.verify_payment(transaction_token)

    amount = response.TransactionAmount
    currency = response.TransactionCurrency
    
    message = f"The payment of {currency} {amount} was successful"

    messages.success(request, message) 

    return redirect(reverse("index"))

```


### Cancel Token

```python

from django.http import HttpResponseBadRequest
from django.contrib import messages
from django.shortcuts import redirect, reverse
from django_dpo import DPOGateway

def cancel_token(request):

    if not request.GET.get('TransID') and not request.GET.get('companyRef'):
        return HttpResponseBadRequest()

    transaction_token = request.GET.get('TransID')
    gateway = DPOGateway()
    gateway.cancel_token(transaction_token)
    messages.success(request, "Transaction cancelled") 
    return redirect(reverse("index"))

```
