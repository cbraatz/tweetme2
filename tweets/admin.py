from django.contrib import admin
from .models import Tweet, TweetLike
# Register your models here.

class TweetLikeAdmin(admin.TabularInline):
    model = TweetLike

class TweetAdmin(admin.ModelAdmin):
    inlines = [TweetLikeAdmin]
    list_display=['__str__','user'] #define las columnas a ser mostradas en admin > Tweet
    search_fields=['content','user__username','user__email'] # define los campos por los que se va a poder buscar dentro de admin > Tweet. O sea busca por Tweet.content, Tweet.user.username y Tweet.user.email
    class Meta:
        model=Tweet

admin.site.register(Tweet, TweetAdmin)