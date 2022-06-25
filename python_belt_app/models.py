from django.db import models
import re

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {} 
        letter_only=re.compile(r'[A-Za-z]')
       
        if not (postData['name']):
            errors["name"] = "please enter a name!!"
        elif len(postData['name']) <3:
            errors["name"] = "name's characters should be at least 3 letters "
        elif not letter_only.match(postData['name']):
             errors["name"] = "name shloud be only letters! "

        if not (postData['username']):
            errors["username"] = "please enter a username!!"
        elif len(postData['username']) <3:
            errors["username"] = "username's characters should be at least 3 letters "
        
        if not (postData['password']):
            errors["password"] = "please enter a password!!"
        elif len(postData['password']) <8:
            errors["password"] = "password's characters should be at least 8"
        
        if not (postData['re_password']):
            errors["re_password"] = "please enter a confirm password!!"
        elif postData['password'] != postData['re_password']:
            errors["re_password"] = "confirm password didnt match with password!! "
        return errors
    

class ItemsManager (models.Manager):
        
   def basic_validator(self, postData):
        errors={}
        if not (postData['item_name']):
            errors["item_name"] = "please enter a product name!!"
        elif len(postData['item_name']) <3:
            errors["item_name"] = "product name's characters should be at least 3 letters "
            
        return errors
      


class User(models.Model): 
    name = models.TextField()
    username = models.TextField()
    hired_date = models.DateField()
    pw_hash = models.TextField()
    objects = UserManager()    


class Items(models.Model): 
    name = models.TextField()
    wish_list = models.ManyToManyField(User, related_name="my_wishlist")
    added_by = models.ForeignKey(User, related_name="items" , on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    objects=ItemsManager()


