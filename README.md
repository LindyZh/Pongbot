# Pongbot

![alt text](https://github.com/LindyZh/Pongbot/blob/7245fe839e22e9de4def622da2afe78c732cddb7/pong_snipshot.png)

Youtube link to the final pong contest matches:
https://www.youtube.com/watch?v=1ylTNh2DiaU&t=3s

Our bot have won the first place in 2021 ESC180 pong contest. 
essentially, we have created a bot that can predict the trajectory of the pong ball in the game and make reasonable reactions:
1. the racket predicts the ball's falling point and can hit the ball with 100% accuracy (if time and the ball speed allows)
2. after every hit it attempts to return to the middle (to avoid the cases where two corner balls are served in a row)
3. the racket will return the ball to the corner which is the farest from the opponent's racket.

That's it :)
