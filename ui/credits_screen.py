import pygame
import time
import math
import os
from dsl.credits_parser import load_credits_text

class CreditsScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        
        # Animation state
        self.animation_state = "scrolling"  # States: scrolling, finished
        self.animation_start_time = 0
        self.scroll_position = self.screen_height  # Start below the screen
        self.scroll_speed = 100  # pixels per second (increased from 40 to 100)
        
        # Text display variables
        self.credits_lines = load_credits_text()
        self.displayed_lines = []
        self.current_line_index = 0
        self.displayed_text = ""
        self.char_index = 0
        self.last_char_time = 0
        self.line_complete = False
        self.line_pause_time = 0
        
        # Load fonts
        self.fonts = {}
        self.load_fonts()
        
        # We'll use the regular background music for credits
        self.credits_music_loaded = False
    
    def load_fonts(self):
        """Load fonts with different sizes"""
        typewriter_font_path = 'assets/fonts/typewriter.ttf'
        bloody_font_path = 'assets/fonts/bloody.ttf'
        font_sizes = [24, 28, 32, 36, 42, 48, 54, 60, 72, 90]  # Added 90 for larger title
        
        # Try to load the custom fonts
        try:
            # Load typewriter font for regular text
            for size in font_sizes:
                self.fonts[size] = pygame.font.Font(typewriter_font_path, size)
                
            # Load bloody font for the title
            self.bloody_fonts = {}
            for size in font_sizes:
                self.bloody_fonts[size] = pygame.font.Font(bloody_font_path, size)
                
        except Exception as e:
            print(f"Error loading custom font: {e}")
            # Fallback to default font
            for size in font_sizes:
                self.fonts[size] = pygame.font.Font(None, size)
                self.bloody_fonts[size] = pygame.font.Font(None, size)
    
    def handle_event(self, event):
        """Handle user input events"""
        # Allow skipping the credits with any key or mouse click
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            self.return_to_menu()
            return True
        
        return False
    
    def return_to_menu(self):
        """Return to the main menu"""
        # Just restore the original volume
        pygame.mixer.music.set_volume(0.3)  # Back to 30%
        
        self.game.change_state("menu")
    
    def update(self):
        """Update the credits screen"""
        current_time = time.time()
        
        # Start the animation if it hasn't started yet
        if self.animation_start_time == 0:
            self.animation_start_time = current_time
            
            # Just adjust the volume for credits
            pygame.mixer.music.set_volume(0.3)
        
        # Calculate total height of all credits
        total_height = 0
        for line in self.credits_lines:
            total_height += line["font_size"] + line["spacing"]
        
        # Scroll the credits
        elapsed_time = current_time - self.animation_start_time
        self.scroll_position = self.screen_height - (elapsed_time * self.scroll_speed)
        
        # Check if credits have scrolled completely
        if self.scroll_position < -total_height:
            self.animation_state = "finished"
            # Wait a moment and then return to menu
            if elapsed_time > (total_height + self.screen_height) / self.scroll_speed + 3:  # 3 second delay
                self.return_to_menu()
    
    def draw(self):
        """Draw the credits screen"""
        # Fill background with black
        self.screen.fill((0, 0, 0))
        
        # Draw scrolling credits
        y_position = self.scroll_position
        
        for line in self.credits_lines:
            # Get the font for this line
            font_size = line["font_size"]
            
            # Use bloody font for the title "Murder in the Mansion"
            if line["text"] == "Murder in the Mansion":
                # Use a larger font size for the title and make it red
                font_size = 90  # Bigger size for the title
                font = self.bloody_fonts.get(font_size, self.bloody_fonts.get(72))  # Default to 72 if size not found
                text_surface = font.render(line["text"], True, (255, 0, 0))  # Red color
            else:
                # Use regular typewriter font for other text
                font = self.fonts.get(font_size, self.fonts.get(36))  # Default to 36 if size not found
                text_surface = font.render(line["text"], True, line["color"])
            
            # Position based on alignment
            if line["align"] == "left":
                text_rect = text_surface.get_rect(left=50, top=y_position)
            elif line["align"] == "right":
                text_rect = text_surface.get_rect(right=self.screen_width - 50, top=y_position)
            else:  # center
                text_rect = text_surface.get_rect(centerx=self.screen_width // 2, top=y_position)
            
            # Only draw if visible on screen
            if (y_position + font_size > 0) and (y_position < self.screen_height):
                self.screen.blit(text_surface, text_rect)
            
            # Update y position for next line
            y_position += font_size + line["spacing"]
        
        # Draw "Press any key to skip" at the bottom of the screen
        skip_font = self.fonts.get(24, self.fonts.get(24))
        skip_text = "Press any key to skip"
        skip_surface = skip_font.render(skip_text, True, (150, 150, 150))
        skip_rect = skip_surface.get_rect(centerx=self.screen_width // 2, bottom=self.screen_height - 20)
        self.screen.blit(skip_surface, skip_rect)
