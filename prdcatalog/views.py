from django.shortcuts import render,redirect, get_object_or_404
# from django.http import HttpResponse
from django.db.models import F
# F is for checking the difference between values.
from django.template import Template
from .models import Product
from .forms import UserAuth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

@login_required(login_url='auth')
def prdlist(request):
    prds = Product.objects.all()
    return render(request,'prdcat.html',{'prds':set(prds)})

def auth(request):
    form = UserAuth()
    if(request.method=='POST'):
        type = request.POST.get('action')
        if(type=='login'):
            uname = request.POST['username']
            pas = request.POST['password']
            user = authenticate(request,username = uname,password = pas)
            if(user):
                login(request,user)
                return redirect('home')
            else:
                messages.error(request,"User dosen't exist with that 'username' and 'password', try signup! or re-enter.")
        elif(type=='signup'):
            form = UserAuth(request.POST)
            if(form.is_valid()):
                form.save()
                uname = form.cleaned_data.get('username')
                messages.success(request,f"Dear {uname}! Account created now you can login.")
            else:
                messages.error(request,"Account exists or Error creating account, try again!") 
    return render(request,'auth.html',{'form':form})

def home(request):
    log = False
    if(login): log=True
    con={
        'log':log
    }
    return render(request,'home.html',con)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    sub = product.in_price-product.fn_price
    con={
        'product':product,
        'sub':sub
    }
    return render(request, 'product_detail.html', con)
@login_required
def product_list(request):
    # category_query = request.GET.get('category', '')
    # products = Product.objects.all()
    # sort_option = request.GET.get('sort')
    # if sort_option == 'low_to_high':
    #     products = products.order_by('fn_price')
    # elif sort_option == 'high_to_low':
    #     products = products.order_by('-fn_price')
    # # for discount.
    # show_discounted = request.GET.get('show_discounted')
    # if show_discounted:
    #     # filtering products where initial price is different from final price
    #     products = products.filter(in_price__gt=F('fn_price'))
    # if category_query:
    #     products = Product.objects.filter(cat__name__icontains=category_query)
    #     return render(request, 'prdcat.html', {'prds': set(products)})
    # return render(request, 'prdcat.html', {'prds': products})
    category_query = request.GET.get('category', '')
    products = Product.objects.all()
    if category_query:
        products = products.filter(cat__name__icontains=category_query)

    sort_option = request.GET.get('sort')
    if sort_option == 'low_to_high':
        products = products.order_by('fn_price')
    elif sort_option == 'high_to_low':
        products = products.order_by('-fn_price')
    show_discounted = request.GET.get('show_discounted')
    if show_discounted:
        # filtering products where initial price is different from final price
        products = products.filter(in_price__gt=F('fn_price'))

    return render(request, 'prdcat.html', {'prds': products,'show_discounted': show_discounted})


