import urllib.request
import urllib.parse
import re
import time
from django.core.management.base import BaseCommand
from awards.models import Game

class Command(BaseCommand):
    help = 'Searches YouTube for game trailers using scraping and saves them as embed URLs.'

    def handle(self, *args, **kwargs):
        # Fetching only games that don't have a trailer yet
        games = Game.objects.all() 
        total_games = games.count()
        
        if total_games == 0:
            self.stdout.write(self.style.SUCCESS("All games already have trailers!"))
            return

        self.stdout.write(f"Starting YouTube scrape for {total_games} games...\n")

        # Adding a User-Agent to look like a real browser
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

        for index, game in enumerate(games, 1):
            self.stdout.write(f"[{index}/{total_games}] Searching: {game.name}...")
            
            # Constructing the search query
            search_query = f"{game.name} official game launch trailer"
            query = urllib.parse.quote(search_query)
            url = f"https://www.youtube.com/results?search_query={query}"
            
            try:
                # Requesting the search results page
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req) as response:
                    html = response.read().decode()
                    
                    # Finding the first video ID using Regex
                    # Looking for the pattern watch?v=XXXXXXXXXXX
                    video_ids = re.findall(r"watch\?v=(\S{11})", html)
                    
                    if video_ids:
                        # Converting the first result to an EMBED URL
                        embed_link = f"https://www.youtube.com/embed/{video_ids[0]}"
                        
                        # Saving to the database
                        game.trailer_url = embed_link
                        game.save()
                        
                        self.stdout.write(self.style.SUCCESS(f"  ✓ Link: {embed_link}"))
                    else:
                        self.stdout.write(self.style.WARNING(f"  ✗ No video ID found in results."))
                        
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  ! Error during request: {e}"))
            
            # Critical: Sleep for 1 second to avoid being blocked by YouTube's anti-bot system
            time.sleep(1)

        self.stdout.write(self.style.SUCCESS("\nProcess finished! All available trailers are updated."))