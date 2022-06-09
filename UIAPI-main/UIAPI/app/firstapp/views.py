# Create your views here.
#IMPORT models

#IMPORT LIBRARIRES/FUNCTIONS
from django.shortcuts import render , HttpResponse, redirect
from django.http import JsonResponse
import json

#IMPORT DJANGO PASSWORD HASH GENERATOR AND COMPARE
from django.contrib.auth.hashers import make_password, check_password
from .models import Videogames, Rating, Users, Order, Cart
from django import forms

#check_password(noHashPassword,HashedPassword) this funcion validate if the password match to the hash

#def vista(request):
#    return render(request,'clase.html')

class VideogameForm(forms.ModelForm):
    class Meta:
        model = Videogames #model es igual al modelo del archivo models.py
        fields = [
            'name',
            'genre',
            'rating_id',
            
        ]
        labels = { 
            'name' : 'Nombre', 
            'genre' : 'Genero',
            'rating_id' : 'Rating id',
            
        }
        widgets = {
            'name' : forms.TextInput(attrs={'required': True, 'class': 'form-control'}), #Para validar los campos del form
            'genre' : forms.TextInput(attrs={'required': True, 'class': 'form-control'}),
            'rating_id' : forms.NumberInput(attrs={'required': True, 'class': 'form-control'})
        }


###############################################
def users(request):

    if request.method == 'GET':

        apikey = request.headers.get('api_key')
        apikey = "33390d09esdioewu0qe0uqu0"
        if apikey is not None:

            if apikey != "33390d09esdioewu0qe0uqu0":
                responseData = {}
                responseData['success'] = 'false'
                responseData['message'] = 'API KEY NOT VALID'
                return JsonResponse(responseData, status=400)

            responseData = {}
            responseData['success'] = 'true'
            responseData['key'] = apikey
            responseData['data'] = list(Users.objects.all().values())
            return JsonResponse(responseData, status=200)

        responseData = {}
        responseData['success'] = 'false'
        responseData['message'] = 'No api Key'
        return JsonResponse(responseData, status=400)

    else:

        responseData = {}
        responseData['success'] = 'false'
        responseData['mesage'] = 'Wrong Method'
        return JsonResponse(responseData, status=400)

def userAdd(request):

    if request.method == 'POST':

        try:
            json_object = json.loads(request.body)
            newuser = Users(username=json_object['user_username'], password=json_object['user_password'], email=json_object['user_email'])
            #INSERT INTO dogs (name, type_id,color,size) values ('Solovino',4,'black','big')
            newuser.save()
            responseData = {}
            responseData['success'] = 'true'
            responseData['message'] = 'user inserted'
            return JsonResponse(responseData, status=200)
        except ValueError as e:
            responseData = {}
            responseData['success'] = 'false'
            responseData['message'] = 'Invalid Json'
            return JsonResponse(responseData, status=400)

    else:

        responseData = {}
        responseData['success'] = 'false'
        responseData['mesage'] = 'Wrong Method'
        return JsonResponse(responseData, status=400)

def userDelete(request):

    if request.method == 'DELETE':

        try:
            json_object = json.loads(request.body)
            try:
                one_entry = Users.objects.get(id=json_object["user_id"])
            except:
                responseData = {}
                responseData['success'] = 'false'
                responseData['message'] = 'The user_id its not valid'
                return JsonResponse(responseData, status=400)
            Users.objects.filter(id=json_object["user_id"]).delete()
            responseData = {}
            responseData['success'] = 'true'
            responseData['message'] = 'The user has been deleted'
            return JsonResponse(responseData, status=200)
        except ValueError as e:
            responseData = {}
            responseData['success'] = 'false'
            responseData['data'] = 'Invalid Json'
            return JsonResponse(responseData, status=400)
    else:

        responseData = {}
        responseData['success'] = 'false'
        responseData['mesage'] = 'Wrong Method'
        return JsonResponse(responseData, status=400)

