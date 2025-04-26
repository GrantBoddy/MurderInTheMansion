import pygame
import os

class InterrogationMenu:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        
        # Load background
        self.background = None
        self.load_background()
        
        # Available interrogations
        self.interrogations = [
            {"name": "Alex", "id": "alex_interrogation", "available": True},
            {"name": "Mary", "id": "mary_interrogation", "available": False},
            {"name": "Lisa", "id": "lisa_interrogation", "available": False},
            {"name": "Emily", "id": "emily_interrogation", "available": False},
            {"name": "Alex (2nd)", "id": "alex_2_interrogation", "available": False}
        ]
        
        # Track completed interrogations
        self.completed_interrogations = set()
        
        # Check if Alex's interrogation has been completed
        self.check_completed_interrogations()
        
        # Button dimensions and positions
        self.button_width = 200
        self.button_height = 60
        self.button_padding = 20
        self.buttons = []
        self.update_buttons()
        
        # Load typewriter font
        try:
            font_path = os.path.join('assets', 'fonts', 'typewriter.ttf')
            self.title_font = pygame.font.Font(font_path, 60)  # Slightly smaller than default 72
            self.button_font = pygame.font.Font(font_path, 30)  # Slightly smaller than default 36
        except Exception as e:
            print(f"Error loading typewriter font: {e}")
            # Fallback to default font
            self.title_font = pygame.font.Font(None, 72)
            self.button_font = pygame.font.Font(None, 36)
        
        # Hover tracking
        self.hovered_button_index = -1  # Index of the button being hovered (-1 means none)
        self.back_button_hovered = False
        
    def load_background(self):
        """Load the interrogation room background"""
        try:
            bg_path = 'assets/images/backgrounds/interrogation_room.png'
            self.background = pygame.image.load(bg_path).convert()
            # Scale to screen size
            self.background = pygame.transform.scale(self.background, 
                                                  (self.screen.get_width(), self.screen.get_height()))
        except Exception as e:
            print(f"Error loading interrogation room background: {e}")
            self.background = None
            
    def update_buttons(self):
        """Update the list of interrogation buttons based on availability"""
        self.buttons = []
        
        # Calculate starting position
        start_x = (self.screen.get_width() - self.button_width) // 2
        start_y = 200
        
        # Create buttons for available interrogations
        available_count = 0
        for interrogation in self.interrogations:
            if interrogation["available"]:
                button_rect = pygame.Rect(
                    start_x,
                    start_y + available_count * (self.button_height + self.button_padding),
                    self.button_width,
                    self.button_height
                )
                self.buttons.append({
                    "rect": button_rect,
                    "text": interrogation["name"],
                    "id": interrogation["id"]
                })
                available_count += 1
    
    def check_completed_interrogations(self):
        """Check which interrogations have been completed and update availability"""
        # If Alex's interrogation is completed, make Mary's available
        if "alex_interrogation" in self.completed_interrogations and not self.interrogations[1]["available"]:
            self.interrogations[1]["available"] = True
            self.update_buttons()
            
        # If Lisa's interrogation is completed, make Emily's available
        if "lisa_interrogation" in self.completed_interrogations and not self.interrogations[3]["available"]:
            self.interrogations[3]["available"] = True
            self.update_buttons()
            
        # Alex's second interrogation is only made available through the evidence board
        # after viewing the ballistics report and completing Emily's interrogation
            
    def handle_event(self, event):
        """Handle user input events"""
        # Track mouse position for hover effects
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
            
            # Reset hover states
            self.hovered_button_index = -1
            self.back_button_hovered = False
            
            # Check for button hovers
            for i, button in enumerate(self.buttons):
                if button["rect"].collidepoint(mouse_pos):
                    self.hovered_button_index = i
                    break
            
            # Check for back button hover
            back_rect = pygame.Rect(20, 20, 100, 40)
            if back_rect.collidepoint(mouse_pos):
                self.back_button_hovered = True
                
            return True
        
        # Handle mouse clicks
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            mouse_pos = event.pos
            
            # Check for button clicks
            for button in self.buttons:
                if button["rect"].collidepoint(mouse_pos):
                    # Start the selected interrogation
                    interrogation_id = button["id"]
                    self.game.start_interrogation(interrogation_id)
                    
                    # Mark this interrogation as completed
                    self.completed_interrogations.add(interrogation_id)
                    
                    # Check if this completion unlocks new interrogations
                    self.check_completed_interrogations()
                    return True
                    
            # Check for back button click
            back_rect = pygame.Rect(20, 20, 100, 40)
            if back_rect.collidepoint(mouse_pos):
                self.game.change_state("evidence_board")
                return True
                
        return False
    
    def update(self):
        """Update interrogation menu state"""
        pass
    
    def draw(self):
        """Draw the interrogation menu screen"""
        # Draw background
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            # Fallback to plain background
            self.screen.fill((30, 30, 30))
        
        # Draw title
        title_text = "Interrogations"
        title_surface = self.title_font.render(title_text, True, (255, 255, 255))
        title_rect = title_surface.get_rect(centerx=self.screen.get_width() // 2, top=50)
        self.screen.blit(title_surface, title_rect)
        
        # Draw back button - grey by default, red when hovered
        back_rect = pygame.Rect(20, 20, 100, 40)
        back_color = (200, 0, 0) if self.back_button_hovered else (80, 80, 80)
        pygame.draw.rect(self.screen, back_color, back_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), back_rect, 2)  # White border
        back_text = self.button_font.render("Back", True, (255, 255, 255))
        back_text_rect = back_text.get_rect(center=back_rect.center)
        self.screen.blit(back_text, back_text_rect)
        
        # Draw interrogation buttons
        for i, button in enumerate(self.buttons):
            # Determine button color - grey by default, red when hovered
            is_hovered = (i == self.hovered_button_index)
            button_color = (200, 0, 0) if is_hovered else (80, 80, 80)
            
            # Draw button background
            pygame.draw.rect(self.screen, button_color, button["rect"])
            pygame.draw.rect(self.screen, (255, 255, 255), button["rect"], 2)  # White border
            
            # Draw button text
            text_surface = self.button_font.render(button["text"], True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=button["rect"].center)
            self.screen.blit(text_surface, text_rect)
