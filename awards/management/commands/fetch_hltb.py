import os
import sys
import django
import time

# Add the Django project directory to the Python path
project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, project_dir)
os.chdir(project_dir)

# Setup required to use Django settings in an external script
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameawards.settings')
django.setup()

from awards.models import Game
from howlongtobeatpy import HowLongToBeat

def update_game_times():
    # Find only the games that don't have playtime data yet (to avoid unnecessary fetches)
    games_to_update = Game.objects.filter(hltb_main__isnull=True)
    
    total_games = games_to_update.count()
    print(f"Fetching playtime data for {total_games} games...\n")

    for index, game in enumerate(games_to_update, 1):
        print(f"[{index}/{total_games}] Searching: {game.name}...", end=" ")
        
        try:
            results = HowLongToBeat().search(game.name)
            
            if results is not None and len(results) > 0:
                # Find the best match based on similarity
                best_match = max(results, key=lambda element: element.similarity)
                
                game.hltb_main = str(best_match.main_story)
                game.hltb_extra = str(best_match.main_extra)
                game.hltb_completionist = str(best_match.completionist)
                game.save()
                
                print(f"✅ Found! (Main: {best_match.main_story}h)")
            else:
                # If not found, save "-" so it doesn't waste time searching again next time
                game.hltb_main = "-"
                game.hltb_extra = "-"
                game.hltb_completionist = "-"
                game.save()
                print("❌ Not found.")
                
        except Exception as e:
            print(f"⚠️ Error occurred: {e}")
            
        # IMPORTANT: Let the bot breathe for 1 second after each search to avoid IP bans!
        time.sleep(1)

    print("\n🎉 All game times have been successfully updated!")

if __name__ == '__main__':
    update_game_times()