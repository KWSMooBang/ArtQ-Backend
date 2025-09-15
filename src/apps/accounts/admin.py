from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'nickname', 'email', 
                    'phone', 'birth_date', 'email_verified', 'phone_verified')
    search_fields = ('username', 'nickname', 'email', 'phone')