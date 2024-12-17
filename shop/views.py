from django.http import JsonResponse
from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import json

def homepage(request):
    products = product.objects.filter(trending=1)
    return render(request,'home.html',{"products":products})


def loginpage(request):

    if request.user.is_authenticated:
        return redirect("/")
    else:

     if request.method=="POST":
        name=request.POST.get('username')
        pwd=request.POST.get('password')
        user=authenticate(request,username=name,password=pwd)
        if user is not None:
            login(request,user)
            messages.success(request,"logged in Successfully")
            return redirect("/")
        else:
            messages.error(request,"invaild user name or password ")
            return redirect("/login/")

    return render(request,'login.html',)


def logoutpage(request):

    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged out Successfully")
        return redirect("/")

    



def registerpage(request):
    form = CustomerForm()
    if request.method == "POST":
        form=CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Regitration success You Can Login Now..!")
            return redirect("/login/")

    return render(request,'register.html',{"form":form})



def collectionpage(request):
    catagory = Catagory.objects.filter(status=0)
    return render(request,'collections.html',{"catagory":catagory})



def collectionpageview(request,name):
    if(Catagory.objects.filter(name=name,status=0)):
        products=product.objects.filter(catagory__name=name)
        return render(request,'index.html',{"products":products,"catagory_name":name})
    
    else:
        messages.warning(request,"no such catagory found")
        return redirect('collections.html')
    
    

def product_details(request,cname,pname):
    if (Catagory.objects.filter(name=cname,status=0)):
        if(product.objects.filter(name=pname,status=0)):
            Products=product.objects.filter(name=pname,status=0).first()
            return render(request,"product_details.html",{"products":Products})
        else:
            messages.error(request,"no such product found")
            return redirect('collect')
    else:
        messages.error(request,"no such product found")
        return redirect('collect')
    


def add_to_Cart(request):

    if request.headers.get('x-requested-with')=='XMLHttpRequest':
     if request.user.is_authenticated:
      data=json.load(request)
      product_qty=data['product_qty']
      product_id=data['pid']
      #print(request.user.id)
      product_status=product.objects.get(id=product_id)
      if product_status:
        if Cart.objects.filter(user=request.user.id,product_id=product_id):
          return JsonResponse({'status':'Product Already in Cart'}, status=200)
        else:
          if product_status.quantity>=product_qty:
            Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
            return JsonResponse({'status':'Product Added to Cart'}, status=200)
          else:
            return JsonResponse({'status':'Product Stock Not Available'}, status=200)
     else:
      return JsonResponse({'status':'Login to Add Cart'}, status=200)
    else:
     return JsonResponse({'status':'Invalid Access'}, status=200)
    

def cart_page(request):
   if request.user.is_authenticated:
      cart=Cart.objects.filter(user=request.user)
      return render(request,"cart.html",{"cart":cart})
   else:
      return redirect("/")
   

def remove_cart(request,cid):
   cartitem=Cart.objects.get(id=cid)
   cartitem.delete()
   return redirect("/cart/")


def fav_page(request):
      
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
      if request.user.is_authenticated:
       data=json.load(request)
       product_id=data['pid']
       product_status=product.objects.get(id=product_id)
       if product_status:
         if Favourite.objects.filter(user=request.user.id,product_id=product_id):
          return JsonResponse({'status':'Product Already in Favourite'}, status=200)
         else:
          Favourite.objects.create(user=request.user,product_id=product_id)
          return JsonResponse({'status':'Product Added to Favourite'}, status=200)
      else:
       return JsonResponse({'status':'Login to Add Favourite'}, status=200)
    else:
     return JsonResponse({'status':'Invalid Access'}, status=200)
    

def fav_view(request):
   if request.user.is_authenticated:
      fav=Favourite.objects.filter(user=request.user)
      return render(request,'fav.html',{"fav":fav})
   else:
      return redirect("/")
   

def remove_fav(request,fid):
   cartitem=Favourite.objects.get(id=fid)
   cartitem.delete()
   return redirect("/favview/")

  
   
     
        
     


