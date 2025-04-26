import pygame

class HelpScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        
        # Load typewriter font
        try:
            self.title_font = pygame.font.Font('assets/fonts/typewriter.ttf', 48)
            self.text_font = pygame.font.Font('assets/fonts/typewriter.ttf', 28)
            self.button_font = pygame.font.Font('assets/fonts/typewriter.ttf', 36)
            print("Loaded typewriter font for help screen")
        except Exception as e:
            print(f"Error loading typewriter font for help screen: {e}")
            # Fallback to default fonts
            self.title_font = pygame.font.Font(None, 48)
            self.text_font = pygame.font.Font(None, 28)
            self.button_font = pygame.font.Font(None, 36)
            
        # Help text content
        self.title = "EVIDENCE BOARD HELP"
        self.help_sections = [
            {
                "title": "NAVIGATING THE EVIDENCE BOARD",
                "content": [
                    "• Click on any evidence item to examine it in detail",
                    "• Use the mouse wheel or UP/DOWN arrow keys to scroll",
                    "• Press the 'Suspects' button to view suspect profiles",
                    "• Press the 'Interrogations' button (when available) to question suspects",
                    "• Press the 'Submit Arrest Warrant' button when you're ready to make an accusation"
                ]
            },
            {
                "title": "EXAMINING EVIDENCE",
                "content": [
                    "• When viewing evidence, use LEFT/RIGHT arrow keys to navigate between pages",
                    "• Use UP/DOWN arrow keys or mouse wheel to scroll through long documents",
                    "• Click the 'Back' button to return to the evidence board",
                    "• Pay close attention to details - they may be crucial to solving the case!"
                ]
            },
            {
                "title": "INVESTIGATION TIPS",
                "content": [
                    "• You must examine at least 3 pieces of evidence to unlock interrogations",
                    "• New evidence may become available after certain interrogations",
                    "• Compare statements from suspects with the evidence you've found",
                    "• Look for inconsistencies and contradictions",
                    "• It might help to take notes while playing the game",
                    "• If you get stuck, click the lightbulb button on the evidence board",
                    "• Take your time - rushing could lead to false accusations"
                ]
            }
        ]
        
        # Button for returning to evidence board
        self.back_button = {
            "text": "Return to Evidence Board",
            "rect": None,
            "hovered": False
        }
        
        # Scrolling variables
        self.scroll_position = 0
        self.max_scroll = 0  # Will be calculated in draw
        self.scroll_speed = 30
        
    def handle_event(self, event):
        """Handle user input events"""
        # Handle mouse movement for button hover
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            if self.back_button["rect"] and self.back_button["rect"].collidepoint(mouse_pos):
                self.back_button["hovered"] = True
            else:
                self.back_button["hovered"] = False
                
        # Handle button click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            mouse_pos = pygame.mouse.get_pos()
            if self.back_button["rect"] and self.back_button["rect"].collidepoint(mouse_pos):
                # Return to evidence board
                self.game.change_state("evidence_board")
                return True
                
        # Handle scrolling with mouse wheel
        if event.type == pygame.MOUSEWHEEL:
            self.scroll_position += event.y * self.scroll_speed
            # Clamp scroll position
            self.scroll_position = max(min(self.scroll_position, 0), -self.max_scroll)
            return True
                
        # Handle scrolling with keyboard
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.scroll_position += self.scroll_speed
                # Clamp scroll position
                self.scroll_position = min(self.scroll_position, 0)
                return True
            elif event.key == pygame.K_DOWN:
                self.scroll_position -= self.scroll_speed
                # Clamp scroll position
                self.scroll_position = max(self.scroll_position, -self.max_scroll)
                return True
            elif event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                # Return to evidence board
                self.game.change_state("evidence_board")
                return True
                
        return True
        
    def update(self):
        """Update game state"""
        pass
        
    def draw(self):
        """Draw the help screen"""
        # Dark background
        self.screen.fill((20, 20, 20))
        
        # Draw title
        title_surface = self.title_font.render(self.title, True, (255, 255, 255))
        title_rect = title_surface.get_rect(centerx=self.screen.get_width() // 2, top=30)
        self.screen.blit(title_surface, title_rect)
        
        # Calculate dimensions
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        content_width = screen_width - 100  # Margin on both sides
        
        # Calculate total height for scrolling
        total_height = 0
        for section in self.help_sections:
            total_height += 60  # Section title
            total_height += len(section["content"]) * 40  # Section content
            total_height += 30  # Spacing between sections
        
        visible_height = screen_height - 200  # Space for title and button
        self.max_scroll = max(0, total_height - visible_height)
        
        # Create a clipping rect for the text area
        text_area_rect = pygame.Rect(50, 100, content_width, visible_height)
        
        # Store original clip area
        original_clip = self.screen.get_clip()
        
        # Set clip area to text area
        self.screen.set_clip(text_area_rect)
        
        # Draw help sections
        y_position = 100 + self.scroll_position
        
        for section in self.help_sections:
            # Draw section title
            section_title = self.text_font.render(section["title"], True, (200, 200, 0))  # Yellow color
            section_title_rect = section_title.get_rect(left=60, top=y_position)
            
            # Only draw if visible
            if y_position > 70 and y_position < screen_height - 100:
                self.screen.blit(section_title, section_title_rect)
            
            y_position += 50  # Space after title
            
            # Draw section content
            for line in section["content"]:
                line_surface = self.text_font.render(line, True, (200, 200, 200))  # Light gray
                line_rect = line_surface.get_rect(left=80, top=y_position)
                
                # Only draw if visible
                if y_position > 70 and y_position < screen_height - 100:
                    self.screen.blit(line_surface, line_rect)
                
                y_position += 40  # Line spacing
            
            y_position += 30  # Space between sections
        
        # Restore original clip area
        self.screen.set_clip(original_clip)
        
        # Draw scroll indicators if needed
        if self.max_scroll > 0:
            if self.scroll_position < 0:
                # Draw up arrow
                pygame.draw.polygon(self.screen, (150, 150, 150), [
                    (screen_width - 30, 110),
                    (screen_width - 20, 90),
                    (screen_width - 10, 110)
                ])
                
            if self.scroll_position > -self.max_scroll:
                # Draw down arrow
                pygame.draw.polygon(self.screen, (150, 150, 150), [
                    (screen_width - 30, screen_height - 110),
                    (screen_width - 20, screen_height - 90),
                    (screen_width - 10, screen_height - 110)
                ])
        
        # Draw back button
        button_color = (200, 0, 0) if self.back_button["hovered"] else (150, 150, 150)
        button_surface = self.button_font.render(self.back_button["text"], True, button_color)
        button_rect = button_surface.get_rect(centerx=screen_width // 2, bottom=screen_height - 30)
        self.back_button["rect"] = button_rect
        self.screen.blit(button_surface, button_rect)
