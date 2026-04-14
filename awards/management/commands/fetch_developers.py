import time
import requests
from django.core.management.base import BaseCommand

API_KEY = "163a906d602046b08f47ad264261846d"

# Manual corrections - API data will not override these values
MANUAL_CORRECTIONS = {
    1: "BioWare",  # Dragon Age: Inquisition
    2: "FromSoftware",  # Dark Souls II
    3: "Creative Assembly",  # Alien: Isolation
    14: "Blizzard Entertainment",  # Overwatch
    17: "Playdead",  # Inside
    18: "FromSoftware",  # Dark Souls III
    28: "Santa Monica Studio",  # God of War
    36: "Remedy Entertainment",  # Control
    44: "Hazelight Studios",  # It Takes Two
    45: "Housemarque",  # Returnal
    50: "Santa Monica Studio",  # God of War Ragnarök
    52: "BlueTwelve Studio",  # Stray
    86: "Bungie",  # Destiny
    109: "Ghost Town Games",  # Overcooked
    115: "Blizzard Entertainment",  # World of Warcraft: Legion
    126: "Arkane Studios",  # Prey
    128: "Hazelight Studios",  # A Way Out
    130: "Lucas Pope",  # Return of the Obra Dinn
    133: "Motion Twin",  # Dead Cells
    141: "Obsidian Entertainment",  # The Outer Worlds
    153: "Square Enix",  # Kingdom Hearts III
    164: "Acid Nerve",  # Death's Door
    172: "Sam Barlow",  # Immortality
    181: "Square Enix",  # Live A Live
    212: "Nintendo",  # Donkey Kong Bananza
    213: "Supergiant Games",  # Hades II
}


class Command(BaseCommand):
    help = "Fetches and updates ONLY developer details from RAWG API for all games."

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            help='Re-fetch all games, even if they already have a developer.',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Override manual corrections from RAWG API data.',
        )

    def handle(self, *args, **kwargs):
        from awards.models import Game

        force_override = kwargs.get('force', False)

        if kwargs['all']:
            games = Game.objects.all()
            self.stdout.write("Re-fetching developers for all games...\n")
        else:
            games = Game.objects.filter(developers__isnull=True) | Game.objects.filter(developers__exact="")
            self.stdout.write("Fetching developers only for games with missing developer data...\n")

        if force_override:
            self.stdout.write(self.style.WARNING("Manuel corrections will be OVERRIDDEN by API data!\n"))
        else:
            self.stdout.write("Skipping manual corrections. Use --force to override them.\n\n")

        total = games.count()
        self.stdout.write(f"Processing {total} games for developer info...\n")

        updated = 0
        not_found = []
        skipped = 0

        for index, game in enumerate(games, 1):
            # Check: is this game manually corrected?
            if game.id in MANUAL_CORRECTIONS and not force_override:
                manual_dev = MANUAL_CORRECTIONS[game.id]
                self.stdout.write(f"[{index}/{total}] {game.name}... (skipped - manual correction)")
                skipped += 1
                continue

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

                time.sleep(0.5)

                # Step 2: Fetch game detail page for developers array
                detail_response = requests.get(
                    f"https://api.rawg.io/api/games/{rawg_id}",
                    params={"key": API_KEY}
                )
                detail_response.raise_for_status()
                detail_data = detail_response.json()

                # Extract developers
                fetched_devs = ", ".join([d["name"] for d in detail_data.get("developers", [])])

                if fetched_devs:
                    game.developers = fetched_devs
                    # Make sure we ONLY update the developers field by using update_fields
                    game.save(update_fields=['developers'])
                    updated += 1
                    self.stdout.write(self.style.SUCCESS(f"  ✓ Updated developer: {fetched_devs}"))
                else:
                    self.stdout.write(self.style.WARNING(f"  ✗ Found on RAWG but no developer info."))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  ! Error: {e}"))

            time.sleep(0.5)

        self.stdout.write(self.style.SUCCESS(f"\nDone! Updated: {updated}/{total}, Skipped (manual): {skipped}"))

        if not_found:
            self.stdout.write(self.style.WARNING(f"\nNot found on RAWG ({len(not_found)}):"))
            for name in not_found:
                self.stdout.write(f"  - {name}")