def userGet(request):

    if request.method == 'POST':

        try:
            json_object = json.loads(request.body)
            try:
                one_entry = Users.objects.get(username=json_object["user_username"], password=json_object["user_password"])
            except:
                responseData = {}
                responseData['success'] = 'false'
                responseData['message'] = 'The credentials are not valid'
                responseData['status'] = "fallido"
                return JsonResponse(responseData, status=400)
            responseData = {}
            responseData['success'] = 'true'
            responseData['data'] = {}
            responseData['data']['id'] = one_entry.id
            responseData['data']['username'] = one_entry.username
            responseData['data']['password'] = one_entry.password
            responseData['data']['email'] = one_entry.email
            responseData['status'] = "conectado"
           

            return JsonResponse(responseData, status=200)
        except ValueError as e:
            responseData = {}
            responseData['success'] = 'false'
            responseData['data'] = 'Invalid Json'
            return JsonResponse(responseData, status=400)
    else:

        responseData = {}
        responseData['success'] = 'false'
        responseData['mesage'] = 'Wrong Method'
        return JsonResponse(responseData, status=400)


def register(request):

    if request.method == 'POST':

        try:
            json_object = json.loads(request.body)
            try:
                userVer = Users.objects.get(username=json_object["user_username"])
            except:
                try:
                    emailVer= Users.objects.get(email=json_object["user_email"])
                except:
                    try: 
                        newuser = Users(username=json_object['user_username'], password=json_object['user_password'], email=json_object['user_email'])
                        newuser.save()
                        responseData = {}
                        responseData['success'] = 'true'
                        responseData['message'] = 'Usuario registrado con exito'
                        return JsonResponse(responseData, status=200)
                    except ValueError as e:
                        responseData = {}
                        responseData['success'] = 'false'
                        responseData['message'] = 'Invalid Json'
                        return JsonResponse(responseData, status=400)
                responseData = {}
                responseData['success'] = 'false'
                responseData['message'] = 'correo en uso'
                responseData['status'] = "fallido"
                return JsonResponse(responseData, status=400)
            responseData = {}
            responseData['success'] = 'false'
            responseData['message'] = 'usuario en uso'
           

            return JsonResponse(responseData, status=400)
        except ValueError as e:
            responseData = {}
            responseData['success'] = 'false'
            responseData['data'] = 'Invalid Json'
            return JsonResponse(responseData, status=400)
    else:

        responseData = {}
        responseData['success'] = 'false'
        responseData['mesage'] = 'Wrong Method'
        return JsonResponse(responseData, status=400)



def userGetId(request, userid):

    if request.method == 'GET':

        try:
            one_entry = Users.objects.get(id=userid)
        except:
            responseData = {}
            responseData['success'] = 'false'
            responseData['message'] = 'The user_id its not valid'
            return JsonResponse(responseData, status=400)

        responseData = {}
        responseData['success'] = 'true'
        responseData['data'] = {}
        responseData['data']['username'] = one_entry.username
        responseData['data']['password'] = one_entry.password
        responseData['data']['email'] = one_entry.email

        return JsonResponse(responseData, status=200)

    else:

        responseData = {}
        responseData['success'] = 'false'
        responseData['mesage'] = 'Wrong Method'
        return JsonResponse(responseData, status=400)

