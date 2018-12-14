# Ian Michael Jesu Alvarez
# CPSC 386 (Friday)
# This creates the window for the whole game

import pygame
import time
from pygame.sprite import Group
from settings import Settings
from paddle import Paddle
from ai_paddle import AiPaddle
from alien import Alien
from ball import Ball
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

import game_functions as gf


def run_game():

    # Initialize game, settings, and screen object.
    pygame.init()
    pong_settings = Settings()
    screen = pygame.display.set_mode((pong_settings.screen_width, pong_settings.screen_height))
    screen_rect = screen.get_rect()
    pygame.display.set_caption("Pong")
    clock = pygame.time.Clock()

    # Make the Play button.
    play_button = Button(pong_settings, screen, "Play")

    # Create an instance to store game statistics and create a scoreboard.
    stats = GameStats(pong_settings)
    sb = Scoreboard(pong_settings, screen, stats)

    # Make a ball
    ball = Ball(pong_settings, screen)

    # Make a paddle, a group of bullets, and a group of aliens.
    paddle1 = Paddle(pong_settings, screen)
    ai_paddle = AiPaddle(pong_settings, screen, ball)
    bullets = Group()
    # aliens = Alien(pong_settings, screen)
    aliens = Group()

    # Create the fleet of aliens.
    gf.create_fleet(pong_settings, screen, paddle1, aliens)

    # Start the main loop for the game.
    while True:
        gf.check_events(pong_settings, screen, stats, sb, play_button, paddle1, ai_paddle, aliens, bullets)  # has ship

        if stats.game_active:
            # Redraw and update screen
            paddle1.update()  # has ship
            ai_paddle.update()
            #bullets.update()
            #ball.update()

            ai_paddle = gf.aiControl(pong_settings, ball, pong_settings.ball_direction, ai_paddle)

#            gf.update_ball(pong_settings, ball, paddle1, ai_paddle)
            ball.update()
        gf.update_screen(pong_settings, screen, stats, sb, paddle1, ai_paddle, aliens, bullets, play_button, ball)
        clock.tick(200)


run_game()
