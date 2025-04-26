import pygame

class Menu:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        
        # Button configuration with rectangles for mouse interaction
        self.buttons = [
            {"text": "Start Game", "action": "start", "rect": None, "hovered": False},
            {"text": "Credits", "action": "credits", "rect": None, "hovered": False},
            {"text": "Quit", "action": "quit", "rect": None, "hovered": False}
        ]
        self.selected_button = 0
        
        # Load custom fonts
        try:
            self.title_font = pygame.font.Font('assets/fonts/bloody.ttf', 80)  # Larger bloody font for title
            self.button_font = pygame.font.Font('assets/fonts/typewriter.ttf', 48)  # Typewriter font for buttons
            self.instruction_font = pygame.font.Font('assets/fonts/typewriter.ttf', 24)  # Smaller font for instructions
        except Exception as e:
            # Fallback to default fonts
            self.title_font = pygame.font.Font(None, 80)
            self.button_font = pygame.font.Font(None, 48)
            self.instruction_font = pygame.font.Font(None, 24)
            
        # Load portrait image
        try:
            self.portrait = pygame.image.load('assets/images/characters/portrait.png')
        except Exception as e:
            self.portrait = None
        
    def handle_event(self, event):
        # Handle keyboard navigation
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_button = (self.selected_button - 1) % len(self.buttons)
                # Reset hover states when using keyboard
                for button in self.buttons:
                    button["hovered"] = False
            elif event.key == pygame.K_DOWN:
                self.selected_button = (self.selected_button + 1) % len(self.buttons)
                # Reset hover states when using keyboard
                for button in self.buttons:
                    button["hovered"] = False
            elif event.key == pygame.K_RETURN:
                self.handle_button_action(self.buttons[self.selected_button]["action"])
                
        # Handle mouse movement for hover effects
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            for i, button in enumerate(self.buttons):
                if button["rect"] and button["rect"].collidepoint(mouse_pos):
                    button["hovered"] = True
                    # Update selected button to match hovered button
                    self.selected_button = i
                else:
                    button["hovered"] = False
                    
        # Handle mouse clicks
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button["rect"] and button["rect"].collidepoint(mouse_pos):
                    self.handle_button_action(button["action"])
                
    def handle_button_action(self, action):
        if action == "start":
            # Transition to the intro screen
            self.game.change_state("intro")
        elif action == "credits":
            # Show the credits screen
            self.game.change_state("credits_screen")
        elif action == "quit":
            # Quit the game
            pygame.quit()
            exit()
            
    def update(self):
        pass
        
    def draw(self):
        # Draw background
        self.screen.fill((20, 20, 20))
        
        # Calculate layout dimensions
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        # Draw portrait FIRST (so it's behind everything else)
        if self.portrait:
            # Scale portrait to be much larger (85% of screen height)
            portrait_height = int(screen_height * 0.85)  # 85% of screen height
            portrait_width = int(self.portrait.get_width() * (portrait_height / self.portrait.get_height()))
            
            # Use smoothscale for better quality scaling with antialiasing
            try:
                # Try to use the highest quality scaling method available
                scaled_portrait = pygame.transform.smoothscale_by_area(self.portrait, (portrait_width, portrait_height))
            except AttributeError:
                # Fall back to regular smoothscale if the advanced method isn't available
                scaled_portrait = pygame.transform.smoothscale(self.portrait, (portrait_width, portrait_height))
            
            # Position portrait on the left side of the screen and moved down more
            portrait_x = int(screen_width * 0.3) - (portrait_width // 2)  # Center at 30% of screen width
            portrait_y = int(screen_height * 0.6) - (portrait_height // 2)  # Moved down more (60% instead of 55%)
            self.screen.blit(scaled_portrait, (portrait_x, portrait_y))
        
        # Draw title with bloody font at the top center (AFTER portrait so it appears on top)
        title = self.title_font.render("Murder in the Mansion", True, (200, 0, 0))
        title_rect = title.get_rect(centerx=self.screen.get_rect().centerx, top=30)  # Moved up from 50 to 30
        self.screen.blit(title, title_rect)
        
        # Draw buttons with typewriter font on the right side
        button_x = int(screen_width * 0.75)  # Center buttons at 75% of screen width (moved more to the left)
        button_y_start = int(screen_height * 0.35)  # Start buttons at 35% of screen height (moved up from 45%)
        button_spacing = 90  # Increased space between buttons even more
        
        # Larger font size for buttons
        try:
            larger_button_font = pygame.font.Font('assets/fonts/typewriter.ttf', 60)  # Increased from 48 to 60
        except Exception:
            larger_button_font = self.button_font  # Fallback to original font if loading fails
        
        for i, button in enumerate(self.buttons):
            # Determine button color based on selection/hover state
            color = (200, 0, 0) if i == self.selected_button or button["hovered"] else (150, 150, 150)
            
            # Render button text with larger font
            text = larger_button_font.render(button["text"], True, color)
            
            # Position button on the right side
            button_y = button_y_start + (i * button_spacing)
            text_rect = text.get_rect(centerx=button_x, centery=button_y)
            
            # Store the rect for collision detection
            button["rect"] = text_rect
            
            # Draw the button
            self.screen.blit(text, text_rect)
            
        # Draw instructions aligned with buttons on the right
        instructions = [
            "Press Up/Down Keys To Move - Press Enter To Select",
            "Or Use Mouse & Click Buttons"
        ]
        
        # Use the same x-position as the buttons for alignment
        instruction_x = button_x
        instruction_y_start = button_y_start + (len(self.buttons) * button_spacing) + 20  # Reduced space from 50 to 20
        
        for i, instruction in enumerate(instructions):
            text = self.instruction_font.render(instruction, True, (150, 150, 150))
            text_rect = text.get_rect(centerx=instruction_x, top=instruction_y_start + (i * 30))
            self.screen.blit(text, text_rect)
            
        # Add creator credit with bloody font in red
        try:
            credit_font = pygame.font.Font('assets/fonts/bloody.ttf', 32)  # Smaller size for credit
        except Exception:
            credit_font = pygame.font.Font(None, 32)  # Fallback
            
        credit_text = credit_font.render("Made By: Grant Boddy", True, (200, 0, 0))  # Red color
        credit_y = instruction_y_start + (len(instructions) * 30) + 20  # Reduced space from 40 to 20
        credit_rect = credit_text.get_rect(centerx=instruction_x, top=credit_y)
        self.screen.blit(credit_text, credit_rect)