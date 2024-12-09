# Chrome Dino Game Clone

A Python implementation of the Chrome Dinosaur Game with added features like user authentication and score tracking.

## Features

### User Management
- User registration and login system
- Password protection
- Remembers last logged-in user
- Multiple user support
- User switching capability

### Gameplay
- Classic dinosaur running game mechanics
- Jump over cacti and dodge birds
- Increasing difficulty with speed
- Score tracking
- Pause functionality

### Score System
- Personal top 5 scores per user
- Global leaderboard (top 5 scores)
- Persistent score storage
- Real-time score updates

### Game States
1. Login/Register
2. Menu
3. Active Game
4. Pause Screen
5. Game Over

## Controls

### Game Controls
- UP ARROW: Jump
- DOWN ARROW: Duck
- SPACE: Pause/Resume

### Menu Controls
- Any key: Start game
- R: Restart
- Q: Quit

### Login/Register Controls
- TAB: Switch between username/password fields
- ENTER: Submit
- R: Switch to registration
- L: Switch to login

## File Structure

- [Description](#description)
- [Installation](#installation)
- [Controls](#controls)
- [Libraries](#libraries)

## Description

This is a simple implementation of the Chrome Dinosaur Game using Python and Pygame. The game is a simple infinite runner where the player has to jump over cacti and avoid birds. 
The game gets progressively harder as the player's score increases. See how far you can get!

## Installation

### Requirements
- Python 3.x
- pip (Python package installer)

### Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd chrome-dino-game
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the game:
   ```bash
   python dino.py
   ```

### Data Files
The game will automatically create these JSON files on first run:
- `users.json`: Stores user credentials
- `scores.json`: Stores game scores
- `last_login.json`: Remembers last login

### Troubleshooting
- Make sure Python and pip are properly installed
- Ensure all game assets are in the correct directories
- Check if the virtual environment is activated before installing requirements

## Controls
- Use the up arrow key or spacebar to jump.
- Press any key to start the game.
- When the game ends, press any key to restart.

## Libraries

- [pygame](https://www.pygame.org/news): Pygame is a cross-platform set of Python modules designed for writing video games.
