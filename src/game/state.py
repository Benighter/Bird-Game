class GameState:
    def __init__(self):
        self.is_game_over = False
        self.is_game_started = False
        self.reset()
    
    def start_game(self):
        self.is_game_started = True
        self.is_game_over = False
    
    def end_game(self):
        self.is_game_over = True
    
    def reset(self):
        self.is_game_over = False
        self.is_game_started = False 