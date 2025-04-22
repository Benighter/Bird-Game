class GameState:
    def __init__(self):
        self.is_game_over = False
        self.is_game_started = False
        self.is_bird_falling = False
        self.reset()
    
    def start_game(self):
        self.is_game_started = True
        self.is_game_over = False
        self.is_bird_falling = False
    
    def end_game(self):
        self.is_game_over = True
        self.is_bird_falling = True
    
    def bird_hit_ground(self):
        self.is_bird_falling = False
    
    def reset(self):
        self.is_game_over = False
        self.is_game_started = False
        self.is_bird_falling = False 