def userUpdate(request,userid):

    if request.method == 'POST':
        try:
            one_entry = Users.objects.get(id=userid)
        except:
            responseData = {}
            responseData['success'] = 'false'
            responseData['message'] = 'The user_id its not valid'
            return JsonResponse(responseData, status=400)
        try:
            json_object = json.loads(request.body)
            contador = 0
            #AQUI VA EL CODIGO DEL UPDATE
            try:
                value = json_object["user_username"]
                Users.objects.filter(id=userid).update(username=json_object["user_username"])
                contador = contador + 1
            except KeyError:
                responseData = {}

            try:
                value = json_object["user_pasword"]
                Users.objects.filter(id=userid).update(password=json_object["user_password"])
                contador = contador + 1
            except KeyError:
                responseData = {}

            try:
                value = json_object["user_email"]
                Users.objects.filter(id=userid).update(email=json_object["user_email"])
                contador = contador + 1
            except KeyError:
                responseData = {}

            if contador == 0:
                responseData = {}
                responseData['success'] = 'false'
                responseData['message'] = 'Nada por actualizar'
                return JsonResponse(responseData, status=400)
            else:
                responseData = {}
                responseData['success'] = 'true'
                responseData['message'] = 'Datos actualizados'
                return JsonResponse(responseData, status=200)

        except ValueError as e:
            responseData = {}
            responseData['success'] = 'false'
            responseData['data'] = 'Invalid Json'
            return JsonResponse(responseData, status=400)

    else:

        responseData = {}
        responseData['success'] = 'false'
        responseData['mesage'] = 'Wrong Method'
        return JsonResponse(responseData, status=400)
###############################################
def carts(request):

    if request.method == 'GET':

        apikey = request.headers.get('api_key')
        apikey = "33390d09esdioewu0qe0uqu0"
        if apikey is not None:

            if apikey != "33390d09esdioewu0qe0uqu0":
                responseData = {}
                responseData['success'] = 'false'
                responseData['message'] = 'API KEY NOT VALID'
                return JsonResponse(responseData, status=400)

            responseData = {}
            responseData['success'] = 'true'
            responseData['key'] = apikey
            responseData['data'] = list(Cart.objects.all().values())
            return JsonResponse(responseData, status=200)

        responseData = {}
        responseData['success'] = 'false'
        responseData['message'] = 'No api Key'
        return JsonResponse(responseData, status=400)

    else:

        responseData = {}
        responseData['success'] = 'false'
        responseData['mesage'] = 'Wrong Method'
        return JsonResponse(responseData, status=400)



def cartInsert(request):

    if request.method == 'POST':

        try:
            json_object = json.loads(request.body)
            try:
                carItem = Cart.objects.get(user_id=json_object["cart_user_id"], videogame_id=json_object["cart_videogame_id"])
            ##si no existe    
            except:
                newcarItem = Cart(user_id=json_object['cart_user_id'], videogame_id=json_object['cart_videogame_id'], quantity=json_object['cart_quantity'], videogame_name=json_object['cart_videogame_name'], videogame_image=json_object['cart_videogame_image'], videogame_price=json_object['cart_videogame_price'])
                newcarItem.save()
                responseData = {}
                responseData['success'] = 'true'
                responseData['message'] = 'Carro insertado'
                return JsonResponse(responseData, status=200)
            ##si existe
            carItem.quantity=json_object['cart_quantity']
            carItem.save()
            responseData = {}
            responseData['success'] = 'true'
            responseData['message'] = 'carro actualizado'
            return JsonResponse(responseData, status=200)
        except ValueError as e:
            responseData = {}
            responseData['success'] = 'false'
            responseData['data'] = 'Invalid Json'
            return JsonResponse(responseData, status=400)
    else:

        responseData = {}
        responseData['success'] = 'false'
        responseData['mesage'] = 'Wrong Method'
        return JsonResponse(responseData, status=400)


def cartAdd(request):

    if request.method == 'POST':

        try:
            json_object = json.loads(request.body)
            newcart = Cart(user_id=json_object['cart_user_id'], videogame_id=json_object['cart_videogame_id'], quantity=json_object['cart_quantity'], videogame_name=json_object['cart_videogame_name'], videogame_image=json_object['cart_videogame_image'], videogame_price=json_object['cart_videogame_price'])
            
            newcart.save()
            responseData = {}
            responseData['success'] = 'true'
            responseData['message'] = 'cart inserted'
            return JsonResponse(responseData, status=200)
        except ValueError as e:
            responseData = {}
            responseData['success'] = 'false'
            responseData['message'] = 'Invalid Json'
            return JsonResponse(responseData, status=400)

    else:

        responseData = {}
        responseData['success'] = 'false'
        responseData['mesage'] = 'Wrong Method'
        return JsonResponse(responseData, status=400)

