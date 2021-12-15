from django.contrib import admin

from games.models import CustomUser, Draw, Exclusion, Game, Santa


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass


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
