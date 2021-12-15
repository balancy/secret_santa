from django.contrib import admin

from games.models import Draw, Exclusion, Game, Santa


@admin.register(Draw)
class DrawAdmin(admin.ModelAdmin):
    pass


@admin.register(Exclusion)
class ExclusionAdmin(admin.ModelAdmin):
    pass


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    pass


@admin.register(Santa)
class SantaAdmin(admin.ModelAdmin):
    pass