def cartDelete(request):

    if request.method == 'DELETE':

        try:
            json_object = json.loads(request.body)
            try:
                one_entry = Cart.objects.get(id=json_object["cart_id"])
            except:
                responseData = {}
                responseData['success'] = 'false'
                responseData['message'] = 'The cart_id its not valid'
                return JsonResponse(responseData, status=400)
            Cart.objects.filter(id=json_object["cart_id"]).delete()
            responseData = {}
            responseData['success'] = 'true'
            responseData['message'] = 'The cart has been deleted'
            return JsonResponse(responseData, status=200)
        except ValueError as e:
            responseData = {}
            responseData['success'] = 'false'
            responseData['data'] = 'Invalid Json'
            return JsonResponse(responseData, status=400)
    else:

        responseData = {}
        responseData['success'] = 'false'
        responseData['mesage'] = 'Wrong Method'
        return JsonResponse(responseData, status=400)


def cartDeleteAll(request):

    if request.method == 'DELETE':

        try:
            json_object = json.loads(request.body)
            try:
                one_entry = Cart.objects.all().filter(user_id=json_object["cart_user_id"])
            except:
                responseData = {}
                responseData['success'] = 'false'
                responseData['message'] = 'The user_id its not valid'
                return JsonResponse(responseData, status=400)
            Cart.objects.all().filter(user_id=json_object["cart_user_id"]).delete()
            responseData = {}
            responseData['success'] = 'true'
            responseData['message'] = 'The carts has been deleted'
            return JsonResponse(responseData, status=200)
        except ValueError as e:
            responseData = {}
            responseData['success'] = 'false'
            responseData['data'] = 'Invalid Json'
            return JsonResponse(responseData, status=400)
    else:

        responseData = {}
        responseData['success'] = 'false'
        responseData['mesage'] = 'Wrong Method'
        return JsonResponse(responseData, status=400)

def cartGet(request):

    if request.method == 'POST':

        try:
            json_object = json.loads(request.body)
            try:
                one_entry = Cart.objects.all().filter(user_id=json_object["cart_user_id"]).values()
            except:
                responseData = {}
                responseData['success'] = 'false'
                responseData['message'] = 'The cart_user_id its not valid'
                return JsonResponse(responseData, status=400)
            responseData = {}
            responseData['success'] = 'true'
            responseData['data'] = list(one_entry)

           

            return JsonResponse(responseData, status=200)
        except ValueError as e:
            responseData = {}
            responseData['success'] = 'false'
            responseData['data'] = 'Invalid Json'
            return JsonResponse(responseData, status=400)
    else:

        responseData = {}
        responseData['success'] = 'false'
        responseData['mesage'] = 'Wrong Method'
        return JsonResponse(responseData, status=400)







def cartItems(request, cartid):

    if request.method == 'GET':

        try:
            one_entry = Cart.objects.all().filter(user_id=cartid)
        except:
            responseData = {}
            responseData['success'] = 'false'
            responseData['message'] = 'The user_id its not valid'
            return JsonResponse(responseData, status=400)

        responseData = {}
        responseData['success'] = 'true'
        responseData['data'] = list(Cart.objects.all().filter(user_id=cartid).values())
        

        return JsonResponse(responseData, status=200)

    else:

        responseData = {}
        responseData['success'] = 'false'
        responseData['mesage'] = 'Wrong Method'
        return JsonResponse(responseData, status=400)






