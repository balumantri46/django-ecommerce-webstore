from django.shortcuts import render,redirect
# from django.http import HttpResponse
from django.template import Template
from .models import Product
from .forms import UserAuth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages


def prdlist(request):
    prds = Product.objects.all()
    return render(request,'prdcat.html',{'prds':prds})

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
@login_required
def home(request):
    return render(request,'home.html')

