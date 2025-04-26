import pygame

class DialogueBox:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.current_dialogue = []
        self.current_index = 0
        self.choices = []
        self.selected_choice = 0
        self.character_image = None
        self.character_position = (0, 0)
        self.target_position = (0, 0)
        self.background = None
        self.character_entry_timer = 0
        self.character_entry_duration = 2000  # 2 seconds
        self.character_entering = False
        self.show_evidence_button = False
        
    def start_dialogue(self, dialogue_data, character_data=None, background=None):
        """Start a new dialogue sequence"""
        if isinstance(dialogue_data, list):
            self.current_dialogue = dialogue_data
        else:
            self.current_dialogue = [dialogue_data]
        
        self.current_index = 0
        self.choices = []
        self.selected_choice = 0
        
        if character_data:
            try:
                # Load and scale character image
                original_image = pygame.image.load(character_data['image'])
                # Scale to be fully visible on screen
                screen_height = self.screen.get_height()
                # Calculate height to fit from top of dialogue box to top of screen
                available_height = screen_height - 100  # Account for dialogue box height + margin
                target_height = available_height
                ratio = target_height / original_image.get_height()
                new_width = int(original_image.get_width() * ratio * 1.5)  # Width ratio
                self.character_image = pygame.transform.scale(original_image, (new_width, target_height))
                
                # Position character at the bottom of the screen
                screen_height = self.screen.get_height()
                x_pos = 10  # Almost aligned with left edge of screen
                # Y position calculated to align bottom of image with bottom of screen minus dialogue box
                y_pos = screen_height - self.character_image.get_height() - 60  # 60px for dialogue box
                
                # Place character immediately in final position (no animation)
                self.character_position = (x_pos, y_pos)
                self.character_entering = False
            except Exception as e:
                print(f"Error loading character image: {e}")
                self.character_image = None
            
        if background:
            try:
                self.background = pygame.image.load(background)
            except Exception as e:
                print(f"Error loading background image: {e}")
                self.background = None
            
    def handle_event(self, event):
        if self.character_entering:
            # Don't handle input while character is entering
            return
            
        if self.show_evidence_button:
            # Handle evidence button interaction - click only
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                # Check if click is on evidence button
                button_rect = self.get_evidence_button_rect()
                if button_rect.collidepoint(event.pos):
                    self.game.change_state("evidence_board")
        else:
            # Normal dialogue advancement
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.advance_dialogue()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                self.advance_dialogue()
            
    def advance_dialogue(self):
        """Advance to the next line of dialogue"""
        if self.current_index < len(self.current_dialogue) - 1:
            self.current_index += 1
        else:
            # On last dialogue, show evidence button
            self.show_evidence_button = True
                        
    def handle_choice(self, choice):
        """Handle a dialogue choice selection"""
        # TODO: Implement choice consequences
        self.choices = []
        self.current_index += 1
        
    def get_choice_rect(self, index):
        """Get the rectangle for a choice button"""
        screen_rect = self.screen.get_rect()
        width = 400
        height = 40
        x = screen_rect.centerx - width // 2
        y = screen_rect.bottom - 200 + index * (height + 10)
        return pygame.Rect(x, y, width, height)
        
    def update(self):
        # No animations to update
        pass
        
    def get_evidence_button_rect(self):
        """Get the rectangle for the evidence button in top-right corner"""
        try:
            # Try to load the bulletin board image as the button
            self.evidence_logo = pygame.image.load("assets/images/backgrounds/full_board.png")
            
            # Calculate size to maintain aspect ratio while keeping height around 160px
            original_width = self.evidence_logo.get_width()
            original_height = self.evidence_logo.get_height()
            button_height = 160  # Target height
            button_width = int(original_width * (button_height / original_height))
            
            # Scale the image to maintain proportions
            self.evidence_logo = pygame.transform.scale(self.evidence_logo, (button_width, button_height))
        except Exception as e:
            print(f"Error loading evidence logo: {e}")
            button_width = 160
            button_height = 160
            self.evidence_logo = None
            
        # Position in top-right corner with some padding
        screen_rect = self.screen.get_rect()
        return pygame.Rect(
            screen_rect.right - button_width - 30,  # 30px from right edge
            30,  # 30px from top
            button_width,
            button_height
        )
        
    def draw(self):
        # Draw background if available
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill((20, 20, 20))
            
        # Draw character if available
        if self.character_image:
            self.screen.blit(self.character_image, self.character_position)
            
        # Draw evidence button if on last dialogue
        if self.show_evidence_button:
            button_rect = self.get_evidence_button_rect()
            
            if hasattr(self, 'evidence_logo') and self.evidence_logo:
                # Draw the evidence logo image
                self.screen.blit(self.evidence_logo, button_rect.topleft)
                
                # No text hint - button is click-only
            else:
                # Fallback to text button if image couldn't be loaded
                pygame.draw.rect(self.screen, (40, 40, 40), button_rect)
                pygame.draw.rect(self.screen, (200, 0, 0), button_rect, 2)  # Red border
                
                # Draw button text
                font = pygame.font.Font(None, 28)
                text = font.render("View Evidence (E)", True, (255, 255, 255))
                text_rect = text.get_rect(center=button_rect.center)
                self.screen.blit(text, text_rect)
            
        # Draw dialogue box - at the very bottom of the screen
        box_height = 60
        box_rect = pygame.Rect(0, self.screen.get_height() - box_height, 
                             self.screen.get_width(), box_height)
        pygame.draw.rect(self.screen, (40, 40, 40), box_rect)
        pygame.draw.rect(self.screen, (200, 0, 0), box_rect, 2)  # Red border
            
        # Draw current dialogue text
        if self.current_dialogue and self.current_index < len(self.current_dialogue):
            font = pygame.font.Font(None, 28)  # Smaller font size
            current_text = str(self.current_dialogue[self.current_index])  # Convert to string
            
            # Add text wrapping for long lines
            words = current_text.split(' ')
            lines = []
            line = ""
            for word in words:
                test_line = line + word + " "
                # If the line is too long, start a new line
                if font.size(test_line)[0] > box_rect.width - 40:
                    lines.append(line)
                    line = word + " "
                else:
                    line = test_line
            lines.append(line)  # Add the last line
            
            # Render each line (centered)
            for i, line in enumerate(lines):
                text = font.render(line, True, (255, 255, 255))
                # Center text horizontally in the box
                text_rect = text.get_rect(centerx=box_rect.centerx, top=box_rect.top + 10 + i * 30)
                self.screen.blit(text, text_rect)
            
            # Draw choices if available
            if self.choices:
                for i, choice in enumerate(self.choices):
                    choice_rect = self.get_choice_rect(i)
                    color = (200, 0, 0) if i == self.selected_choice else (100, 100, 100)
                    pygame.draw.rect(self.screen, color, choice_rect)
                    pygame.draw.rect(self.screen, (200, 0, 0), choice_rect, 2)
                    
                    choice_text = str(choice.get('text', ''))
                    text = font.render(choice_text, True, (255, 255, 255))
                    text_rect = text.get_rect(center=choice_rect.center)
                    self.screen.blit(text, text_rect)
                    
            # Draw continue prompt if no choices
            elif self.current_index < len(self.current_dialogue) - 1:
                prompt_font = pygame.font.Font(None, 22)
                prompt = prompt_font.render("Press SPACE or click to continue...", True, (200, 200, 200))
                prompt_rect = prompt.get_rect(right=box_rect.right - 20, bottom=box_rect.bottom - 10)
                self.screen.blit(prompt, prompt_rect)
                
                # Add a blinking arrow indicator
                current_time = pygame.time.get_ticks()
                if (current_time // 500) % 2 == 0:  # Blink every half second
                    arrow = prompt_font.render("▼", True, (200, 0, 0))
                    arrow_rect = arrow.get_rect(right=box_rect.right - 10, bottom=box_rect.bottom - 10)
                    self.screen.blit(arrow, arrow_rect) 