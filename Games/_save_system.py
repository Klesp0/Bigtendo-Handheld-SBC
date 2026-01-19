import json
from config import *
import time
# mozno dorobit ukladanie settings ked bude cas


class SaveSystem:
    def __init__(self):
        self.save_file = HIGHSCORES_TIME_FILE
        
        try:
            with open(self.save_file, "r") as file:
                self.highscores_times = json.load(file)
                self.highscores = self.highscores_times["highscores"]
                self.times = self.highscores_times["times"]
        
        except FileNotFoundError as e:
            print(f"Nenajdeny subor {e}")
    
    def get_highscore(self, game_name):
        return self.highscores[game_name]
    
    def get_time(self, game_name):
        return self.times[game_name]
    
    def save(self):
        with open(self.save_file, "w") as file:
            json.dump(self.highscores_times, file, indent = 4)
    
    def update_score(self, game_name, score):
        if score > self.get_highscore(game_name):
            self.highscores[game_name] = score
            self.highscores_times["highscores"] =self.highscores
            self.save()
    
    def update_time(self, game_name):
        current_time = time.time()
        self.times[game_name] = current_time
        self.highscores_times["times"] = self.times
        self.save()
        
# Test
if __name__ == "__main__":
    s = SaveSystem()
    
    print(s.get_highscore("Pong"))
    print(s.get_time("Pong"))
    
    s.update_score("Pong", 100)
    print(s.get_highscore("Pong"))
    
    s.update_score("Pong", 170)
    print(s.get_highscore("Pong"))
    
    print(s.get_time("Pong"))
    s.update_time("Pong")
    
    print(s.get_time("Pong"))