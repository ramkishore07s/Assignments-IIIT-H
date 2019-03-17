> Developed and Tested on MAC OS SIERRA v.10.12.6
> Should work on all Unix based systems, may not work on Windows
> Bonus implemented: Powerups, Bomb timer count, levels
> Animate elements of the game are enclosed in brackets to differentiate them from inanimate ones.
> Controls: WSAD for movement, P for powerup and B for dropping bombs
> Only one powerup per level is permitted, two powerups were implemented: SLOWDOWN enemies and INFINITE life
> files included:
   * main.py
     the entry point into the game. handles input and interactions between various implementation of classes and levels
   * animations.py
     takes care of the animations in the game, the static screens like the startup one etc
   * graphic.py
     the design that is displayed to the user, the one that makes this dynamic multilevel program into a single static display.
   * characters.py
     the blueprints of the characters of the game are defined here, they are instantiated in the main file.
   * accessories.py
     classes of inanimate objects are implemented here. eg walls, bomb, brick, powerup etc
   * board.py
     The class board is implemented here.
