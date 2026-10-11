# Infinite Tic-Tac-Toe

Infinite tic-tac-toe (5 in a row) on an HTML5 canvas. Singleplayer works offline;
multiplayer (lobby, rooms, spectating, rematch) runs on Firebase (Firestore + anonymous auth).
No server to host.

## One-time Firebase setup
1. Console → **Build → Firestore Database** → Create database.
2. Console → **Build → Authentication → Sign-in method** → enable **Anonymous**.

## Deploy
```
npm i -g firebase-tools
firebase login
firebase deploy
```
Deploys `public/` to Hosting and publishes `firestore.rules`.
Live at https://infinite-tictactoe-cd43f.web.app

## Local test
`firebase emulators:start --only hosting` or just open `public/index.html` through any static server.
