from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from .forms import TweetForm
from .models import Tweet

ALLOWED_HOSTS=settings.ALLOWED_HOSTS

# Create your views here.
def home_view(request, *args, **kwargs):
    #return HttpResponse("<h1>Home View</h1>")
    return render(request,"pages/home.html",context={},status=200)

def tweet_create_view(request, *args, **kwargs):
    form = TweetForm(request.POST or None) # el formulario puede ser inicializado con datos o sin
    next_url = request.POST.get("next") or None # next es el hiddenfield del form en home osea sería /
    if form.is_valid():
        obj=form.save()
        if next_url != None and is_safe_url(next_url,ALLOWED_HOSTS): # si va a un host seguro, seteado en settings.py > ALLOWED_HOSTS
            return redirect(next_url)
        form=TweetForm() #si viene con datos guarda y crea un TweetForm vacio
    return render(request, 'components/form.html',context={"form":form})

def tweet_list_view(request,*args, **kwargs):
    """
    REST API VIEW
    Consume by JavaScript or Swift or Java/iOS/Android
    return json data
    """
    qs=Tweet.objects.all()
    tweets_list=[{"id":x.id,"content":x.content,"likes":12} for x in qs]
    data={
        "isUser": False,
        "response":tweets_list
    }
    return JsonResponse(data)

def tweet_detail_view(request, tweet_id, *args, **kwargs): #tweet_id debe ser el mismo nombre del id especificado en url 'tweets/<int:tweet_id>'
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