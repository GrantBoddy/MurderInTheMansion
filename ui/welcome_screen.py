import pygame
import time
from dsl.intro_parser import load_intro_sequence

class WelcomeScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        
        # Load typewriter font
        try:
            self.font_large = pygame.font.Font('assets/fonts/typewriter.ttf', 48)
            self.font_medium = pygame.font.Font('assets/fonts/typewriter.ttf', 36)
            self.font_small = pygame.font.Font('assets/fonts/typewriter.ttf', 24)
            print("Loaded typewriter font for welcome screen")
        except Exception as e:
            print(f"Error loading typewriter font: {e}")
            # Fallback to default fonts
            self.font_large = pygame.font.Font(None, 48)
            self.font_medium = pygame.font.Font(None, 36)
            self.font_small = pygame.font.Font(None, 24)
        
        # Load background image
        try:
            self.background = pygame.image.load('assets/images/backgrounds/crime_scene.PNG')
            self.background = pygame.transform.scale(self.background, 
                                                    (self.screen.get_width(), self.screen.get_height()))
        except Exception as e:
            print(f"Error loading crime scene background: {e}")
            # Create a fallback dark background
            self.background = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
            self.background.fill((20, 20, 30))  # Dark blue-gray
        
        # Load cop character image with high quality scaling
        try:
            self.character_image = pygame.image.load('assets/images/characters/cop2.png')
            
            # Use smoothscale for better quality
            target_height = int(self.screen.get_height() * 0.8)
            ratio = target_height / self.character_image.get_height()
            target_width = int(self.character_image.get_width() * ratio)
            
            # Use smoothscale for better quality scaling
            self.character_image = pygame.transform.smoothscale(self.character_image, (target_width, target_height))
            
            # Position character on the left side of the screen
            self.character_position = (50, self.screen.get_height() - target_height)
            print("Loaded cop character image for welcome screen")
        except Exception as e:
            print(f"Error loading cop character image: {e}")
            self.character_image = None
            self.character_position = (0, 0)
        
        # Load dialogue from DSL
        try:
            self.dialogue_sequence = load_intro_sequence()
            self.dialogue_lines = [line['text'] for line in self.dialogue_sequence.get_lines()]
            # Skip the first 3 lines which are for the intro screen
            self.dialogue_lines = self.dialogue_lines[3:]
            print(f"Loaded {len(self.dialogue_lines)} dialogue lines for welcome screen")
        except Exception as e:
            print(f"Error loading dialogue sequence: {e}")
            # Fallback dialogue
            self.dialogue_lines = [
                "Thank God you're here, Detective! We've got a murder case on our hands.",
                "The victim, John Wallace, was found dead in his study around 4:00 AM.",
                "Go ahead and review everything, then start questioning the suspects."
            ]
        
        # Dialogue display variables
        self.current_line_index = 0
        self.current_displayed_text = ""
        self.typewriter_index = 0
        self.last_char_time = 0
        self.char_delay = 0.01  # Faster typing for dialogue
        self.typewriter_complete = False
        
        # Dialogue box dimensions
        self.dialogue_box_rect = pygame.Rect(
            20, 
            self.screen.get_height() - 180, 
            self.screen.get_width() - 40, 
            150
        )
        
        # Continue button
        self.continue_button_rect = pygame.Rect(
            self.screen.get_width() - 200,
            self.screen.get_height() - 60,
            180,
            40
        )
        self.continue_text = "Continue"
        self.button_hovered = False
        
        # Evidence board button (initially hidden, shown after all dialogue)
        try:
            self.evidence_board_image = pygame.image.load('assets/images/backgrounds/full_board.png')
            # Scale to a thumbnail size
            thumbnail_size = (150, 120)
            self.evidence_board_image = pygame.transform.smoothscale(self.evidence_board_image, thumbnail_size)
            print("Loaded evidence board thumbnail")
        except Exception as e:
            print(f"Error loading evidence board thumbnail: {e}")
            # Create a fallback thumbnail
            self.evidence_board_image = pygame.Surface((150, 120))
            self.evidence_board_image.fill((100, 100, 100))
            font = pygame.font.Font(None, 20)
            text = font.render("Evidence Board", True, (255, 255, 255))
            text_rect = text.get_rect(center=(75, 60))
            self.evidence_board_image.blit(text, text_rect)
        
        # Position in top right corner
        self.evidence_board_rect = pygame.Rect(
            self.screen.get_width() - 170,
            20,
            150,
            120
        )
        self.evidence_board_visible = False
        self.evidence_board_hovered = False
        self.all_dialogue_shown = False
    
    def handle_event(self, event):
        """Handle user input events"""
        # Track mouse position for button hover effects
        if event.type == pygame.MOUSEMOTION:
            self.button_hovered = self.continue_button_rect.collidepoint(event.pos)
            if self.evidence_board_visible:
                self.evidence_board_hovered = self.evidence_board_rect.collidepoint(event.pos)
            else:
                self.evidence_board_hovered = False
        
        # Handle clicks
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            # Check if evidence board is visible and clicked
            if self.evidence_board_visible and self.evidence_board_rect.collidepoint(event.pos):
                print("Evidence board clicked, transitioning to evidence board screen")
                self.game.change_state("evidence_board")
                return True
                
            # Check if clicking continue button
            if self.continue_button_rect.collidepoint(event.pos):
                self.advance_dialogue()
                return True
        
        # Handle keyboard input (only for dialogue advancement, not for evidence board)
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN) and not self.all_dialogue_shown:
                self.advance_dialogue()
                return True
        
        return False
    
    def advance_dialogue(self):
        """Advance to the next line of dialogue or show evidence board button"""
        # If current line is not fully displayed, show it all immediately
        if not self.typewriter_complete:
            self.current_displayed_text = self.dialogue_lines[self.current_line_index]
            self.typewriter_complete = True
            return
        
        # Move to next line
        self.current_line_index += 1
        
        # If we've shown all dialogue, show evidence board button
        if self.current_line_index >= len(self.dialogue_lines):
            print("Dialogue complete, showing evidence board button")
            self.evidence_board_visible = True
            self.all_dialogue_shown = True
            # Change continue button text to indicate what to do next
            self.continue_text = "Click Evidence Board"
            return
        
        # Reset typewriter effect for the new line
        self.current_displayed_text = ""
        self.typewriter_index = 0
        self.typewriter_complete = False
        self.last_char_time = time.time()
    
    def update(self):
        """Update typewriter effect for dialogue"""
        if not self.typewriter_complete:
            current_time = time.time()
            
            # If it's time to add a new character
            if current_time - self.last_char_time >= self.char_delay:
                self.last_char_time = current_time
                
                # Get the full text we're currently displaying
                full_text = self.dialogue_lines[self.current_line_index]
                
                # Add one more character if we haven't shown the full text
                if self.typewriter_index < len(full_text):
                    self.current_displayed_text = full_text[:self.typewriter_index + 1]
                    self.typewriter_index += 1
                else:
                    self.typewriter_complete = True
    
    def draw(self):
        """Draw the welcome screen with background, character and dialogue"""
        # Draw background
        self.screen.blit(self.background, (0, 0))
        
        # Draw character if loaded
        if self.character_image:
            self.screen.blit(self.character_image, self.character_position)
        
        # Draw evidence board button if visible
        if self.evidence_board_visible:
            # Draw a glowing effect if hovered
            if self.evidence_board_hovered:
                # Draw a slightly larger glow behind the image
                glow_rect = self.evidence_board_rect.inflate(10, 10)
                pygame.draw.rect(self.screen, (255, 255, 150, 128), glow_rect)  # Yellow glow
            
            # Draw the evidence board image
            self.screen.blit(self.evidence_board_image, self.evidence_board_rect)
            
            # Draw a border around the image
            border_color = (255, 255, 0) if self.evidence_board_hovered else (255, 255, 255)
            pygame.draw.rect(self.screen, border_color, self.evidence_board_rect, 2)  # Border
            
            # Draw a label below the image
            label_text = self.font_small.render("Evidence Board", True, (255, 255, 255))
            label_rect = label_text.get_rect(centerx=self.evidence_board_rect.centerx, 
                                            top=self.evidence_board_rect.bottom + 5)
            self.screen.blit(label_text, label_rect)
        
        # Draw dialogue box
        pygame.draw.rect(self.screen, (0, 0, 0, 200), self.dialogue_box_rect)  # Semi-transparent black
        pygame.draw.rect(self.screen, (255, 255, 255), self.dialogue_box_rect, 2)  # White border
        
        # Draw current dialogue text
        if self.current_line_index < len(self.dialogue_lines):
            # Wrap text to fit dialogue box
            wrapped_text = self.wrap_text(self.current_displayed_text, self.font_medium, 
                                         self.dialogue_box_rect.width - 40)
            
            # Draw each line of wrapped text
            for i, line in enumerate(wrapped_text):
                text_surface = self.font_medium.render(line, True, (255, 255, 255))
                text_rect = text_surface.get_rect(
                    x=self.dialogue_box_rect.left + 20,
                    y=self.dialogue_box_rect.top + 20 + (i * 30)
                )
                self.screen.blit(text_surface, text_rect)
        
        # Only draw continue button if not all dialogue shown or evidence board not visible yet
        if not self.all_dialogue_shown or not self.evidence_board_visible:
            button_color = (100, 0, 0) if self.button_hovered else (50, 0, 0)
            pygame.draw.rect(self.screen, button_color, self.continue_button_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), self.continue_button_rect, 2)  # White border
            
            # Draw button text
            button_text = self.font_small.render(self.continue_text, True, (255, 255, 255))
            button_text_rect = button_text.get_rect(center=self.continue_button_rect.center)
            self.screen.blit(button_text, button_text_rect)
    
    def wrap_text(self, text, font, max_width):
        """Wrap text to fit within a given width"""
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            # Try adding the word to the current line
            test_line = ' '.join(current_line + [word])
            test_width = font.size(test_line)[0]
            
            if test_width <= max_width:
                # Word fits, add it to the current line
                current_line.append(word)
            else:
                # Word doesn't fit, start a new line
                if current_line:  # Only add if there's text in the current line
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        # Add the last line if it's not empty
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
