# This is like the ship

import pygame
from pygame.sprite import Sprite


class Paddle(Sprite):

    def __init__(self, pong_settings, screen):
        """Initialize the ship and set its starting position."""
        super(Paddle, self).__init__()
        self.screen = screen
        self.pong_settings = pong_settings

        # Load the paddle image and get its rect.
        self.image = pygame.image.load('images/stick_horizontal.png')
        self.image2 = pygame.image.load('images/stick_vertical.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Load second paddle
        self.rect2 = self.image.get_rect()

        # Load third paddle
        self.rect3 = self.image2.get_rect()

        # Start each new paddle at the bottom center of the screen.
        self.rect.centerx = (self.screen_rect.centerx + (pong_settings.screen_width/4))
        self.rect.bottom = self.screen_rect.bottom

        # Start second paddle at top
        self.rect2.centerx = (self.screen_rect.centerx + (pong_settings.screen_width / 4))
        self.rect2.top = self.screen_rect.top

        # Start third paddle
        self.rect3.centery = self.screen_rect.centery
        self.rect3.right = self.screen_rect.right

        # Store a decimal value for the paddle's center.
        self.center = float(self.rect.centerx)

        # Store a decimal value for the paddle's center at right
        self.centerRight = float(self.rect.centery)

        # Movement flag
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Update the ship's position based on the movement flag."""
        # Update the paddle's center value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:  # If true
            self.center += self.pong_settings.ship_speed_factor

        if self.moving_left and self.rect.left > self.pong_settings.screen_width/2:
            self.center -= self.pong_settings.ship_speed_factor

        if self.moving_up and self.rect3.top > self.screen_rect.top:
            self.centerRight -= self.pong_settings.ship_speed_factor

        if self.moving_down and self.rect3.bottom < self.pong_settings.screen_height:
            self.centerRight += self.pong_settings.ship_speed_factor

        # Update rect object from self.center.
        self.rect.centerx = self.center
        self.rect2.centerx = self.center

        # Update rect object from self.centerRight
        self.rect3.centery = self.centerRight - self.pong_settings.screen_height/4

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.image, self.rect2)
        self.screen.blit(self.image2, self.rect3)

    def center_ship(self):
        """Center the ship on the screen."""
        self.center = self.screen_rect.centerx + (self.pong_settings.screen_width/4)
        self.centerRight = self.pong_settings.screen_width/2
