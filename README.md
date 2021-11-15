# Puzzle Game
![puzzleGame](https://user-images.githubusercontent.com/70440104/141772769-efd7c756-ca92-4190-83ea-66501097c8a9.jpg)
## Contributors
- Minh Chien Nguyen<br/>ID: 19110173<br/>

- Phi Anh Pham<br/>ID: 19110512

## Description
`Puzzle Game` is a game which the player is expected to move pieces in a logical way, in order to reach at the inital state of the provided image, players can also choose any images from their local computers. The game was implemented in Python using Pygame.

`A* algorithm` is used in this project to assist identify the quickest path.

## Prerequisites
- Make sure your machine had installed `python3.9`, `pygame`, `numpy` and `tkinter`.
- You are using a Windows machine.
- If you haven't installed any of these, you can install [python3.9](https://www.python.org/downloads/) and libraries.
```
pip install pygame
pip install numpy
pip install tkinter
```

## Jump In The Game
- Locate and open main.py in source folder `src` to play the game.
- After clicking on `Shuffle` button, you can use your cursor to interact with the puzzle.

## Features
- `Shuffle` function performs random moves.
- `Solve` funtion solves the Puzzle using [A* algorithm](https://en.wikipedia.org/wiki/A*_search_algorithm).
- `Hint` funtion indicates best move possible so as to reach the initial images.
- `File` funtion uses the selected image in your local machine as the puzzle itself.

## References
https://www.pygame.org/docs/ <br/>
https://yinyangit.wordpress.com/2010/12/11/algorithm-tim-hiểu-về-bai-toan-n-puzzle-updated/ <br/>
https://stackoverflow.com/questions/16235564/convert-1d-array-into-numpy-matrix/16235630 <br/>
https://www.youtube.com/watch?v=XRqA6RQr3SQ&ab_channel=APCRPDEE
