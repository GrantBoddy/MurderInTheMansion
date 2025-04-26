import pygame
import time

class AnswerScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        
        # Load the select text image
        self.select_text = pygame.image.load('assets/images/other/select_text.png')
        
        # Load character images
        original_images = {
            'alex': pygame.image.load('assets/images/characters/alex.png'),
            'mary': pygame.image.load('assets/images/characters/mary.png'),
            'lisa': pygame.image.load('assets/images/characters/lisa.png'),
            'emily': pygame.image.load('assets/images/characters/emily.png'),
            'tom': pygame.image.load('assets/images/characters/tom.png')
        }
        
        # Resize images to be much smaller (150px height)
        self.character_images = {}
        for char_id, img in original_images.items():
            # Get original dimensions
            orig_width, orig_height = img.get_size()
            # Calculate new dimensions maintaining aspect ratio
            new_height = 150  # Much smaller height
            new_width = int(orig_width * (new_height / orig_height))
            # Scale the image with better quality
            self.character_images[char_id] = pygame.transform.smoothscale(img, (new_width, new_height))
        
        # Character positions (evenly spaced horizontally)
        screen_width = self.screen.get_width()
        self.character_positions = {
            'alex': (screen_width * 0.2, 300),
            'mary': (screen_width * 0.35, 300),
            'lisa': (screen_width * 0.5, 300),
            'emily': (screen_width * 0.65, 300),
            'tom': (screen_width * 0.8, 300)
        }
        
        # Character names to display
        self.character_names = {
            'alex': "Alex",
            'mary': "Mary",
            'lisa': "Lisa",
            'emily': "Emily",
            'tom': "Tom"
        }
        
        # Selected character (None initially)
        self.selected_character = None
        
        # Confirmation UI elements
        self.showing_confirmation = False
        self.sure_text = pygame.image.load('assets/images/other/sure_text.png')
        self.yes_normal = pygame.image.load('assets/images/other/yes_normal.png')
        self.yes_hover = pygame.image.load('assets/images/other/yes_hover.png')
        self.yes_button_hovered = False
        
    def handle_event(self, event):
        """Handle user input events"""
        # Track mouse position for hover effects
        mouse_pos = pygame.mouse.get_pos()
        
        # Handle confirmation UI if it's showing
        if self.showing_confirmation:
            # Get yes button rect
            screen_width = self.screen.get_width()
            yes_rect = self.yes_normal.get_rect(center=(screen_width * 0.7, 450))
            
            # Check for hover
            self.yes_button_hovered = yes_rect.collidepoint(mouse_pos)
            
            # Check for click on yes button
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and yes_rect.collidepoint(event.pos):
                # Start the fade effect and transition to suspense screen
                self.game.transition.start_fade("suspense_screen", fade_out_music=True)
                return True
            
            # Allow canceling the confirmation by clicking elsewhere or pressing escape
            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not yes_rect.collidepoint(event.pos)) or \
               (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.showing_confirmation = False
                return True
                
            # Check if clicking on back button while confirmation is showing
            back_rect = pygame.Rect(20, 20, 100, 40)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and back_rect.collidepoint(event.pos):
                self.showing_confirmation = False  # Hide confirmation
                self.game.change_state("evidence_board")
                return True
                
            # Check if clicking on a different character while confirmation is showing
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for char_id, pos in self.character_positions.items():
                    char_rect = self.character_images[char_id].get_rect(center=pos)
                    if char_rect.collidepoint(event.pos):
                        self.selected_character = char_id  # Change selection
                        return True
            
        # Handle main screen UI
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                # Check if clicking on back button
                back_rect = pygame.Rect(20, 20, 100, 40)
                if back_rect.collidepoint(event.pos):
                    self.game.change_state("evidence_board")
                    return True
                    
                # Check if clicking on a character
                for char_id, pos in self.character_positions.items():
                    # Create a rect for the character image
                    char_rect = self.character_images[char_id].get_rect(center=pos)
                    if char_rect.collidepoint(event.pos):
                        self.selected_character = char_id
                        self.showing_confirmation = True  # Show confirmation UI
                        print(f"Selected {char_id} as the murderer")
                        return True
                        
        # Add a way to return to the evidence board
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.change_state("evidence_board")
                return True
                
        return False
        
    def update(self):
        """Update game state"""
        pass
        
    def draw(self):
        """Draw the answer screen"""
        # Clear screen with black background
        self.screen.fill((0, 0, 0))
        
        # Draw the select text at the top
        text_rect = self.select_text.get_rect(centerx=self.screen.get_width() // 2, top=50)
        self.screen.blit(self.select_text, text_rect)
        
        # Draw back button
        back_rect = pygame.Rect(20, 20, 100, 40)
        pygame.draw.rect(self.screen, (150, 0, 0), back_rect)  # Red color
        pygame.draw.rect(self.screen, (255, 255, 255), back_rect, 2)  # White border
        back_font = pygame.font.Font(None, 28)
        back_text = back_font.render('Back', True, (255, 255, 255))
        back_text_rect = back_text.get_rect(center=back_rect.center)
        self.screen.blit(back_text, back_text_rect)
        
        # Draw each character
        font = pygame.font.Font(None, 36)
        for char_id, pos in self.character_positions.items():
            # Draw character image
            char_image = self.character_images[char_id]
            char_rect = char_image.get_rect(center=pos)
            
            # Highlight selected character
            if self.selected_character == char_id:
                # Draw a highlight around the selected character
                highlight_rect = char_rect.inflate(20, 20)
                pygame.draw.rect(self.screen, (255, 0, 0), highlight_rect, 3)  # Red highlight
                
            self.screen.blit(char_image, char_rect)
            
            # Draw character name below image
            name_text = font.render(self.character_names[char_id], True, (255, 255, 255))
            name_rect = name_text.get_rect(centerx=pos[0], top=pos[1] + char_rect.height // 2 + 10)
            self.screen.blit(name_text, name_rect)
        
        # Draw confirmation UI if showing
        if self.showing_confirmation:
            screen_width = self.screen.get_width()
            
            # Draw "ARE YOU SURE??" text on the left
            sure_rect = self.sure_text.get_rect(center=(screen_width * 0.3, 450))
            self.screen.blit(self.sure_text, sure_rect)
            
            # Draw YES button on the right with hover effect
            yes_rect = self.yes_normal.get_rect(center=(screen_width * 0.7, 450))
            
            # Use hover image if hovered
            if self.yes_button_hovered:
                self.screen.blit(self.yes_hover, yes_rect)
            else:
                self.screen.blit(self.yes_normal, yes_rect)
