import os
from django.core.management.base import BaseCommand
import requests
import time
 
API_KEY = os.environ.get("RAWG_API_KEY", "")
 
STORE_MAP = {
    1: "steam",
    2: "xbox",
    3: "playstation",
    6: "nintendo",
}
 
 
class Command(BaseCommand):
    help = "Fetch Steam, PlayStation, Xbox and Nintendo store links for all games"
 
    def handle(self, *args, **kwargs):
        from awards.models import Game
 
        games = Game.objects.filter(
            steam_url__isnull=True,
            playstation_url__isnull=True,
            xbox_url__isnull=True,
            nintendo_url__isnull=True,
        )
        total = games.count()
        self.stdout.write(f"Fetching store links for {total} games...\n")
 
        updated = 0
        not_found = []
 
        for game in games:
            try:
                search_response = requests.get(
                    "https://api.rawg.io/api/games",
                    params={
                        "key": API_KEY,
                        "search": game.name,
                        "page_size": 1,
                    }
                )
                results = search_response.json().get("results", [])
 
                if not results:
                    not_found.append(game.name)
                    self.stdout.write(self.style.WARNING(f"  ✗ Not found: {game.name}"))
                    time.sleep(0.3)
                    continue
 
                rawg_id = results[0]["id"]
                time.sleep(0.3)
 
                stores_response = requests.get(
                    f"https://api.rawg.io/api/games/{rawg_id}/stores",
                    params={"key": API_KEY}
                )
                stores_data = stores_response.json().get("results", [])
 
                found = []
                for store in stores_data:
                    store_name = STORE_MAP.get(store["store_id"])
                    if store_name == "steam":
                        game.steam_url = store["url"]
                        found.append("steam")
                    elif store_name == "playstation":
                        game.playstation_url = store["url"]
                        found.append("playstation")
                    elif store_name == "xbox":
                        game.xbox_url = store["url"]
                        found.append("xbox")
                    elif store_name == "nintendo":
                        game.nintendo_url = store["url"]
                        found.append("nintendo")
 
                if found:
                    game.save()
                    updated += 1
                    self.stdout.write(f"  ✓ {game.name} → [{', '.join(found)}]")
                else:
                    not_found.append(game.name)
                    self.stdout.write(self.style.WARNING(f"  ✗ No links found: {game.name}"))
 
            except Exception as e:
                not_found.append(game.name)
                self.stdout.write(self.style.ERROR(f"  ✗ Error for {game.name}: {e}"))
 
            time.sleep(0.3)
 
        self.stdout.write(self.style.SUCCESS(f"\nDone! Updated: {updated}/{total}"))
 
        if not_found:
            self.stdout.write(self.style.WARNING(f"\nNo links found for ({len(not_found)}):"))
            for name in not_found:
                self.stdout.write(f"  - {name}")