
from django.shortcuts import render , redirect
from django.contrib import messages
from .models import User , Items
import bcrypt


def index(request):
	return render(request  ,"index.html")

def login(request):
    if request.method == "POST":
        try:
          user=User.objects.get(username=request.POST['username'])
          if (bcrypt.checkpw(request.POST['password'].encode(), user.pw_hash.encode())):
            request.session['userid'] = user.id
            return redirect('/dashboard')
          else:
                messages.error(request, "User password do not match")
        except User.DoesNotExist:
            messages.error(request, "User not found")
            

    return redirect ('/')


def register(request):
    if request.method == "POST":
       errors = User.objects.basic_validator(request.POST)
       if len(errors) >0:
           for key, value in errors.items(): 
             messages.error(request, value)
           return redirect('/')
       else:
          password = request.POST['password']
          pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  # create the hash           
          User.objects.create(name=request.POST['name'],
          username=request.POST['username']  , pw_hash=pw_hash ,
          hired_date=request.POST['date'] ) 
          the_user=User.objects.last()
          request.session['userid'] = the_user.id
          
          return redirect ('/dashboard')

    return redirect ('/')

def dashboard(request):
    if "userid" not in request.session:
        messages.error(request, "Plese login first")
        return redirect("/")
    
    this_user=User.objects.get(id=request.session['userid'])
    
    context={
        "this_user":this_user,
        "my_wishlist":this_user.my_wishlist.all(),
        "users_wishlist":Items.objects.all()
    }
    return render(request,"dashboard.html" , context)

def create_form(request):
    return render(request , "create_item.html")

def create_item(request):
    if request.method=="POST":
        errors = Items.objects.basic_validator(request.POST)
        if len(errors) >0:
           for key, value in errors.items(): 
             messages.error(request, value)
           return redirect('/wish_items/create')
        else:
          this_user=User.objects.get(id=request.session['userid'])
          product_name=request.POST["item_name"]
          Items.objects.create(name=product_name , added_by = this_user)
          the_item=Items.objects.last()
          this_user.my_wishlist.add(the_item) # add the item to wish list of the current user 

          return redirect('/dashboard')


def show_item(request , id ):
    context={
        "all_user":User.objects.all(),
        "item":Items.objects.get(id=id),
    }
    return render(request , "show_item.html" , context)


def add_to_wishlist(request , id):
    this_user=User.objects.get(id=request.session['userid'])
    the_item=Items.objects.get(id=id)
    this_user.my_wishlist.add(the_item)
    return redirect('/dashboard')


def remove_item_from_wishlist(request , id):
    this_user=User.objects.get(id=request.session['userid'])
    the_item=Items.objects.get(id=id)
    the_item.wish_list.remove(this_user) #remove the item from the user's wishlist
    return redirect('/dashboard')

def delete(request , id):
    Items.objects.get(id=id).delete()
    return redirect ('/dashboard')

def logout(request):
    request.session.clear()
    return redirect('/')


