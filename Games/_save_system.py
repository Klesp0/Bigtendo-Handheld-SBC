import json
from config import *


class SaveSystem:
    def __init__(self):
        self.save_file = HIGHSCORES_TIME_FILE
        
        try:
            with open(self.save_file, "r") as file:
                self.highscores = json.load(file)
        
        except FileNotFoundError as e:
            print(f"Nenajdeny subor {e}")
    
    def get_highscore(self, game_name):
        return self.highscores[game_name]
    
    def save(self):
        with open(self.save_file, "w") as file:
            json.dump(self.highscores, file, indent = 4)
    
    def update_score(self, game_name, score):
        if score > self.get_highscore(game_name):
            self.highscores[game_name] = score
            self.save()
        
if __name__ == "__main__":
    s = SaveSystem()
    
    print(s.get_highscore("Pong"))
    
    s.update_score("Pong", 100)
    print(s.get_highscore("Pong"))
    
    s.update_score("Pong", 170)
    print(s.get_highscore("Pong"))