def cartGetId(request, cartid):

    if request.method == 'GET':

        try:
            one_entry = Cart.objects.get(id=cartid)
        except:
            responseData = {}
            responseData['success'] = 'false'
            responseData['message'] = 'The cart_id its not valid'
            return JsonResponse(responseData, status=400)

        responseData = {}
        responseData['success'] = 'true'
        responseData['data'] = {}
        responseData['data']['user_id'] = one_entry.user_id
        responseData['data']['videogame_id'] = one_entry.videogame_id
        responseData['data']['quantity'] = one_entry.quantity
        return JsonResponse(responseData, status=200)

    else:

        responseData = {}
        responseData['success'] = 'false'
        responseData['mesage'] = 'Wrong Method'
        return JsonResponse(responseData, status=400)

def cartUpdate(request,cartid):

    if request.method == 'POST':
        try:
            one_entry = Cart.objects.get(id=cartid)
        except:
            responseData = {}
            responseData['success'] = 'false'
            responseData['message'] = 'The cart_id its not valid'
            return JsonResponse(responseData, status=400)
        try:
            json_object = json.loads(request.body)
            contador = 0
            
            try:
                value = json_object["cart_user_id"]
                Cart.objects.filter(id=cartid).update(user_id=json_object["cart_user_id"])
                contador = contador + 1
            except KeyError:
                responseData = {}

            try:
                value = json_object["cart_videogame_id"]
                Cart.objects.filter(id=cartid).update(videogame_id=json_object["cart_videogame_id"])
                contador = contador + 1
            except KeyError:
                responseData = {}

            try:
                value = json_object["cart_quantity"]
                Cart.objects.filter(id=cartid).update(quantity=json_object["cart_quantity"])
                contador = contador + 1
            except KeyError:
                responseData = {}

            if contador == 0:
                responseData = {}
                responseData['success'] = 'false'
                responseData['message'] = 'Nada por actualizar'
                return JsonResponse(responseData, status=400)
            else:
                responseData = {}
                responseData['success'] = 'true'
                responseData['message'] = 'Datos actualizados'
                return JsonResponse(responseData, status=200)

        except ValueError as e:
            responseData = {}
            responseData['success'] = 'false'
            responseData['data'] = 'Invalid Json'
            return JsonResponse(responseData, status=400)

    else:

        responseData = {}
        responseData['success'] = 'false'
        responseData['mesage'] = 'Wrong Method'
        return JsonResponse(responseData, status=400)
###############################################
def orders(request):

    if request.method == 'GET':

        apikey = request.headers.get('api_key')
        apikey = "33390d09esdioewu0qe0uqu0"
        if apikey is not None:

            if apikey != "33390d09esdioewu0qe0uqu0":
                responseData = {}
                responseData['success'] = 'false'
                responseData['message'] = 'API KEY NOT VALID'
                return JsonResponse(responseData, status=400)

            responseData = {}
            responseData['success'] = 'true'
            responseData['key'] = apikey
            responseData['data'] = list(Order.objects.all().values())
            return JsonResponse(responseData, status=200)

        responseData = {}
        responseData['success'] = 'false'
        responseData['message'] = 'No api Key'
        return JsonResponse(responseData, status=400)

    else:

        responseData = {}
        responseData['success'] = 'false'
        responseData['mesage'] = 'Wrong Method'
        return JsonResponse(responseData, status=400)


def orderAdd(request):

    if request.method == 'POST':

        try:
            json_object = json.loads(request.body)
            neworder = Order(user_id=json_object['order_user_id'], total=json_object['order_total'], items=json_object['order_items'], status=json_object['order_status'])
           
            neworder.save()
            responseData = {}
            responseData['success'] = 'true'
            responseData['message'] = 'order inserted'
            return JsonResponse(responseData, status=200)
        except ValueError as e:
            responseData = {}
            responseData['success'] = 'false'
            responseData['message'] = 'Invalid Json'
            return JsonResponse(responseData, status=400)

    else:

        responseData = {}
        responseData['success'] = 'false'
        responseData['mesage'] = 'Wrong Method'
        return JsonResponse(responseData, status=400)

