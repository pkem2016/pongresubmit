import pygame
from pygame.sprite import Sprite
from random import randint


class Ball(Sprite):
    def __init__(self, pong_settings, screen):

        super(Ball, self).__init__()
        self.pong_settings = pong_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.image = pygame.image.load('images/newball.png.png')
        self.rect = self.image.get_rect()  # "Hit box" for the image sprite

        # Starting position of the ball
        self.rect.x = pong_settings.screen_width/2 - (self.rect.width/2)
        self.rect.y = pong_settings.screen_height/2 - (self.rect.height/2)

        # Store a decimal value for the ball's center
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Randomize initial direction
        self.direction = 1

        # Music effects
        self.ball_hit_wall = pygame.mixer.Sound('sounds/ball_hit_wall.wav')
        self.ball_hit_paddle = pygame.mixer.Sound('sounds/ball_hit_paddle.wav')
        self.ball_miss = pygame.mixer.Sound('sounds/ball_miss.wav')

        # Movement flag
        self.moving_upleft = 0
        self.moving_upright = 1
        self.moving_downleft = 2
        self.moving_downright = 3

    def check_edges(self):
        """Return True if alien is at the edge of screen."""  # Determine who scores?
        print("hit edge")
        if self.rect.right >= self.screen_rect.right:
            pygame.mixer.Sound.play(self.ball_miss)
            return True
        elif self.rect.left <= 0:
            pygame.mixer.Sound.play(self.ball_miss)
            return True
        elif self.rect.top <= 0:
            pygame.mixer.Sound.play(self.ball_miss)
            return True
        elif self.rect.bottom >= self.screen_rect.bottom:
            pygame.mixer.Sound.play(self.ball_miss)
            return True

    def update(self):
        """Move the ball around"""
        if self.direction == self.moving_upleft:
            self.x -= (self.pong_settings.ball_speed * self.pong_settings.ball_direction)
            self.y -= (self.pong_settings.ball_speed * self.pong_settings.ball_direction)
            self.rect.x = self.x
            self.rect.y = self.y

        elif self.direction == self.moving_upright:
            self.x += (self.pong_settings.ball_speed * self.pong_settings.ball_direction)
            self.y -= (self.pong_settings.ball_speed * self.pong_settings.ball_direction)
            self.rect.x = self.x
            self.rect.y = self.y

        elif self.direction == self.moving_downleft:
            self.x -= (self.pong_settings.ball_speed * self.pong_settings.ball_direction)
            self.y += (self.pong_settings.ball_speed * self.pong_settings.ball_direction)
            self.rect.x = self.x
            self.rect.y = self.y

        elif self.direction == self.moving_downright:
            self.x += (self.pong_settings.ball_speed * self.pong_settings.ball_direction)
            self.y += (self.pong_settings.ball_speed * self.pong_settings.ball_direction)
            self.rect.x = self.x
            self.rect.y = self.y

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    # def center_ship(self):
    #     self.center = self.screen_rect.centerx


