class ScoreManager:
    def __init__(self, highscore_file="highscore.txt"):
        self.score = 0
        self.highscore_file = highscore_file
        self.high_score = self.load_high_score()
    
    def increment(self):
        self.score += 1
        
    def reset(self):
        self.score = 0
        
    def load_high_score(self):
        try:
            with open(self.highscore_file, "r") as f:
                return int(f.read())
        except (FileNotFoundError, ValueError):
            return 0
    
    def save_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            try:
                with open(self.highscore_file, "w") as f:
                    f.write(str(self.score))
                return True
            except Exception:
                return False
        return False
    
    def is_new_high_score(self):
        return self.score > self.high_score 