def orderDelete(request):

    if request.method == 'DELETE':

        try:
            json_object = json.loads(request.body)
            try:
                one_entry = Order.objects.get(id=json_object["order_id"])
            except:
                responseData = {}
                responseData['success'] = 'false'
                responseData['message'] = 'The order_id its not valid'
                return JsonResponse(responseData, status=400)
            Users.objects.filter(id=json_object["order_id"]).delete()
            responseData = {}
            responseData['success'] = 'true'
            responseData['message'] = 'The order has been deleted'
            return JsonResponse(responseData, status=200)
        except ValueError as e:
            responseData = {}
            responseData['success'] = 'false'
            responseData['data'] = 'Invalid Json'
            return JsonResponse(responseData, status=400)
    else:

        responseData = {}
        responseData['success'] = 'false'
        responseData['mesage'] = 'Wrong Method'
        return JsonResponse(responseData, status=400)

def orderGet(request):

    if request.method == 'POST':

        try:
            json_object = json.loads(request.body)
            try:
                one_entry = Order.objects.all().filter(username=json_object["order_user_id"]).values()
            except:
                responseData = {}
                responseData['success'] = 'false'
                responseData['message'] = 'The user_id its not valid'
                
                return JsonResponse(responseData, status=400)
            responseData = {}
            responseData['success'] = 'true'
            responseData['data'] = list(one_entry)
           

            return JsonResponse(responseData, status=200)
        except ValueError as e:
            responseData = {}
            responseData['success'] = 'false'
            responseData['data'] = 'Invalid Json'
            return JsonResponse(responseData, status=400)
    else:

        responseData = {}
        responseData['success'] = 'false'
        responseData['mesage'] = 'Wrong Method'
        return JsonResponse(responseData, status=400)

def orderGetId(request, orderid):

    if request.method == 'GET':

        try:
            one_entry = Order.objects.get(user_id=orderid)
        except:
            responseData = {}
            responseData['success'] = 'false'
            responseData['message'] = 'The user_id its not valid'
            responseData['data'] = list(Order.objects.all().filter(user_id=orderid).values())
            return JsonResponse(responseData, status=400)

        responseData = {}
        responseData['success'] = 'true'
        responseData['data'] = list(Order.objects.all().filter(user_id=orderid).values())
        return JsonResponse(responseData, status=200)

    else:

        responseData = {}
        responseData['success'] = 'false'
        responseData['mesage'] = 'Wrong Method'
        return JsonResponse(responseData, status=400)

def orderUpdate(request,orderid):

    if request.method == 'POST':
        try:
            one_entry = Users.objects.get(id=orderid)
        except:
            responseData = {}
            responseData['success'] = 'false'
            responseData['message'] = 'The order_id its not valid'
            return JsonResponse(responseData, status=400)
        try:
            json_object = json.loads(request.body)
            contador = 0
            #AQUI VA EL CODIGO DEL UPDATE
            try:
                value = json_object["order_user_id"]
                Order.objects.filter(id=orderid).update(user_id=json_object["order_user_id"])
                contador = contador + 1
            except KeyError:
                responseData = {}

            try:
                value = json_object["order_total"]
                Order.objects.filter(id=orderid).update(total=json_object["order_total"])
                contador = contador + 1
            except KeyError:
                responseData = {}

            try:
                value = json_object["order_items"]
                Order.objects.filter(id=orderid).update(items=json_object["order_items"])
                contador = contador + 1
            except KeyError:
                responseData = {}

            try:
                value = json_object["order_status"]
                Order.objects.filter(id=orderid).update(status=json_object["order_status"])
                contador = contador + 1
            except KeyError:
                responseData = {}

            if contador == 0:
                responseData = {}
                responseData['success'] = 'false'
                responseData['message'] = 'Nada por actualizar'
                return JsonResponse(responseData, status=400)
            else:
                responseData = {}
                responseData['success'] = 'true'
                responseData['message'] = 'Datos actualizados'
                return JsonResponse(responseData, status=200)

        except ValueError as e:
            responseData = {}
            responseData['success'] = 'false'
            responseData['data'] = 'Invalid Json'
            return JsonResponse(responseData, status=400)

    else:

        responseData = {}
        responseData['success'] = 'false'
        responseData['mesage'] = 'Wrong Method'
        return JsonResponse(responseData, status=400)
