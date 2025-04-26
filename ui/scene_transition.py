import pygame
import time

class SceneTransition:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.transitioning = False
        self.next_scene = None
        
        # Fade effect properties
        self.fade_surface = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        self.fade_surface.fill((0, 0, 0))  # Black surface for fading
        self.fade_alpha = 0  # Fully transparent
        self.fade_duration = 2.0  # Fade duration in seconds
        self.fade_start_time = 0
        self.fade_out_music = False  # Whether to fade out music during transition
        
    def start_fade(self, next_scene, fade_out_music=False):
        """Start a fade transition to the next scene"""
        self.transitioning = True
        self.next_scene = next_scene
        self.fade_start_time = time.time()
        self.fade_alpha = 0
        self.fade_out_music = fade_out_music
        
    def handle_event(self, event):
        """Handle events during transition"""
        # Block all events during transition
        return True
        
    def update(self):
        """Update the fade transition"""
        if not self.transitioning:
            return
            
        # Calculate fade progress
        elapsed = time.time() - self.fade_start_time
        progress = min(1.0, elapsed / self.fade_duration)
        
        # Update fade alpha
        self.fade_alpha = int(255 * progress)
        
        # Fade out music if requested
        if self.fade_out_music:
            # Gradually reduce volume
            new_volume = max(0.0, 0.3 * (1.0 - progress))  # Starting from 0.3 (30%)
            pygame.mixer.music.set_volume(new_volume)
        
        # Check if fade is complete
        if progress >= 1.0:
            # Complete transition
            self.transitioning = False
            
            # Change to the next scene
            if self.next_scene:
                self.game.current_state = self.next_scene
                
                # Initialize the suspense screen if needed
                if self.next_scene == "suspense_screen":
                    player_selection = self.game.states["answer_screen"].selected_character
                    self.game.states["suspense_screen"].enter(player_selection)
                
                self.next_scene = None
                
    def draw(self):
        """Draw the transition effect over the current scene"""
        if self.transitioning:
            # Set the alpha value for the fade surface
            self.fade_surface.set_alpha(self.fade_alpha)
            
            # Draw the fade surface over the screen
            self.screen.blit(self.fade_surface, (0, 0))
            
    def draw_character_entrance(self, character_image, start_pos, end_pos):
        """Draw a character sliding into the scene"""
        # TODO: Implement character entrance animation
        pass