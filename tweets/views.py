from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from rest_framework.decorators import api_view, permission_classes#, authentication_classes era para SessionAuthentication
from rest_framework.permissions import IsAuthenticated
#from rest_framework.authentication import SessionAuthentication # SessionAuthentication no necesito especificar porque es luego el que se usa por defecto como se puede ver en settings.py
from rest_framework.response import Response
from .forms import TweetForm
from .models import Tweet
from .serializers import TweetSerializer, TweetActionSerializer

ALLOWED_HOSTS=settings.ALLOWED_HOSTS

# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request,"pages/home.html",context={},status=200)

@api_view(['POST'])#http method the client must send == POST
#@authentication_classes([SessionAuthentication]) # SessionAuthentication no necesito especificar porque es luego el que se usa por defecto
@permission_classes([IsAuthenticated]) #hay otros decorators como IsAdminUser, IsAuthenticatedOrReadOnly
def tweet_create_view(request, *args, **kwargs):
    '''
    Texto a mostrar en la salida html:
    This view add a new tweet
    REST API - Create View con Django REST Framework (DRF)
    '''
    serializer=TweetSerializer(data=request.POST)#data=request.POST tiene que estar dentro no puede estar arriba sino tira el siguiente server error: Cannot call `.is_valid()` as no `data=` keyword argument was passed when instantiating the serializer instance.
    if serializer.is_valid(raise_exception=True):#raise_exception=True significa que va a devolver los errores de validacion sin necesidad de especificar como se habia hecho antes en la ultima parte del view tweet_create_view_pure_django
        serializer.save(user=request.user)#se le pasa el user como parametro sino tira error ya que el user no puede ser null, tambien se le puede pasar el content como content='abc' pero ahi no tomaria el content del formulario, sino el que le pasamos aca
        return Response(serializer.data,status=201)#parametro status=201 SI seria necesario
    return Response({}, status=400)

@api_view(['GET'])
def tweet_list_view(request,*args, **kwargs):
    '''
    Texto a mostrar en la salida html:
    This view lists all tweet
    REST API - List View con Django REST Framework (DRF)
    '''
    qs=Tweet.objects.all()
    serializer=TweetSerializer(qs, many=True)
    return Response(serializer.data, status=200)#parametro status=200 no seria necesario en get requests

@api_view(['GET'])
def tweet_detail_view(request,tweet_id,*args, **kwargs):
    '''
    Texto a mostrar en la salida html:
    This view returns a tweet requested by id
    REST API - Detail View con Django REST Framework (DRF)
    '''
    qs=Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    obj=qs.first()
    serializer=TweetSerializer(obj)
    return Response(serializer.data,status=200)#parametro status=200 no seria necesario en get requests

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_action_view(request,*args, **kwargs):
    '''
    Texto a mostrar en la salida html:
    This view has the following options: like, unlike, retweet
    id is required
    REST API - Action View con Django REST Framework (DRF)
    '''
    serializer=TweetActionSerializer(data=request.POST)
    if serializer.is_valid(raise_exception=True):
        data=serializer.validated_data
        tweet_id=data.get("id")
        action=data.get("action")

        qs=Tweet.objects.filter(id=tweet_id)
        if not qs.exists():
            return Response({}, status=404)
        obj=qs.first()
        if action=="like":
            obj.likes.add(request.user)    
        elif action=="unlike":   
            obj.likes.remove(request.user)
        elif action=="retweet":   
            #this is todo
            pass
    return Response({"message":"Tweet removed"},status=200)#parametro status=200 no seria necesario en get requests

@api_view(['DELETE','POST'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request,tweet_id,*args, **kwargs):
    '''
    Texto a mostrar en la salida html:
    REST API - Delete View con Django REST Framework (DRF)
    '''
    qs=Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    qs=qs.filter(user=request.user)
    if not qs.exists():
        return Response({"message":"You can not delete this tweet"}, status=401)
    obj=qs.first()
    obj.delete()
    return Response({"message":"Tweet removed"},status=200)#parametro status=200 no seria necesario en get requests

def tweet_create_view_pure_django(request, *args, **kwargs): #esta hecho sin Django REST Framework (DRF) y preparado para renderizar html y Json, o sea via api y via /create-tweet
    '''''
    REST API Create View SIN Django REST Framework (DRF)
    '''''
    user=request.user #para que user no sea AnonymousUser
    if not request.user.is_authenticated:
        user=None
        if request.is_ajax():
            return JsonResponse({},status=403)#forbidden
        return redirect(settings.LOGIN_URL)
    form = TweetForm(request.POST or None) # el formulario puede ser inicializado con datos o sin
    next_url = request.POST.get("next") or None # next es el hiddenfield del form en home osea sería /
    if form.is_valid(): 
        obj=form.save(commit=False)
        obj.user=user
        obj=form.save()
        if request.is_ajax():#retorna true si viene del javascript con los headers especiales que pide django para un ajax request
            return JsonResponse(obj.serialize(), status=201) #201 es el estado para created items
        if next_url != None and is_safe_url(next_url,ALLOWED_HOSTS): # si va a un host seguro, seteado en settings.py > ALLOWED_HOSTS
            return redirect(next_url)
        form=TweetForm() #si viene con datos guarda y crea un TweetForm vacio
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400) #Retorna en Json si hay un error en el servidor
    return render(request, 'components/form.html',context={"form":form})

def tweet_list_view_pure_django(request,*args, **kwargs):#esta hecho sin Django REST Framework (DRF)
    """
    REST API VIEW
    Consume by JavaScript or Swift or Java/iOS/Android
    return json data
    """
    qs=Tweet.objects.all()
    tweets_list=[x.serialize() for x in qs]
    data={
        "isUser": False,
        "response":tweets_list
    }
    return JsonResponse(data)

def tweet_detail_view_pure_django(request, tweet_id, *args, **kwargs): #tweet_id debe ser el mismo nombre del id especificado en url 'tweets/<int:tweet_id>'
    """
    REST API VIEW
    Consume by JavaScript or Swift or Java/iOS/Android
    return json data
    """
    data={
        "id": tweet_id,
    }
    status=200
    try:
        obj=Tweet.objects.get(id=tweet_id)
        data['content']=obj.content
    except:
        data['message']="Not found"
        status=404
    return JsonResponse(data, status=status) # similar a Json.dumps content_type='application_json'