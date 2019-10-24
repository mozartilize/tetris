# Tetris

![screenshot](/assets/images/sreenshot.png "screenshot")

## Installation

This game is made of python3 and pygame.

Install via pip:

```bash
$ pip install git+git://github.com/mozartilize/tetris.git
```

Then run it in terminal to play:

```bash
$ tetris
```

##  Usage

<kbd>↑</kbd> - Rotate shape

<kbd>→</kbd> - Move shape to right

<kbd>←</kbd> - Move shape to left

<kbd>↓</kbd> - Go down faster

<kbd>F9</kbd> - Pause

## Credits

This repo is built upon [this pygame tutorial](https://techwithtim.net/tutorials/game-development-with-python/tetris-pygame/tutorial-4/).

The `original_tetris.py` source code is credit to the tutorial.

## Notes

- This game is an improvement from the tutorial which reduces CPU usage from 22% to 8% (tested on my computer) by:

  - Change logic for `check_lost` which only check for positions of the latest shape.
  - Reduce for loop in grid by tracking grid's available positions used in `valid_space` and `grid#update`.
  - Draw only changed parts on pygame's surface.
  - Take advantage of python's generator.
  - And some other minor optimizations.

- Game pause was added.