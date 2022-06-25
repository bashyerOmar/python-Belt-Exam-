from django.urls import path     
from . import views

urlpatterns = [
   path('', views.index),
   path('dashboard', views.dashboard),
   path('create', views.create_item),
   path('register', views.register),	
   path('login', views.login),
   path('logout', views.logout),
   path('wish_items/<int:id>', views.show_item),	
   path('wish_items/<int:id>/delete', views.delete),
   path('wish_items/<int:id>/remove', views.remove_item_from_wishlist),
   path('wish_items/<int:id>/add_to_wishlist', views.add_to_wishlist),
   path('wish_items/create', views.create_form),
   
]