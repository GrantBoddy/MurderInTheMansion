import pygame
import time

class ExplainScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        
        # Load fonts
        try:
            self.title_font = pygame.font.Font('assets/fonts/bloody.ttf', 60)
            self.text_font = pygame.font.Font('assets/fonts/typewriter.ttf', 28)
            self.button_font = pygame.font.Font('assets/fonts/typewriter.ttf', 36)
            print("Loaded fonts for explain screen")
        except Exception as e:
            print(f"Error loading fonts for explain screen: {e}")
            # Fallback to default fonts
            self.title_font = pygame.font.Font(None, 60)
            self.text_font = pygame.font.Font(None, 28)
            self.button_font = pygame.font.Font(None, 36)
            
        # Button for returning to menu
        self.return_button = {
            "text": "Return to Menu",
            "rect": None,
            "hovered": False
        }
        
        # Explanation text
        self.explanation_title = "The Truth Revealed"
        self.explanation_text = [
            "You were wrong.",
            "The real murderer was Lisa Carter, John Wallace’s assistant.",
            "John had uncovered damning evidence of Lisa’s embezzlement.",
            "But instead of calling the police immediately, he gave her one final chance.",
            "He invited her to his home office for a late-night meeting…",
            "not to punish her, but to hear her out.",
            "But Lisa didn’t come looking for forgiveness.", 
            "She came prepared to protect herself, no matter the cost…..",
            "When John confronted her with the evidence, things got heated.",
            "Lisa panicked.",
            "She realized the walls were closing in, the money trail was obvious….", 
            "John had enough to ruin her life.", 
            "So, in a desperate, split-second decision, she improvised a brutal plan.",
            "She slipped out of the study,", 
            "went to Alex Wallace’s old bedroom,", 
            "and retrieved one of his guns.......", 
            "a Glock 19.",
            "Then, she returned to the study and shot John Wallace in the head.",
            "To cover her tracks, she wiped the gun clean and quietly returned", 
            "it to Alex’s room to frame him for the murder!!", 
            "It just so happened, that the murder happened", 
            "on the night the clocks sprang forward for", 
            "Daylight Saving Time on March 12, 2023.",
            "This wasn't clear because several pieces of evidence", 
            "(like security logs and receipts) were not adjusted for DST.", 
            "That meant her real exit at 3:41 AM appeared in the logs as 2:41 AM.",
            "So, when Tom the neighbor heard the gunshot at 3:34", 
            "and Lisa had already left at 2:41", 
            "she seemed to be in the clear.",
            "She even had a gas station receipt timestamped at 3:15", 
            "which looked like solid proof she was miles away.",
            "When the real timeline is restored, the picture becomes clear:", 
            "Lisa never left before the murder…..", 
            "she committed it,", 
            "cleaned up,", 
            "and only then slipped away,",
            "hiding in plain sight behind the illusion of time.",
            "She then killed you to cover her tracks.",
            "You missed it. But time never lies.",
            ""
        ]
        
        # Scrolling variables
        self.scroll_position = 0
        self.max_scroll = 0  # Will be calculated in draw
        self.scroll_speed = 30
        
    def enter(self):
        """Called when entering this state"""
        # Reset scroll position
        self.scroll_position = 0
        
        # Only adjust volume, don't restart the music
        # First check if music is already playing to avoid restarting it
        
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.set_volume(0.2)  # 20% volume
        else:
            # If music isn't playing for some reason, don't try to start it here
            # The main game loop will handle this
            print("Music not playing in explain screen, will be handled by main loop")
        
    def handle_event(self, event):
        """Handle user input events"""
        # Handle mouse movement for button hover
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            if self.return_button["rect"] and self.return_button["rect"].collidepoint(mouse_pos):
                self.return_button["hovered"] = True
            else:
                self.return_button["hovered"] = False
                
        # Handle button click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            mouse_pos = pygame.mouse.get_pos()
            if self.return_button["rect"] is not None and self.return_button["rect"].collidepoint(mouse_pos):
                # Return to menu
                pygame.mixer.music.set_volume(0.3)  # Restore volume
                self.game.change_state("menu")
                return True
                
        # Handle scrolling with mouse wheel
        if event.type == pygame.MOUSEWHEEL:
            self.scroll_position += event.y * self.scroll_speed
            # Clamp scroll position
            self.scroll_position = max(min(self.scroll_position, 0), -self.max_scroll)
                
        # Handle scrolling with keyboard
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.scroll_position += self.scroll_speed
                # Clamp scroll position
                self.scroll_position = min(self.scroll_position, 0)
            elif event.key == pygame.K_DOWN:
                self.scroll_position -= self.scroll_speed
                # Clamp scroll position
                self.scroll_position = max(self.scroll_position, -self.max_scroll)
                
        return True
        
    def update(self):
        """Update game state"""
        pass
        
    def draw(self):
        """Draw the explain screen"""
        # Dark background
        self.screen.fill((10, 10, 10))
        
        # Draw title
        title_surface = self.title_font.render(self.explanation_title, True, (200, 0, 0))
        title_rect = title_surface.get_rect(centerx=self.screen.get_width() // 2, top=50)
        self.screen.blit(title_surface, title_rect)
        
        # Draw explanation text
        text_y = 150 + self.scroll_position
        line_height = 40
        
        # Calculate total height for scrolling
        total_height = len(self.explanation_text) * line_height
        visible_height = self.screen.get_height() - 250  # Space for title and button
        self.max_scroll = max(0, total_height - visible_height)
        
        # Create a clipping rect for the text area
        text_area_rect = pygame.Rect(50, 150, self.screen.get_width() - 100, visible_height)
        
        # Store original clip area
        original_clip = self.screen.get_clip()
        
        # Set clip area to text area
        self.screen.set_clip(text_area_rect)
        
        # Draw text lines
        for i, line in enumerate(self.explanation_text):
            line_y = text_y + (i * line_height)
            
            # Only draw lines that are visible
            if line_y > 120 and line_y < self.screen.get_height() - 100:
                text_surface = self.text_font.render(line, True, (220, 220, 220))
                text_rect = text_surface.get_rect(centerx=self.screen.get_width() // 2, top=line_y)
                self.screen.blit(text_surface, text_rect)
                
        # Restore original clip area
        self.screen.set_clip(original_clip)
        
        # Draw scroll indicators if needed
        if self.max_scroll > 0:
            if self.scroll_position < 0:
                # Draw up arrow
                pygame.draw.polygon(self.screen, (150, 150, 150), [
                    (self.screen.get_width() - 30, 160),
                    (self.screen.get_width() - 20, 140),
                    (self.screen.get_width() - 10, 160)
                ])
                
            if self.scroll_position > -self.max_scroll:
                # Draw down arrow
                pygame.draw.polygon(self.screen, (150, 150, 150), [
                    (self.screen.get_width() - 30, self.screen.get_height() - 160),
                    (self.screen.get_width() - 20, self.screen.get_height() - 140),
                    (self.screen.get_width() - 10, self.screen.get_height() - 160)
                ])
        
        # Draw return button
        button_color = (255, 0, 0) if self.return_button["hovered"] else (150, 150, 150)
        button_surface = self.button_font.render(self.return_button["text"], True, button_color)
        button_rect = button_surface.get_rect(centerx=self.screen.get_width() // 2, bottom=self.screen.get_height() - 50)
        self.return_button["rect"] = button_rect
        self.screen.blit(button_surface, button_rect)
