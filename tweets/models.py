from django.db import models
from django.conf import settings

import random

User=settings.AUTH_USER_MODEL #para usar el build-in feature que trae django, ej superuser, que luego de correr migrations lo seteo como el user de los tweets existentes en la bd

class TweetLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE) #"Tweet" because Tweet is bellow TweetLike
    timestamp = models.DateTimeField(auto_now_add=True)

# Create your models here.
class Tweet(models.Model):
    # id = models.AutoField(primary_key=True)
    parent= models.ForeignKey("self",null=True,on_delete=models.SET_NULL)#se referencia a si mismo y si se borra el padre, el fk queda null
    user = models.ForeignKey(User, on_delete=models.CASCADE) # a user can have many tweets, si se borra el user se borran tambien todos sus tweets
    likes = models.ManyToManyField(User, related_name="tweet_user", blank=True, through=TweetLike)
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    #def __str__(self):
        #return self.content

    class Meta:
        ordering= ['-id']

    @property
    def is_retweet(self):
        return self.parent != None

    #def serialize(self): #ya no se necesita esto
    #    return{
    #        "id": self.id,
    #        "content":self.content,
    #        "likes": random.randint(1,200)
    #    }