###############################################
# videogames

def videogames(request):
    
    if request.method == 'GET':

        responseData = {}
        responseData['success'] = 'true'
        responseData['data'] = list(Videogames.objects.all().values())
        return JsonResponse(responseData, status=200)

    else:

        responseData = {}
        responseData['success'] = 'false'
        responseData['mesage'] = 'Wrong Method'
        return JsonResponse(responseData, status=400)

def videogamesAdd(request):

    if request.method == 'POST':

      newVideogame = Videogames(name=request.POST.get("name"), genre=request.POST.get("genre"), rating_id=request.POST.get("rating_id"), image=request.POST.get("image"), price=request.POST.get("price"))
      newVideogame.save()
    return redirect('/')

def videogamesDelete(request,videogameid):

    if request.method == 'POST':
        
        Videogames.objects.filter(id=videogameid).delete() #lo que está dentro del filter(id=), ese "id" debe ser escrito igual a como está declarado en mi modelo o bd
        
    return redirect('/')

def videogamesGet(request):

    if request.method == 'POST':

        try:
            json_object = json.loads(request.body)
            try:
                one_entry = Videogames.objects.get(id=json_object["videogame_id"])
            except:
                responseData = {}
                responseData['success'] = 'false'
                responseData['message'] = 'The videogame_id its not valid'
                return JsonResponse(responseData, status=400)
            responseData = {}
            responseData['success'] = 'true'
            responseData['data'] = {}
            responseData['data']['name'] = one_entry.name
            responseData['data']['genre'] = one_entry.genre
            responseData['data']['rating_id'] = one_entry.rating_id
            responseData['data']['image'] = one_entry.rating_id
            responseData['data']['price'] = one_entry.rating_id
           

            return JsonResponse(responseData, status=200)
        except ValueError as e:
            responseData = {}
            responseData['success'] = 'false'
            responseData['data'] = 'Invalid Json'
            return JsonResponse(responseData, status=400)
    else:

        responseData = {}
        responseData['success'] = 'false'
        responseData['mesage'] = 'Wrong Method'
        return JsonResponse(responseData, status=400)

def videogamesGetId(request, videogameid):

    if request.method == 'GET':
       
        try:
            one_entry = Videogames.objects.get(id=videogameid)
        except:
            responseData = {}
            responseData['success'] = 'false'
            responseData['message'] = 'The videogame_id its not valid'
            return JsonResponse(responseData, status=400)
        
        responseData = {}
        responseData['success'] = 'true'
        responseData['data'] = {}
        responseData['data']['name'] = one_entry.name
        responseData['data']['genre'] = one_entry.genre
        responseData['data']['rating_id'] = one_entry.rating_id
        responseData['data']['image'] = one_entry.image
        responseData['data']['price'] = one_entry.price

        return JsonResponse(responseData, status=200)
      
    else:

        responseData = {}
        responseData['success'] = 'false'
        responseData['mesage'] = 'Wrong Method'
        return JsonResponse(responseData, status=400)

