# Infinite Tic-Tac-Toe - Mobile-Friendly Multiplayer Game

## Overview
An infinite tic-tac-toe (Gomoku) game built with HTML5 Canvas that works on both desktop and mobile devices. Players need to get 5 in a row to win. Features both singleplayer and real-time multiplayer modes.

## Features
- **Start Menu** with Singleplayer and Multiplayer options
- **Singleplayer Mode** - Play locally with alternating X and O turns
- **Multiplayer Mode** - Real-time online play with room hosting/joining
- Infinite game board with pan and zoom
- Arrow indicators for off-screen pieces with teleport functionality
- Score tracking and alternating starts (loser starts next game)

## Game Modes

### Singleplayer
- Play locally on your device
- X and O alternate turns
- Score tracked across games
- Loser starts the next game

### Multiplayer
- Host or join games via waiting room
- Enter your name before hosting/joining
- Real-time gameplay via WebSocket
- Quit button to leave at any time
- Rematch option after game ends
- Opponent disconnect detection

## Controls

### Desktop
- Right-click and drag: Pan the board
- Mouse wheel: Zoom in/out
- Left-click: Place X or O
- Click arrow: Teleport to off-screen piece

### Mobile
- Hold and drag: Pan the board
- Pinch with two fingers: Zoom in/out
- Double-tap: Place X or O
- Tap arrow: Teleport to off-screen piece

## Technical Details
- **Frontend**: HTML5 Canvas, Decimal.js for precision, Socket.IO client
- **Backend**: Flask with Flask-SocketIO for WebSocket support
- **Real-time**: gevent async mode for concurrent connections
- Responsive design that adapts to screen size

## Project Structure
- `index.html` - Main game file with all HTML, CSS, and JavaScript
- `app.py` - Flask backend with WebSocket handlers for multiplayer
- `replit.md` - Project documentation

## Running the Game
The game runs on Flask-SocketIO server on port 5000.
- `python app.py` - Starts the server

## Recent Changes
- Added start menu with title "Infinite Tic-Tac-Toe"
- Implemented Singleplayer and Multiplayer modes
- Added waiting room for multiplayer (host/join)
- Real-time game synchronization via WebSocket
- Quit button in game screen
- Game over overlay with rematch option
- Opponent disconnect handling
