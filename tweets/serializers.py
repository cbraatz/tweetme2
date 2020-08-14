from django.conf import settings
from rest_framework import serializers

from .models import Tweet

MAX_TWEET_LENGTH=settings.MAX_TWEET_LENGTH
TWEET_ACTION_OPTIONS=settings.TWEET_ACTION_OPTIONS
class TweetActionSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    action=serializers.CharField()

    def validate_action(self,value):
        value=value.lower().strip() # "Like " -> "like"
        if not value in TWEET_ACTION_OPTIONS:
            raise serializers.ValidationError("This is not a valid option for tweets")
        else:
            return value

class TweetSerializer(serializers.ModelSerializer):#similar a lo que hicimos en forms.py antes de empezar usar Django Rest Framework
    likes=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model= Tweet
        fields=['id','content','likes']

    def get_likes(self,obj):#No necesitamos la lista de likes sino el numero de likes de ese tweet
        return obj.likes.count()

    def validate_content(self,value):
        if len(value) > MAX_TWEET_LENGTH:
            raise serializers.ValidationError("This tweet is too long...!")
        return value
