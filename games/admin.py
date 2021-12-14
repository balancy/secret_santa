from django.contrib import admin

from games.models import Game, Santa, Draw


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    pass


@admin.register(Santa)
class SantaAdmin(admin.ModelAdmin):
    pass


@admin.register(Draw)
class DrawAdmin(admin.ModelAdmin):
    pass
