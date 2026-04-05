import re
from django.shortcuts import render, get_object_or_404
from .models import AwardYear, Category, Nomination, Game
 
 
def home(request):
    years = AwardYear.objects.all().order_by('-year')
    categories = Category.objects.all().order_by('name')
    return render(request, 'awards/home.html', {
        'years': years,
        'categories': categories,
    })

def render_year_page(request, year_obj):
    all_years = AwardYear.objects.all().order_by('-year')
    year_with_data = AwardYear.objects.prefetch_related('nomination_set__game', 'nomination_set__category').get(id=year_obj.id)
    goty_winner = None
    for nom in year_with_data.nomination_set.all(): 
        if nom.category.name == "Game of the Year" and nom.is_winner:
            goty_winner = nom
            break
    
    return render(request, 'awards/home.html', {
        'selected_year': year_with_data,
        'all_years': all_years,           
        'years': all_years,               
        'goty_winner': goty_winner,
    })

def year_detail(request, year):
    selected_year = get_object_or_404(AwardYear, year=year)
    return render_year_page(request, selected_year)
 

def parse_hltb_hours(value):
    if not value:
        return None
    if isinstance(value, str):
        match = re.search(r"[0-9]+(?:[.,][0-9]+)?", value)
        if not match:
            return None
        value = match.group(0).replace(',', '.')
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return None
 

def game_detail(request, slug):
    game = get_object_or_404(Game, slug=slug)
    nominations = Nomination.objects.filter(
        game=game
    ).select_related('category', 'year').order_by('-year__year')
 
    # Extract YouTube video ID from any URL format
    trailer_id = None
    if game.trailer_url:
        if 'embed/' in game.trailer_url:
            trailer_id = game.trailer_url.split('embed/')[-1]
        elif 'watch?v=' in game.trailer_url:
            trailer_id = game.trailer_url.split('watch?v=')[-1]
 
    return render(request, 'awards/game_details.html', {
        'game': game,
        'nominations': nominations,
        'genres': game.genres.split(', ') if game.genres else [],      
        'platforms': game.platforms.split(', ') if game.platforms else [],
        'total_nominations': nominations.count(),
        'total_wins': nominations.filter(is_winner=True).count(),
        'trailer_id': trailer_id,
        'hltb_main_hours': parse_hltb_hours(game.hltb_main),
        'hltb_extra_hours': parse_hltb_hours(game.hltb_extra),
        'hltb_completionist_hours': parse_hltb_hours(game.hltb_completionist),
    })