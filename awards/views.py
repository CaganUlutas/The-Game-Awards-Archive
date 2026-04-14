import re
from django.shortcuts import render, get_object_or_404
from .models import AwardYear, Category, Nomination, Game
from django.db.models import Q
 
 
def home(request):
    latest_year = AwardYear.objects.all().order_by('-year').first()
    if latest_year:
        return render_year_page(request, latest_year)
    else:
        return render(request, 'awards/home.html', {'years': []})

def search(request):
    query = request.GET.get('q', '')
    results = Game.objects.none()
    if query:
        results = Game.objects.filter(name__icontains=query)
    
    return render(request, 'awards/search_results.html', {
        'query': query,
        'results': results,
    })

def render_year_page(request, year_obj):
    all_years = AwardYear.objects.all().order_by('-year')
    year_with_data = AwardYear.objects.prefetch_related('nomination_set__game', 'nomination_set__category').get(id=year_obj.id)
    goty_winner = None
    goty_trailer_id = None
    for nom in year_with_data.nomination_set.all(): 
        if nom.category.name == "Game of the Year" and nom.is_winner:
            goty_winner = nom
            if nom.game.trailer_url:
                if 'embed/' in nom.game.trailer_url:
                    base_id = nom.game.trailer_url.split('embed/')[-1]
                    goty_trailer_id = base_id.split('?')[0]
                elif 'watch?v=' in nom.game.trailer_url:
                    goty_trailer_id = nom.game.trailer_url.split('watch?v=')[-1].split('&')[0]
            break
    
    return render(request, 'awards/home.html', {
        'selected_year': year_with_data,
        'all_years': all_years,           
        'years': all_years,               
        'goty_winner': goty_winner,
        'goty_trailer_id': goty_trailer_id,
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

def hall_of_fame(request):
    #Fetches all 'Game of the Year' winners, ordered by year (newest first).   
    goty_winners = Nomination.objects.filter(
        category__name="Game of the Year",
        is_winner=True
    ).order_by('-year__year') # Orders by the year field descending (e.g., 2023, 2022, 2021)

    context = {
        'winners': goty_winners
    }
    return render(request, 'awards/hall_of_fame.html', context)