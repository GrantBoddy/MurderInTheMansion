import pygame

import math
import random
import time
import os
from dsl.congrats_parser import load_congrats_text
from ui.confetti import Confetti

class WinningScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        
        # Animation state
        self.animation_state = "spinning"  # States: spinning, landed, typing, waiting
        self.animation_start_time = 0
        self.spin_duration = 2.0  # seconds
        self.spin_angle = 0
        self.image_scale = 2.0  # Starting scale (larger)
        self.final_scale = 0.4  # Final scale after landing (smaller)
        
        # Stamp animation
        self.show_stamp = False
        self.stamp_start_time = 0
        self.stamp_animation_duration = 0.3  # seconds
        self.stamp_scale = 1.0
        self.stamp_angle = 30  # Diagonal angle in degrees (positive for left-down, right-up)
        
        # Load arrest image
        self.arrest_image = None
        self.load_arrest_image()
        
        # Text display variables
        self.congrats_lines = load_congrats_text()
        self.current_line_index = 0
        self.displayed_text = ""
        self.char_index = 0
        self.last_char_time = 0
        self.line_complete = False
        self.waiting_for_input = False  # Whether we're waiting for user input to continue
        
        # Load fonts
        self.load_fonts()
        
        # Load stamp font
        self.stamp_font = None
        try:
            self.stamp_font = pygame.font.Font('assets/fonts/stamp.ttf', 120)  # Increased font size from 80 to 120
        except Exception as e:
            print(f"Error loading stamp font: {e}")
            # Fallback to default font
            self.stamp_font = pygame.font.Font(None, 120)  # Increased font size from 80 to 120
        
        # Create confetti effect
        self.confetti = Confetti(self.screen.get_width(), self.screen.get_height())
        self.show_confetti = False
        
        # Load victory music
        try:
            self.victory_music_loaded = False
            self.victory_music_path = 'assets/sounds/victory.mp3'
        except Exception as e:
            print(f"Error setting up victory music: {e}")
    
    def load_arrest_image(self):
        """Load the arrest image"""
        try:
            image_path = 'assets/images/characters/lisa_arrest.png'
            self.arrest_image = pygame.image.load(image_path).convert_alpha()
            print(f"Successfully loaded arrest image from {image_path}")
        except Exception as e:
            print(f"Error loading arrest image: {e}")
            self.arrest_image = None
    
    def load_fonts(self):
        """Load fonts for text display"""
        try:
            font_path = os.path.join('assets', 'fonts', 'typewriter.ttf')
            if os.path.exists(font_path):
                self.fonts = {}
                # Create fonts of different sizes (including larger sizes for emphasis)
                for size in [24, 28, 32, 36, 38, 42, 48, 52, 60, 72]:
                    self.fonts[size] = pygame.font.Font(font_path, size)
                print("Successfully loaded typewriter fonts")
            else:
                print(f"Warning: Typewriter font not found at {font_path}")
                # Fallback to default font
                self.fonts = {}
                for size in [24, 28, 32, 36, 38, 42, 48, 52, 60, 72]:
                    self.fonts[size] = pygame.font.Font(None, size)
        except Exception as e:
            print(f"Error loading fonts: {e}")
            # Fallback to default font
            self.fonts = {}
            for size in [24, 28, 32, 36, 38, 42, 48, 52, 60, 72]:
                self.fonts[size] = pygame.font.Font(None, size)
        
    def enter(self):
        """Called when entering this state"""
        # Reset animation state
        self.animation_state = "spinning"
        self.animation_start_time = time.time()
        self.spin_angle = 0
        self.image_scale = 2.0
        
        # Reset text display
        self.current_line_index = 0
        self.displayed_text = ""
        self.char_index = 0
        self.last_char_time = 0
        self.line_pause_time = 0
        self.line_complete = False
        
        # Stop any currently playing music
        pygame.mixer.music.stop()
        
        # Load and play victory music
        try:
            pygame.mixer.music.load(self.victory_music_path)
            pygame.mixer.music.set_volume(0.5)  # Set volume to 50%
            pygame.mixer.music.play(-1)  # Loop indefinitely
            self.victory_music_loaded = True
            print("Victory music started")
        except Exception as e:
            print(f"Error playing victory music: {e}")
    
    def handle_event(self, event):
        """Handle user input events"""
        # Handle space key or mouse click during text display
        if self.animation_state == "waiting" and (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN):
            # Continue to the next line
            self.waiting_for_input = False
            self.animation_state = "typing"
            self.current_line_index += 1
            self.displayed_text = ""
            self.char_index = 0
            self.line_complete = False
            return True
        
        # Handle return to menu when all text is displayed
        elif self.current_line_index >= len(self.congrats_lines):
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self.return_to_menu()
                return True
        
        # For other states, only allow return to menu with escape key
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.return_to_menu()
            return True
            
        return False
        
    def return_to_menu(self):
        """Return to the main menu"""
        # Restore original background music when returning to menu
        pygame.mixer.music.stop()
        try:
            pygame.mixer.music.load('assets/sounds/background.mp3')
            pygame.mixer.music.set_volume(0.3)  # Back to 30%
            pygame.mixer.music.play(-1)  # Loop indefinitely
        except Exception as e:
            print(f"Error restoring background music: {e}")
            
        self.game.change_state("menu")
            
        return False
        
    def update(self):
        """Update game state"""
        current_time = time.time()
        
        # Update confetti if it's active - make sure to call this every frame
        if self.show_confetti:
            self.confetti.update()  # This will generate and update confetti particles
        
        # Update spinning animation
        if self.animation_state == "spinning":
            elapsed_time = current_time - self.animation_start_time
            progress = min(elapsed_time / self.spin_duration, 1.0)
            
            # Update spin angle (starts fast, slows down)
            self.spin_angle = 720 * (1 - math.pow(1 - progress, 3))  # Easing function
            
            # Update scale (starts large, gets smaller)
            self.image_scale = 2.0 - (progress * (2.0 - self.final_scale))
            
            # Check if animation is complete
            if progress >= 1.0:
                self.animation_state = "landed"
                self.animation_start_time = current_time  # Reset for next animation phase
                self.show_confetti = True  # Start showing confetti when image lands after landing before starting text
        elif self.animation_state == "landed":
            # Start stamp animation after a brief pause
            if not self.show_stamp and current_time - self.animation_start_time >= 0.5:
                self.show_stamp = True
                self.stamp_start_time = current_time
            
            # Update stamp animation
            if self.show_stamp:
                stamp_progress = min(1.0, (current_time - self.stamp_start_time) / self.stamp_animation_duration)
                
                # Stamp animation - starts large and quickly settles to normal size
                if stamp_progress < 0.5:
                    # Coming in phase - grow quickly
                    self.stamp_scale = 1.0 + (1.0 - stamp_progress * 2) * 0.5
                else:
                    # Settling phase - add a slight bounce
                    bounce_progress = (stamp_progress - 0.5) * 2  # 0 to 1
                    self.stamp_scale = 1.0 + math.sin(bounce_progress * math.pi) * 0.1
            
            # Wait a moment before starting to type (after stamp animation)
            if self.show_stamp and current_time - self.stamp_start_time >= 1.0:  # Wait for stamp + extra time
                self.animation_state = "typing"
                self.animation_start_time = current_time
        
        # Update typewriter text effect
        elif self.animation_state == "typing":
            if self.current_line_index < len(self.congrats_lines):
                current_line = self.congrats_lines[self.current_line_index]
                
                # Add characters with delay
                if current_time - self.last_char_time >= current_line["delay"]:
                    if self.char_index < len(current_line["text"]):
                        # Ensure we're adding characters from left to right
                        self.displayed_text = current_line["text"][:self.char_index + 1]
                        self.char_index += 1
                        self.last_char_time = current_time
                    else:
                        # Line is complete, wait for user input
                        self.line_complete = True
                        self.animation_state = "waiting"
                        self.waiting_for_input = True
            else:
                # All lines have been displayed
                pass
        
    def draw(self):
        """Draw the winning screen"""
        # Fill background with black
        self.screen.fill((0, 0, 0))
        
        # Draw confetti first (behind everything else)
        if self.show_confetti:
            self.confetti.draw(self.screen)
        
        # Draw the arrest image with animation
        if self.arrest_image:
            # Get the center of the screen
            center_x = self.screen.get_width() // 2
            center_y = self.screen.get_height() // 3  # Position in upper third
            
            # Calculate image dimensions based on scale
            orig_width, orig_height = self.arrest_image.get_rect().size
            target_width = int(orig_width * self.image_scale)
            target_height = int(orig_height * self.image_scale)
            
            # Scale the image
            scaled_image = pygame.transform.scale(self.arrest_image, (target_width, target_height))
            
            # Apply rotation if in spinning state
            if self.animation_state == "spinning":
                rotated_image = pygame.transform.rotate(scaled_image, self.spin_angle)
            else:
                rotated_image = scaled_image
            
            # Draw the image
            image_rect = rotated_image.get_rect(center=(center_x, center_y))
            self.screen.blit(rotated_image, image_rect)
            
            # Draw the ARRESTED stamp if it's visible
            if self.show_stamp:
                # Create the stamp text
                stamp_text = "ARRESTED"
                stamp_color = (255, 0, 0)  # Red
                
                # Render the text
                stamp_surface = self.stamp_font.render(stamp_text, True, stamp_color)
                
                # Scale the stamp based on animation
                scaled_stamp = pygame.transform.scale(stamp_surface, (int(stamp_surface.get_width() * self.stamp_scale), int(stamp_surface.get_height() * self.stamp_scale)))
                
                # Rotate the stamp
                rotated_stamp = pygame.transform.rotate(scaled_stamp, self.stamp_angle)
                
                # Position the stamp over the image
                stamp_rect = rotated_stamp.get_rect(center=image_rect.center)
                
                # Draw the stamp
                self.screen.blit(rotated_stamp, stamp_rect)
        
        # Draw congratulatory text
        if self.animation_state in ["typing", "landed", "waiting"]:
            text_y = self.screen.get_height() // 2 + 120  # Much more space between image and text
            
            # Only draw the current line being typed
            if self.current_line_index < len(self.congrats_lines):
                current_line = self.congrats_lines[self.current_line_index]
                font_size = current_line["font_size"]
                font = self.fonts.get(font_size, self.fonts.get(32))
                
                # Handle multi-line text by splitting at newlines or wrapping long lines
                # First, check if the text contains manual line breaks
                if '\n' in self.displayed_text:
                    lines = self.displayed_text.split('\n')
                else:
                    # For long lines, we'll wrap them to fit the screen width
                    max_width = int(self.screen.get_width() * 0.8)  # Use 80% of screen width
                    lines = [self.displayed_text]
                    
                    # If the text is too wide, we would wrap it here
                    # But for now, we'll just display it as is
                
                # Draw each line of text
                line_y = text_y
                for line in lines:
                    if line.strip():  # Only render non-empty lines
                        text_surface = font.render(line, True, current_line["color"])
                        text_rect = text_surface.get_rect(centerx=self.screen.get_width() // 2, top=line_y)
                        self.screen.blit(text_surface, text_rect)
                        line_y += font_size + 5  # Add spacing between lines
                
                # Draw a "continue" prompt if waiting for input
                if self.waiting_for_input:
                    prompt_font = self.fonts.get(24, self.fonts.get(24))
                    prompt_text = "Press any key to continue..."
                    prompt_surface = prompt_font.render(prompt_text, True, (180, 180, 180))
                    prompt_rect = prompt_surface.get_rect(centerx=self.screen.get_width() // 2, top=text_y + font_size + 40)
                    self.screen.blit(prompt_surface, prompt_rect)
            
            # If all lines have been displayed, show a final prompt
            elif self.current_line_index >= len(self.congrats_lines):
                prompt_font = self.fonts.get(28, self.fonts.get(28))
                prompt_text = "Press any key to return to the menu"
                prompt_surface = prompt_font.render(prompt_text, True, (200, 200, 200))
                prompt_rect = prompt_surface.get_rect(centerx=self.screen.get_width() // 2, top=text_y + 40)
                self.screen.blit(prompt_surface, prompt_rect)
