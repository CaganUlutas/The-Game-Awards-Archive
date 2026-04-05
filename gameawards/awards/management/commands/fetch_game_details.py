import time
import requests
from django.core.management.base import BaseCommand
 
API_KEY = "163a906d602046b08f47ad264261846d"
 
 
class Command(BaseCommand):
    help = "Fetches and updates game details from RAWG API for all games in the database."
 
    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            help='Re-fetch all games, including ones already updated.',
        )
 
    def handle(self, *args, **kwargs):
        from awards.models import Game
 
        if kwargs['all']:
            games = Game.objects.all()
            self.stdout.write("Re-fetching all games from scratch...\n")
        else:
            games = Game.objects.filter(background_image__isnull=True) | Game.objects.filter(description__isnull=True)
            self.stdout.write("Fetching only games with missing data...\n")
 
        total = games.count()
        self.stdout.write(f"Processing {total} games...\n")
 
        updated = 0
        not_found = []
 
        for index, game in enumerate(games, 1):
            self.stdout.write(f"[{index}/{total}] {game.name}...")
 
            try:
                # Step 1: Search for the game to get its RAWG ID
                search_response = requests.get(
                    "https://api.rawg.io/api/games",
                    params={
                        "key": API_KEY,
                        "search": game.name,
                        "page_size": 1,
                        "search_exact": True,
                    }
                )
                search_response.raise_for_status()
                search_data = search_response.json()
 
                # Fallback to fuzzy search if exact match returns nothing
                if not search_data.get("results"):
                    search_response = requests.get(
                        "https://api.rawg.io/api/games",
                        params={
                            "key": API_KEY,
                            "search": game.name,
                            "page_size": 1,
                        }
                    )
                    search_response.raise_for_status()
                    search_data = search_response.json()
 
                if not search_data.get("results"):
                    not_found.append(game.name)
                    self.stdout.write(self.style.WARNING(f"  ✗ Not found on RAWG."))
                    time.sleep(0.5)
                    continue
 
                rawg_game = search_data["results"][0]
                rawg_id = rawg_game["id"]
 
                # Update fields from search result
                game.background_image = rawg_game.get("background_image") or None
                game.rating = rawg_game.get("rating")
                game.ratings_count = rawg_game.get("ratings_count")
                game.genres = ", ".join([g["name"] for g in rawg_game.get("genres", [])])
                game.platforms = ", ".join([p["platform"]["name"] for p in rawg_game.get("platforms", [])])
 
                # Only update if not manually set
                if game.metacritic_score is None:
                    game.metacritic_score = rawg_game.get("metacritic")
                if game.released is None:
                    game.released = rawg_game.get("released") or None
 
                time.sleep(0.5)
 
                # Step 2: Fetch game detail page for description_raw
                detail_response = requests.get(
                    f"https://api.rawg.io/api/games/{rawg_id}",
                    params={"key": API_KEY}
                )
                detail_response.raise_for_status()
                detail_data = detail_response.json()
 
                raw_desc = detail_data.get("description_raw", "") or ""
                if raw_desc:
                    trimmed = raw_desc[:500].rsplit(".", 1)
                    game.description = trimmed[0] + "." if len(trimmed) > 1 else raw_desc[:500]
                else:
                    game.description = None
 
                game.save()
                updated += 1
                self.stdout.write(self.style.SUCCESS(f"  ✓ Updated."))
 
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  ! Error: {e}"))
 
            time.sleep(0.5)
 
        self.stdout.write(self.style.SUCCESS(f"\nDone! Updated: {updated}/{total}"))
 
        if not_found:
            self.stdout.write(self.style.WARNING(f"\nNot found on RAWG ({len(not_found)}):"))
            for name in not_found:
                self.stdout.write(f"  - {name}")
 