def videogamesUpdate(request, videogameid):
    if request.method == 'POST':
       
        try:
            one_entry = Videogames.objects.get(id=videogameid)
           
        except:
            responseData = {}
            responseData['success'] = 'false'
            responseData['message'] = 'The videogame_id its not valid'
            return JsonResponse(responseData, status=400)
        try:
            json_object = json.loads(request.body)
            contador = 0
            try:
                value = json_object["videogame_name"]
                Videogames.objects.filter(id=videogameid).update(name=json_object["videogame_name"])
                contador = contador + 1
            except KeyError:
                responseData = {}
            try:
                value = json_object["videogame_genre"]
                Videogames.objects.filter(id=videogameid).update(size=json_object["videogame_genre"])
                contador = contador + 1
            except KeyError:
                responseData = {}
            try:
                value = json_object["videogame_rating"]
                Videogames.objects.filter(id=videogameid).update(type_id=json_object["videogame_rating"])
                contador = contador + 1
            except KeyError:
                responseData = {}


            if contador == 0:
                responseData = {}
                responseData['success'] = 'false'
                responseData['mesage'] = 'nada por actuailzar'
                return JsonResponse(responseData, status=200)
            else:
                responseData = {}
                responseData['success'] = 'true'
                responseData['mesage'] = 'datos actualizados'
                return JsonResponse(responseData, status=200)



        except ValueError:
            responseData = {}
            responseData['success'] = 'false'
            responseData['mesage'] = 'invalid json'
            return JsonResponse(responseData, status=400)
        
      
    else:

        responseData = {}
        responseData['success'] = 'false'
        responseData['mesage'] = 'Wrong Method'
        return JsonResponse(responseData, status=400)
########################################################
def rating(request):

    if request.method == 'GET':

        responseData = {}
        responseData['success'] = 'true'
        responseData['data'] = list(Rating.objects.all().values())
        return JsonResponse(responseData, status=200)

    else:

        responseData = {}
        responseData['success'] = 'false'
        responseData['mesage'] = 'Wrong Method'
        return JsonResponse(responseData, status=400)

def ratingAdd(request):

    if request.method == 'POST':

        try:
            json_object = json.loads(request.body)
            newRating = Rating(name=json_object['rating_name'], image=json_object['rating_image'])
            newRating.save()
            responseData = {}
            responseData['success'] = 'true'
            responseData['message'] = 'rating inserted'
            return JsonResponse(responseData, status=200)
        except ValueError as e:
            responseData = {}
            responseData['success'] = 'false'
            responseData['message'] = 'Invalid Json'
            return JsonResponse(responseData, status=400)

    else:

        responseData = {}
        responseData['success'] = 'false'
        responseData['mesage'] = 'Wrong Method'
        return JsonResponse(responseData, status=400)

def ratingDelete(request):

    if request.method == 'DELETE':

        try:
            json_object = json.loads(request.body)
            try:
                one_entry = Rating.objects.get(id=json_object["rating_id"])
            except:
                responseData = {}
                responseData['success'] = 'false'
                responseData['message'] = 'The rating_id its not valid'
                return JsonResponse(responseData, status=400)
            Rating.objects.filter(id=json_object["rating_id"]).delete()
            responseData = {}
            responseData['success'] = 'true'
            responseData['message'] = 'The rating has been deleted'
            return JsonResponse(responseData, status=200)
        except ValueError as e:
            responseData = {}
            responseData['success'] = 'false'
            responseData['data'] = 'Invalid Json'
            return JsonResponse(responseData, status=400)
    else:

        responseData = {}
        responseData['success'] = 'false'
        responseData['mesage'] = 'Wrong Method'
        return JsonResponse(responseData, status=400)
########################################################
def add(request):
    form = VideogameForm()
    return render(request, "add.html", {'form' : form} )

def delete(request, videogameid, videogame):
    
    return render(request, "delete.html", {'videogameid': videogameid, 'videogame':videogame} )

def update(request, videogameid):
    
    videogameedit = Videogames.objects.get(id = videogameid)

    if request.method == 'GET':
        form = VideogameForm(instance = videogameedit)
    else:
        form = VideogameForm(request.POST, instance = videogameedit)
        if form.is_valid():
            form.save()
        return redirect('/')




    return render(request, "editar.html", {'videogameid': videogameid, 'form' : form} )