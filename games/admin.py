from django.contrib import admin

from games.models import CustomUser, Draw, Exclusion, Game, Santa


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')
    list_display_links = ('id', 'username')

    ordering = ('username',)


@admin.register(Draw)
class DrawAdmin(admin.ModelAdmin):
    list_display = ('id', 'game', 'giver', 'receiver')
    list_display_links = ('id', 'game')


@admin.register(Exclusion)
class ExclusionAdmin(admin.ModelAdmin):
    list_display = ('id', 'game', 'giver', 'receiver')
    list_display_links = ('id', 'game')


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'coordinator',
        'max_price',
        'draw_date',
        'gift_date',
    )
    list_display_links = ('id', 'name')

    ordering = ('name',)


@admin.register(Santa)
class SantaAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_games')
    list_display_links = ('id', 'user')

    def get_games(self, obj):
        return "; ".join([game.name for game in obj.games.all()])

    ordering = ('user__username',)
