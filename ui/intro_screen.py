import pygame
import time

class IntroScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        
        # Load typewriter font
        try:
            self.font_large = pygame.font.Font('assets/fonts/typewriter.ttf', 72)
            self.font_medium = pygame.font.Font('assets/fonts/typewriter.ttf', 48)
            self.font_small = pygame.font.Font('assets/fonts/typewriter.ttf', 32)
            print("Loaded typewriter font for intro screen")
        except Exception as e:
            print(f"Error loading typewriter font: {e}")
            # Fallback to default fonts
            self.font_large = pygame.font.Font(None, 72)
            self.font_medium = pygame.font.Font(None, 48)
            self.font_small = pygame.font.Font(None, 32)
        
        # Text to display in sequence
        self.intro_texts = [
            "Wallace Estate",
            "March 12, 2023",
            "3:50 PM"
        ]
        
        # Track current text index and wait for input
        self.current_text_index = 0
        self.waiting_for_input = True
        self.all_texts_shown = False  # Flag to track if all texts have been shown
        
        # Typewriter effect variables
        self.current_displayed_text = ""
        self.typewriter_index = 0
        self.last_char_time = 0
        self.char_delay = 0.08  # Seconds between characters (slower typing)
        self.typewriter_complete = False
        
        # Continue prompt
        self.continue_text = "Click Mouse or Press Space To Continue"
        
        # Background
        self.background = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        self.background.fill((0, 0, 0))  # Black background
    
    def handle_event(self, event):
        # Check for mouse click or space bar to continue
        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) or \
           (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
            
            if self.waiting_for_input:
                # If all texts have been shown, transition to welcome screen
                if self.all_texts_shown:
                    # Transition to the welcome screen with the cop character and dialogue
                    print("Transitioning to welcome screen")
                    self.game.change_state("welcome_screen")
                # Otherwise show next text
                elif self.current_text_index < len(self.intro_texts):
                    # Move to next text
                    self.current_text_index += 1
                    # Reset typewriter effect for the new text
                    self.current_displayed_text = ""
                    self.typewriter_index = 0
                    self.typewriter_complete = False
                    self.last_char_time = time.time()
                    # Check if we've shown all texts
                    if self.current_text_index >= len(self.intro_texts):
                        self.all_texts_shown = True
    
    def update(self):
        # Update typewriter effect
        if self.current_text_index > 0 and not self.typewriter_complete:
            current_time = time.time()
            
            # If it's time to add a new character
            if current_time - self.last_char_time >= self.char_delay:
                self.last_char_time = current_time
                
                # Get the full text we're currently displaying
                full_text = self.intro_texts[self.current_text_index - 1]
                
                # Add one more character if we haven't shown the full text
                if self.typewriter_index < len(full_text):
                    self.current_displayed_text = full_text[:self.typewriter_index + 1]
                    self.typewriter_index += 1
                else:
                    self.typewriter_complete = True
    
    def draw(self):
        # Draw black background
        self.screen.blit(self.background, (0, 0))
        
        # Draw intro texts up to current index
        screen_center_x = self.screen.get_width() // 2
        
        # Draw previous texts (fully visible)
        for i in range(self.current_text_index - 1):
            # Position texts in the middle of the screen, spaced vertically
            y_position = self.screen.get_height() // 2 - 100 + (i * 80)
            
            # Render text
            text_surface = self.font_large.render(self.intro_texts[i], True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(screen_center_x, y_position))
            self.screen.blit(text_surface, text_rect)
            
        # Draw current text with typewriter effect
        if self.current_text_index > 0:
            y_position = self.screen.get_height() // 2 - 100 + ((self.current_text_index - 1) * 80)
            
            # Render text with typewriter effect
            text_surface = self.font_large.render(self.current_displayed_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(screen_center_x, y_position))
            self.screen.blit(text_surface, text_rect)
        
        # Draw continue prompt
        # Always show the continue prompt - either to show next text or to continue to next scene
        continue_surface = self.font_small.render(self.continue_text, True, (200, 200, 200))
        continue_rect = continue_surface.get_rect(center=(screen_center_x, self.screen.get_height() - 100))
        self.screen.blit(continue_surface, continue_rect)
