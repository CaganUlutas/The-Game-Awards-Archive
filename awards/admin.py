from django.contrib import admin
from .models import Game, AwardYear, Category, Nomination

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    # The columns to display in the list view
    list_display = ('name', 'metacritic_score', 'released', 'rating')
    # Adds a search bar for game names
    search_fields = ('name',)
    # Number of items to display per page (Overrides default 100)
    list_per_page = 200 

@admin.register(Nomination)
class NominationAdmin(admin.ModelAdmin):
    list_display = ('game', 'category', 'year', 'is_winner')
    # Adds a sidebar to filter nominations by year, category, or win status
    list_filter = ('year', 'category', 'is_winner')
    search_fields = ('game__name', 'category__name')
    list_per_page = 200

admin.site.register(AwardYear)
admin.site.register(Category)

