# pig-game

Implementation of pig-game

Full-Stack Pig Game
Pig Game is a simple race-to-100 dice game for two players.

The two players must decide if they should play safe or keep rolling to gain more points, knowing that a single bad roll (a number 1) can wipe out their entire progress.

In the beginning of the game, there is a start session page where a user needs to identify by entering an email, username, etc. This makes the game differentatiate betweeen multiple game sessions.

After the user enters the session, the default first player is Player 1. It start rolling the dice (that generates a random number between 1 and 6), and the points accumulated go to Current score.
The player can keep playing to accumulate a bigger score untill it reaches 100 points.
"In my version of the game, I used JavaScript to handle the user interface and animations, while Python acts as the 'referee' in the background to calculate the scores and ensure the game rules are followed fairly."
If the player rolls a 1, they lose all the points gathered during that specific turn, and it becomes the other's playert turn.

If a player clicks "Hold", they decide to play it safe and gather all the points accumulated in the Current score. The game then checks if their total Score is 100 or more.
If yes: That player is declared the Winner, and the game ends.
If no: The turn passes to the opponent.

In my version of the game, I used JavaScript to handle the user interface and animations, while Python acts as the 'referee' in the background to calculate the scores and ensure the game rules are followed fairly.
