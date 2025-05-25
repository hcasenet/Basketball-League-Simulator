from django.contrib import admin

#Hinsley Casenet - U59220930
#project/admin.py

# Register your models here.


from .models import Player, Team, League, Game
admin.site.register(Player)
admin.site.register(Team)
admin.site.register(League)
admin.site.register(Game)
