import re
import time
import requests
from django.core.management.base import BaseCommand


def parse_steam_appid(steam_url):
    """Extract Steam App ID from a Steam store URL."""
    if not steam_url:
        return None
    match = re.search(r'/app/(\d+)', steam_url)
    return match.group(1) if match else None


class Command(BaseCommand):
    help = "Fetch Steam review scores, screenshots, and ownership data for games with Steam URLs."

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            help='Re-fetch all games, including ones already updated.',
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=0,
            help='Limit the number of games to process (0 = no limit).',
        )

    def handle(self, *args, **kwargs):
        from awards.models import Game

        if kwargs['all']:
            games = Game.objects.exclude(steam_url__isnull=True).exclude(steam_url='')
            self.stdout.write("Re-fetching Steam data for ALL games with Steam URLs...\n")
        else:
            games = Game.objects.exclude(
                steam_url__isnull=True
            ).exclude(
                steam_url=''
            ).filter(
                steam_review_score__isnull=True,
                steam_screenshots__isnull=True,
            )
            self.stdout.write("Fetching Steam data for games missing data...\n")

        if kwargs['limit'] > 0:
            games = games[:kwargs['limit']]

        total = len(games)
        self.stdout.write(f"Processing {total} games...\n")

        updated = 0
        errors = []

        for index, game in enumerate(games, 1):
            appid = parse_steam_appid(game.steam_url)
            if not appid:
                self.stdout.write(self.style.WARNING(
                    f"[{index}/{total}] {game.name} - Could not parse App ID from: {game.steam_url}"
                ))
                continue

            self.stdout.write(f"[{index}/{total}] {game.name} (AppID: {appid})...")

            changes = []

            # --- Steam Reviews API ---
            try:
                reviews_resp = requests.get(
                    f"https://store.steampowered.com/appreviews/{appid}",
                    params={"json": 1, "language": "all", "purchase_type": "all"},
                    timeout=15,
                )
                reviews_resp.raise_for_status()
                reviews_data = reviews_resp.json()

                if reviews_data.get("success") == 1:
                    summary = reviews_data.get("query_summary", {})
                    review_desc = summary.get("review_score_desc")
                    total_positive = summary.get("total_positive", 0)
                    total_negative = summary.get("total_negative", 0)
                    total_reviews = total_positive + total_negative

                    if review_desc and review_desc != "0 user reviews":
                        game.steam_review_score = review_desc
                        game.steam_total_reviews = total_reviews
                        if total_reviews > 0:
                            game.steam_review_percentage = round(total_positive / total_reviews * 100)
                        changes.append(f"reviews: {review_desc} {round(total_positive / total_reviews * 100) if total_reviews > 0 else 0}% ({total_reviews:,})")
                else:
                    self.stdout.write(self.style.WARNING("  Reviews API returned success=0"))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"  Reviews error: {e}"))

            time.sleep(0.4)

            # --- Steam Store API (Screenshots) ---
            try:
                store_resp = requests.get(
                    "https://store.steampowered.com/api/appdetails",
                    params={"appids": appid},
                    timeout=15,
                )
                store_resp.raise_for_status()
                store_data = store_resp.json()

                app_data = store_data.get(str(appid), {})
                if app_data.get("success"):
                    data = app_data.get("data", {})
                    screenshots_raw = data.get("screenshots", [])
                    if screenshots_raw:
                        screenshots = [
                            {
                                "thumb": ss.get("path_thumbnail", ""),
                                "full": ss.get("path_full", ""),
                            }
                            for ss in screenshots_raw[:12]  # Max 12 screenshots
                        ]
                        game.steam_screenshots = screenshots
                        changes.append(f"screenshots: {len(screenshots)}")
                else:
                    self.stdout.write(self.style.WARNING("  Store API returned success=false"))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"  Store error: {e}"))

            time.sleep(0.4)

            # --- SteamSpy API (Owners) ---
            try:
                spy_resp = requests.get(
                    "https://steamspy.com/api.php",
                    params={"request": "appdetails", "appid": appid},
                    timeout=15,
                )
                spy_resp.raise_for_status()
                spy_data = spy_resp.json()

                owners = spy_data.get("owners", "")
                if owners and owners != "0 .. 0":
                    game.steam_owners = owners
                    changes.append(f"owners: {owners}")
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"  SteamSpy error: {e}"))

            time.sleep(0.4)

            # Save if any data was fetched
            if changes:
                game.save()
                updated += 1
                self.stdout.write(self.style.SUCCESS(f"  [OK] {', '.join(changes)}"))
            else:
                errors.append(game.name)
                self.stdout.write(self.style.WARNING(f"  [!] No data fetched"))

            time.sleep(0.3)

        self.stdout.write(self.style.SUCCESS(f"\nDone! Updated: {updated}/{total}"))

        if errors:
            self.stdout.write(self.style.WARNING(f"\nNo data fetched for ({len(errors)}):"))
            for name in errors:
                self.stdout.write(f"  - {name}")
