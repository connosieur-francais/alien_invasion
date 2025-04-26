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

ADDING THE ALIENS

- Add a single alien to the top left corner of the screen, with appropriate spacing around it
- Fill the upper portion of the screen with as many aliens as we can fit horizontally.
  We'll then create additional rows of aliens until we have a full fleet.
- Make the fleet move sideways and down until the entire fleet is shot down, an alien hits the ship
  or an alien hits the ground. If the entire fleet is shot down, we'll create a new fleet.
  If an alien hits the ship or the ground, we'll destroy the ship and create a new fleet.
- Limit the number of ships the player can use, and end the game when the player has used up
  the alloted number of ships.
"""
import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Overall class to manage game assets and behavior."""
    
    def __init__(self):
        """Initialize the game, and create game resources"""
        pygame.init()
        self.clock = pygame.time.Clock() #Controls the frame rate
        self.settings = Settings() # Create an instance of Settings and assign it to the self.settings variable
        
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        # This is a "Surface" which allows game element to be displayed
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics.
        self.stats = GameStats(self)
        
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        
        self._create_fleet()
        
        # Start Alien Invasion in an inactive state.
        self.game_active = False
        
        # Make the Play Button
        self.play_button = Button(self, "Play")
        
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self.check_events()
            
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            
            self._update_screen()
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
        
    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play"""
        if self.play_button.rect.collidepoint(mouse_pos):
            self.game_active = True
        
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
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
                    
    
    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions
        self.bullets.update()
        
        # Get rid of bullets that have dissapeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
                
        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
        
        self._check_bullet_alien_collisions()
    
    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Check for any bullets that have hit aliens.
        #   If so, get rid of the bullet and the alien.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        
        if not self.aliens:
            # Destroy existing bullets and create a new fleet.
            self.bullets.empty()
            self._create_fleet()
    
    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the ship gets hit
                self._ship_hit()
                break
    
    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""
        if self.stats.ships_left > 0:
            # Decrement ships_left.
            self.stats.ships_left -= 1
            
            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()
            
            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
            
            # Pause
            sleep(0.5)
        else:
            self.game_active = False
    
    def _update_aliens(self):
        """Update the positions of all aliens in the fleet"""
        self.aliens.update()
        
        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        # Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()
        
        """Check if the fleet is at an edge, then update positions."""
        self._check_fleet_edges()

    
    def _create_alien(self, x_position, y_position):
        """Create an Alien and place it in the fleet."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)
    
    def _create_fleet(self):
        """Create the fleet of aliens"""
        # Create an alien and keep adding aliens until there's no room left.
        # Spacing between aliens is one alien's width.
        # Spacing between aliens is one alien width and one alien height.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        
        
        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - (3 * alien_height) ):
            while current_x < (self.settings.screen_width - (2 * alien_width) ):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # Finished a row; reset x value and increment y value
            current_x = alien_width
            current_y += 2 * alien_height
    
    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Updates images on the screen, and flip to the new screen"""
        
        # Redraw the screen during each pass through the loop
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        
        # Draw the play button if the game is inactive.
        if not self.game_active:
            self.play_button.draw_button()
        
        # Make the most recently drawn screen visible
        pygame.display.flip()
    
if __name__ == "__main__":
    # Make a game isntance, and run the game
    ai = AlienInvasion()
    ai.run_game()