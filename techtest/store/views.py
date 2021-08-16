from django.shortcuts import render
import requests, json, uuid
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from .models import ProductDetails, ProductCart
from django.contrib import messages

# Create your views here.

def index(request):
    products =  ProductDetails.objects.all()
    cart = ProductCart.objects.all()
    total = total_cart(cart)
    return render(request, 'index.html',{'products':products,'cart':cart,'len_cart':total[1],'total_cart_price':total[0]})

def total_cart(obj_cart):
    total_cart_price = 0
    total_qty = 0
    for product in obj_cart:
        total_cart_price = total_cart_price + product.product_price * product.qty
        total_qty = total_qty + product.qty    
    return total_cart_price, total_qty
    
def product(request):
    return render(request, 'products.html')

def add_toCart(request, pid):
    obj = ProductDetails.objects.get(product_id=pid)
    cart = ProductCart.objects.filter(product_id=pid)

    if cart:
        update_qty = [x.qty for x in cart][0]       
        cart.update(qty= update_qty  + 1 )
    else:
        product_dict = obj.__dict__
        del product_dict['_state']
        post = ProductCart(**product_dict)
        post.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def remove_fromCart(request, pid):
    cart = ProductCart.objects.filter(product_id=pid).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
def cart(request):
    cart = ProductCart.objects.all()
    total = total_cart(cart)
    return render(request, 'cart.html',{'cart':cart,'len_cart':total[1],'total_cart_price':total[0]})
    
def checkout(request):
    cart = ProductCart.objects.all()
    total = total_cart(cart)
    return render(request, 'checkout.html' ,{'cart':cart,'len_cart':total[1],'total_cart_price':total[0], 'payment_options': json.dumps(payment(total))})
    
def get_api_response(url,data):
    headers = {'x-api-key' : 'AQEyhmfxLI3MaBFLw0m/n3Q5qf3VaY9UCJ14XWZE03G/k2NFitRvbe4N1XqH1eHaH2AksaEQwV1bDb7kfNy1WIxIIkxgBw==-y3qzswmlmALhxaVPNjYf74bqPotG12HroatrKA066yE=-W+t7NF;s4}%=kUSD','content-type': 'application/json'}    
    response = requests.post(url, data=json.dumps(data), headers=headers)
    return response

def payment(total):
    url = 'https://checkout-test.adyen.com/v67/paymentMethods'
    data = {
            "merchantAccount": "AdyenRecruitmentCOM",
            "countryCode": "AU",
            "amount": {
                        "currency": "AUD",
                        "value": int(total[0]*100)
                      },
            "channel": "Web",
            "shopperLocale": "en_US"
            }
    response = get_api_response(url,data)
    formatted_response = json.loads(response.content)
    return formatted_response

@csrf_exempt 
def initiatePayment(request):  
    if request.method == "POST":
        cart = ProductCart.objects.all()
        total = total_cart(cart)
        json_data = json.loads(request.body)
        url = 'https://checkout-test.adyen.com/v67/payments' 
        paymentMethod = json_data['paymentMethod']
        
        if paymentMethod['type']=='scheme':
            data = {
                    'paymentMethod': paymentMethod ,
                    'origin':'http://127.0.0.1:5000/',
                    'browserInfo': json_data['browserInfo'],
                    'channel': "Web",
                    'storePaymentMethod':json_data['storePaymentMethod'],
                    'amount': {
                                'value': int(total[0]*100),
                                'currency': 'AUD'
                              },
                    'reference': "Rahul_checkoutChallenge",
                    'returnUrl': 'http://127.0.0.1:5000/api/redirect/',
                    'merchantAccount': 'AdyenRecruitmentCOM'
                    }
        else:
            data = {
                    'paymentMethod': paymentMethod ,
                    'origin':'http://127.0.0.1:5000/',
                    'channel': "Web",
                    'amount': {
                                'value': int(total[0]*100),
                                'currency': 'AUD'
                              },
                    'reference': "Rahul_checkoutChallenge",
                    'returnUrl': 'http://127.0.0.1:5000/api/redirect/',
                    'merchantAccount': 'AdyenRecruitmentCOM'
                    }
           
        response = get_api_response(url,data)
        formatted_response = json.loads(response.content)
        try:
            request.session['resultCode'] = formatted_response['resultCode']
            request.session['pspReference'] = formatted_response['pspReference']            
            request.session['refusalReason'] = formatted_response['refusalReason']
        except Exception as e: 
            print("error occurred due to: " + str(e))
        
        return JsonResponse(formatted_response)
    
    if request.method == "GET":
        redirectResult = request.GET.get('redirectResult')
        url = 'https://checkout-test.adyen.com/v67/payments/details'
        data =  {
                "details": 
                    {
                        "redirectResult":redirectResult
                    }
                }
        response = get_api_response(url,data)
        formatted_response = json.loads(response.content)
        try:
            request.session['resultCode'] = formatted_response['resultCode']
            request.session['pspReference'] = formatted_response['pspReference']            
            request.session['refusalReason'] = formatted_response['refusalReason']
        except Exception as e: 
            print("error occurred due to: " + str(e))
        if formatted_response['resultCode'] == 'Authorised':
            return redirect("success")
        if formatted_response['resultCode'] == 'Received':
            return redirect("pending")            
        if formatted_response['resultCode'] == 'Pending':
            return redirect("pending")
        else:
            return redirect("error")

def clear_cart(request):
    ProductCart.objects.all().delete()
    return HttpResponseRedirect('/home/')
    
def success(request):
    return render(request,"success.html")
    
def pending(request):
    return render(request,"pending.html")
    
def error(request):
    return render(request,"error.html")