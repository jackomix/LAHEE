#!/usr/bin/env python3
import pygame
import sys
import json
import urllib.request
import urllib.parse

# R36S Screen Resolution
WIDTH = 640
HEIGHT = 480

pygame.init()
pygame.display.set_caption("LAHEE UI")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont("monospace", 20)
large_font = pygame.font.SysFont("monospace", 30)

API_URL = "http://127.0.0.1:8000/dorequest.php"

def fetch_lahee_info():
    try:
        req = urllib.request.Request(API_URL, data=b"r=laheeinfo", headers={'Content-Type': 'application/x-www-form-urlencoded'})
        with urllib.request.urlopen(req, timeout=3) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Error fetching LAHEE info: {e}")
        return None

def main():
    clock = pygame.time.Clock()
    running = True

    info = fetch_lahee_info()
    
    if not info:
        state = "ERROR"
    else:
        state = "LIST"
        
    games = info.get("games", []) if info else []
    users = info.get("users", []) if info else []
    
    selected_game_idx = 0
    
    while running:
        screen.fill((30, 30, 30))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_UP:
                    selected_game_idx = max(0, selected_game_idx - 1)
                elif event.key == pygame.K_DOWN:
                    selected_game_idx = min(len(games) - 1, selected_game_idx + 1)
                elif event.key == pygame.K_RETURN:
                    # In a full UI, pressing Enter would show achievements for the game
                    pass

        if state == "ERROR":
            text = font.render("Could not connect to LAHEE Server.", True, (255, 100, 100))
            screen.blit(text, (20, 20))
            text2 = font.render("Make sure LAHEE is running in the background.", True, (200, 200, 200))
            screen.blit(text2, (20, 60))
            text3 = font.render("Press B (ESC) to exit.", True, (200, 200, 200))
            screen.blit(text3, (20, 100))
        elif state == "LIST":
            title = large_font.render("LAHEE Games", True, (255, 255, 255))
            screen.blit(title, (20, 20))
            
            if not games:
                text = font.render("No games found in LAHEE Data folder.", True, (200, 200, 200))
                screen.blit(text, (20, 80))
            else:
                for i, game in enumerate(games):
                    color = (255, 255, 100) if i == selected_game_idx else (200, 200, 200)
                    text = font.render(f"{game.get('Title', 'Unknown')} (ID: {game.get('ID', '0')})", True, color)
                    screen.blit(text, (20, 80 + i * 30))
                    
                # Display basic user stats for selected game
                if len(users) > 0 and len(games) > 0:
                    current_user = users[0] # Just pick first user
                    game_id = str(games[selected_game_idx].get("ID", ""))
                    ug_data = current_user.get("GameData", {}).get(game_id, {})
                    ach_dict = ug_data.get("Achievements", {})
                    
                    unlocked_count = len([a for a in ach_dict.values() if a.get("Status", 0) > 0])
                    total_count = len(games[selected_game_idx].get("AchievementSets", [{}])[0].get("Achievements", []))
                    
                    stat_text = font.render(f"Unlocked: {unlocked_count} / {total_count}", True, (100, 255, 100))
                    screen.blit(stat_text, (20, 400))
            
            text_footer = font.render("Press B (ESC) to exit", True, (150, 150, 150))
            screen.blit(text_footer, (20, 440))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
