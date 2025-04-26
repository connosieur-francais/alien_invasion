"""
ALIEN INVASION - USING PYGAME
Question is gotten from: Python Crash Course EBOOK

In the Alien Invasion project, you'll use the Pygame package to develop a 2D game.
The goal of the game is to shoot down a fleet of aliens as they drop down the screen,
in levels that increase in speed and difficulty.
At the end of the project,
you'll have learned skills that will enable you to develop your own 2D games in python.

ALIEN INVASION spans a number of different files, so make a new alien_invasion folder on your system.
Be sure to save all files for the project to this folder, so your import statements will work correctly.
    Also, if you feel comfortable using version control, you might want to use it for this project.
    If you haven't used version control before, this is a good time to start.
    
----> PLANNING THE PROJECT <----

1. Player controls the ship that appears at the bottom center of the screen.

2. Player can move the ship left right using "A" and "D" keys and shoot bullets using "SPACE" key.

3. When the game starts, a fleet of aliens fill the sky and moves across and down the screen.

4. The player shoots and destryos the aliens.

5. If the player destroys all the aliens, a new fleet appears that moves faster than the previous fleet.

6. If any alien hits the ship or reaches the bottom of the screen, the player loses a ship.

7. If the player loses three ships, the game ends.

"""
import sys

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet

class AlienInvasion:
    """Overall class to manage game assets and behavior."""
    
    def __init__(self):
        """Initialize the game, and create game resources"""
        pygame.init()
        self.clock = pygame.time.Clock() #Controls the frame rate
        self.settings = Settings() # Create an instance of Settings and assign it to the self.settings variable
        
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        # This is a "Surface" which allows game element to be displayed
        pygame.display.set_caption("Alien Invasion")
        
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self.check_events()
            self.ship.update()
            self.bullets.update()
            self.update_screen()
            self.clock.tick(60) # The number inside the () determines how many frames per second the game should run
    
    def check_events(self):
        """Respond to keypresses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
        
    def _check_keydown_events(self, event):
        """Respond to keypresses"""
        if event.key == pygame.K_d:
            # Move the ship to the right
            self.ship.moving_right = True
        elif event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
    
    def _check_keyup_events(self, event):
        """Responds to key releases"""
        if event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_a:
            self.ship.moving_left = False   
        
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)
                    
    
    def update_screen(self):
        """Updates images on the screen, and flip to the new screen"""
        
        # Redraw the screen during each pass through the loop
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        
        # Make the most recently drawn screen visible
        pygame.display.flip()
    
if __name__ == "__main__":
    # Make a game isntance, and run the game
    ai = AlienInvasion()
    ai.run_game()