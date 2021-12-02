import math
import turtle
import winsound
import pygame as pg
# import random


def draw_borders():
    border_pen = turtle.Turtle()
    border_pen.speed(0)
    border_pen.color("white")
    border_pen.penup()
    border_pen.setposition(-280, -280)
    border_pen.pendown()
    border_pen.pensize(3)

    for side in range(4):
        border_pen.fd(560)
        border_pen.lt(90)

    border_pen.hideturtle()


def draw_score():
    score_pen.speed(0)
    score_pen.color('white')
    score_pen.penup()
    score_pen.setposition(-280, 282)
    score_pen.write(score_string, False, align='left', font=('Arial', 14, 'normal'))
    score_pen.hideturtle()


def move_left():
    player.speed = -4
    move_player()


def move_right():
    player.speed = 4
    move_player()


def move_player():
    x = player.xcor()
    x += player.speed
    # boundary checking
    if x < -265:
        x = -265
    # boundary checking
    if x > 265:
        x = 265
    player.setx(x)


def fire_bullet():
    # Declare bullet_state as a global if it needs changed
    global bullet_state
    if bullet_state == 'ready':
        # winsound.PlaySound('laser.wav', winsound.SND_ASYNC)
        play_sound('laser.wav')
        bullet_state = 'fire'
        # Move the bullet above the player
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x, y)
        bullet.showturtle()


def isCollision(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))

    if distance < 15:
        return True
    else:
        return False


def update_score():
    global score
    score += 10
    global score_string
    score_string = f'Score: {score}'
    score_pen.clear()
    score_pen.write(score_string, False, align='left', font=('Arial', 14, 'normal'))


def play_sound(sound_file):
    winsound.PlaySound(sound_file,winsound.SND_ASYNC | winsound.SND_ASYNC)

    # if time > 0:
    #     print('inside if')
    #     turtle.ontimer(lambda: play_sound(sound_file, time), t=int(time * 1000))


def bg_music():
    pg.init()
    pg.mixer.music.load('beverly-hill-cop.wav')
    pg.mixer.music.play(-1)


# Set up the screen
wn = turtle.Screen()
wn.setup(width=600, height=600)
wn.bgcolor("black")
wn.title("Space Invaders")
wn.bgpic("space-invaders-background.gif")
wn.tracer(0)

# Register the shapes
wn.register_shape('invader.gif')
wn.register_shape('player.gif')

# Score starting score
score = 0
score_pen = turtle.Turtle()
score_string = f'Score: {score}'

draw_score()
draw_borders()

player = turtle.Turtle()
player.color("blue")
player.shape("player.gif")
player.penup()
player.speed(0)
player.setposition(0, -250)
player.setheading(90)
player.speed = 0

# Choose a number of enemies
number_of_enemies = 30
# Empty list of enemies
enemies = []

# Add enemies to the lis
for i in range(number_of_enemies):
    # Create enemy
    enemies.append(turtle.Turtle())

enemy_start_x = -225
enemy_start_y = 250
enemy_number = 0


for enemy in enemies:
    enemy.color("red")
    enemy.shape("invader.gif")
    enemy.penup()
    enemy.speed(0)
    # x = random.randint(-200, 200)
    x = enemy_start_x + (50 * enemy_number)
    # y = random.randint(100, 250)
    y = enemy_start_y
    enemy.setposition(x, y)
    # update enemy number
    enemy_number += 1
    if enemy_number == 10:
        enemy_start_y -= 50
        enemy_number = 0

enemy_speed = .2

# Keyboard binding
wn.listen()
wn.onkeypress(move_left, "Left")
wn.onkeypress(move_right, "Right")
wn.onkeypress(fire_bullet, "space")

# Create player's bullet
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.setposition(0, -250)
bullet.shapesize(.5, .5)
bullet.hideturtle()

bullet_speed = 5

# Define bullet state
# ready - ready to fire
# fire = bullet is firing
bullet_state = 'ready'

# Play background music
bg_music()

# main loop
while True:
    wn.update()
    for enemy in enemies:
        # Move the enemy
        x = enemy.xcor()
        x += enemy_speed
        enemy.setx(x)

        # Once the enemy reaches an edge move down
        if enemy.xcor() > 265:
            # Move all the enemies down
            for e in enemies:
                y = e.ycor()
                y -= 30
                e.sety(y)
            # Change enemy direction
            enemy_speed *= -1

        if enemy.xcor() < -265:
            # Move all the enemies down
            for e in enemies:
                y = e.ycor()
                y -= 30
                e.sety(y)
            # Change enemy direction
            enemy_speed *= -1

        # Check for collision between the bullet and the enemy
        if isCollision(bullet, enemy):
            # winsound.PlaySound('explosion.wav', winsound.SND_ASYNC)
            play_sound('explosion.wav')
            # Reset the bullet
            bullet.hideturtle()
            bullet_state = 'ready'
            bullet.setposition(0, -400)
            # Reset the enemy
            # x = random.randint(-200, 200)
            # y = random.randint(100, 250)
            enemy.setposition(0, -10000)
            # update score
            update_score()

        if isCollision(player, enemy):
            # winsound.PlaySound('explosion.wav', winsound.SND_ASYNC)
            play_sound('explosion.wav')
            player.hideturtle()
            enemy.hideturtle()
            print("Game Over")
            break
        # Hide enemy is out of y bounds
        if enemy.ycor() < -265:
            enemy.hideturtle()

        # Move the bullet
    if bullet_state == 'fire':
        y = bullet.ycor()
        y += bullet_speed
        bullet.sety(y)

    # Check to see if the bullet has gone to the top
    if bullet.ycor() > 275:
        bullet.hideturtle()
        bullet_state = 'ready'

# wn.exitonclick()

# 10
