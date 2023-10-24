from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile
# Register your models here.

#unregister Groups:
admin.site.unregister(Group)


#Mix Profile and User (place here so that it exists before we use it in UserAdmin)
class ProfileInline(admin.StackedInline):
    model=Profile

#Extend User Model
class UserAdmin(admin.ModelAdmin):
    model = User
    #display only username field in admin:
    fields = ['username']
    inlines = [ProfileInline]

#unregister initial User:
admin.site.unregister(User)

#register User again:
admin.site.register(User, UserAdmin)

#register Profile:
admin.site.register(Profile)


