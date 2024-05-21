from django.contrib import admin

from .models import Comments, Articles,FavoriteArticle

class FavouriteArticleInline(admin.TabularInline):
    model = FavoriteArticle
    extra = 0
admin.site.register(FavoriteArticle)
admin.site.register(Comments)
admin.site.register(Articles)

