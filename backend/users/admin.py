from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from backend.main_app.admin import FavouriteArticleInline

class CustomUserAdmin(UserAdmin):
    inlines = [FavouriteArticleInline]

    def change_view(self , request , object_id , form_url='' , extra_context=None):
        self.exclude = ('password' ,)
        return super().change_view(request , object_id , form_url , extra_context)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)