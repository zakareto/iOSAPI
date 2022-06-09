from django.urls import path

from . import views

app_name="firstapp"

urlpatterns = [
    path('users',views.users,name='users'),
    path('user/add',views.userAdd,name='userAdd'),
    path('user/delete',views.userDelete,name='userdelete'),
    path('user/get',views.userGet,name='userGet'),
    path('user/get/<int:userid>',views.userGetId,name='userGetId'),
    path('user/update/<int:userid>',views.userUpdate,name='userUpdate'),
    path('user/register',views.register,name='userRegister'),

    path('order',views.orders,name='order'),
    path('order/add',views.orderAdd,name='orderAdd'),
    path('order/delete',views.orderDelete,name='orderdelete'),
    path('order/get',views.orderGet,name='orderGet'),
    path('order/get/<int:orderid>',views.orderGetId,name='orderGetId'),
    path('order/update/<int:orderid>',views.orderUpdate,name='orderUpdate'),


    path('carts',views.carts,name='carts'),
    path('cart/add',views.cartAdd,name='cartAdd'),
    path('cart/insert',views.cartInsert,name='cartInsert'),
    path('cart/delete',views.cartDelete,name='cartdelete'),
    path('cart/delete/all',views.cartDeleteAll,name='cartdeleteAll'),
    path('cart/get',views.cartGet,name='cartGet'),
    path('cart/get/<int:cartid>',views.cartGetId,name='cartGetId'),
    path('cart/items/<int:cartid>',views.cartItems,name='cartItems'),
    path('cart/update/<int:cartid>',views.cartUpdate,name='cartUpdate'),

    
   

    path('videogames',views.videogames,name='videogames'),
    path('videogame/add',views.videogamesAdd,name='videogamesAdd'),
    path('videogame/delete/<int:videogameid>',views.videogamesDelete,name='videogamesdelete'),
    path('videogame/get',views.videogamesGet,name='videogamesGet'),
    path('videogame/get/<int:videogameid>',views.videogamesGetId,name='videogamesGetId'),
    path('videogame/update/<int:videogameid>',views.videogamesUpdate,name='videogamesUpdate'),

    path('rating',views.rating,name='rating'),
    path('rating/add',views.ratingAdd,name='ratingAdd'),
    path('rating/delete',views.ratingDelete,name='ratingdelete'),

    path('add',views.add,name='add'),
    path('delete/<int:videogameid>/<str:videogame>',views.delete,name='delete'),
    path('update/<int:videogameid>',views.update,name='update'),

]
