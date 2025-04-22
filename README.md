# Flappy Bird Game

A Python implementation of the classic Flappy Bird game using Pygame.

## Features

- Classic Flappy Bird gameplay mechanics
- Parallax scrolling background
- Score tracking with high score persistence
- Game state management (start menu, gameplay, game over)
- Bird animation with realistic physics
- Collision detection

## Tech Stack

- Python 3.x
- Pygame

## Setup Instructions

1. Make sure you have Python and Pygame installed:
   ```
   pip install pygame
   ```

2. Clone the repository or download the source code

3. Run the game:
   ```
   python main.py
   ```

## How to Play

- Press SPACE to make the bird jump/flap
- Navigate through the pipes
- Try to achieve the highest score possible
- Press R to restart after game over

## Project Structure

```
Flappy-Bird/
├── main.py                  # Entry point
├── src/                     # Source code
│   ├── components/          # Game objects
│   │   ├── bird.py          # Bird class
│   │   ├── pipe.py          # Pipe class
│   │   └── button.py        # UI button class
│   ├── game/                # Game logic
│   │   ├── controller.py    # Main game controller
│   │   ├── state.py         # Game state management
│   │   ├── score.py         # Score tracking
│   │   └── ui.py            # User interface handling
│   ├── utils/               # Utilities
│   │   ├── constants.py     # Game constants
│   │   └── assets.py        # Asset loading
│   └── assets/              # Game assets
│       ├── bird.png         # Bird sprite
│       └── background.png   # Background image
└── highscore.txt            # Persistent high score
```

## 👤 Author
Bennet Nkolele  
- GitHub: [Benighter](https://github.com/Benighter)  
- LinkedIn: [Bennet Nkolele](https://www.linkedin.com/in/bennet-nkolele-321285249/)  
- Portfolio: [My Work](https://react-personal-portfolio-alpha.vercel.app/) 