import pygame
import math
import random
import time
import os

class TipsScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        
        # Load background
        self.background = None
        try:
            self.background = pygame.image.load('assets/images/backgrounds/paper.jpg')
            self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        except Exception as e:
            # Fallback to a plain background if image can't be loaded
            self.background = pygame.Surface((self.screen_width, self.screen_height))
            self.background.fill((245, 245, 220))  # Beige color as fallback
        
        # Load handwriting font
        self.fonts = {}
        self.load_fonts()
        
        # Load images
        self.pencil_img = None
        self.scribble1_img = None
        self.scribble2_img = None
        self.load_images()
        
        # Tips content
        self.tip1_text = "...... everyone seems so tired."
        self.tip2_text = "He didn't fall backward, he ______________."
        
        # Tips state
        self.tip1_revealed = False
        self.tip2_revealed = False
        
        # Animation state
        self.animating = False
        self.current_tip = 0  # 0 = none, 1 = tip1, 2 = tip2
        self.animation_start_time = 0
        self.animation_duration = 2.0  # seconds
        self.pencil_pos = [0, 0]
        self.pencil_direction = 1
        self.reveal_progress = 0.0
        
        # Layout positions
        self.title_pos = (self.screen_width // 2, 80)
        self.intro_text_pos = (self.screen_width // 2, 150)
        self.tip1_title_pos = (100, 250)
        self.tip1_question_pos = (150, 290)
        self.tip1_content_pos = (150, 350)
        self.tip1_buttons_pos = (550, 290)  # Moved further right
        self.tip2_title_pos = (100, 450)
        self.tip2_question_pos = (150, 490)
        self.tip2_content_pos = (150, 550)
        self.tip2_buttons_pos = (550, 490)  # Moved further right
        self.back_button_pos = (self.screen_width // 2, self.screen_height - 80)
        
        # Button state
        self.buttons = []
        self.setup_buttons()
        self.hovered_button = None
    
    def load_fonts(self):
        """Load handwriting font in different sizes"""
        self.fonts = {}
        
        try:
            # Try to load the handwriting font in different sizes
            # Check for both .ttf and .otf extensions
            font_path_ttf = os.path.join('assets', 'fonts', 'handwriting.ttf')
            font_path_otf = os.path.join('assets', 'fonts', 'handwriting.otf')
            
            # First try .otf (OpenType)
            if os.path.exists(font_path_otf):
                font_path = font_path_otf
                print(f"Using OpenType font: {font_path_otf}")
            # Then try .ttf (TrueType)
            elif os.path.exists(font_path_ttf):
                font_path = font_path_ttf
                print(f"Using TrueType font: {font_path_ttf}")
            else:
                font_path = None
                print(f"Warning: Handwriting font not found at {font_path_ttf} or {font_path_otf}")
            
            if font_path:
                for size in [24, 32, 48, 64]:
                    self.fonts[size] = pygame.font.Font(font_path, size)
                print("Successfully loaded handwriting font")
            else:
                # Fallback to default font
                for size in [24, 32, 48, 64]:
                    self.fonts[size] = pygame.font.Font(None, size)
        except Exception as e:
            # Fallback to default font
            for size in [24, 32, 48, 64]:
                self.fonts[size] = pygame.font.Font(None, size)
            print(f"Error loading handwriting font: {e}")
        
        # Set common fonts for easy access
        self.title_font = self.fonts.get(48, pygame.font.Font(None, 48))
        self.content_font = self.fonts.get(32, pygame.font.Font(None, 32))
    
    def load_images(self):
        """Load necessary images"""
        # Initialize all image variables to None first
        self.pencil_img = None
        self.scribble1_img = None
        self.scribble2_img = None
        
        try:
            # Load pencil image
            pencil_path = 'assets/images/other/pencil.png'
            if os.path.exists(pencil_path):
                self.pencil_img = pygame.image.load(pencil_path)
                self.pencil_img = pygame.transform.scale(self.pencil_img, (120, 120))  # Increased size
                print(f"Successfully loaded pencil image from {pencil_path}")
            else:
                print(f"Warning: Pencil image not found at {pencil_path}")
            
            # Load scribble images
            scribble1_path = 'assets/images/other/scribble.png'
            if os.path.exists(scribble1_path):
                self.scribble1_img = pygame.image.load(scribble1_path)
                self.scribble1_img = pygame.transform.scale(self.scribble1_img, (400, 60))
                print(f"Successfully loaded scribble1 image from {scribble1_path}")
            else:
                print(f"Warning: Scribble1 image not found at {scribble1_path}")
            
            # Fixed filename from scribble_1.png to scribble_2.png
            scribble2_path = 'assets/images/other/scribble_2.png'
            if os.path.exists(scribble2_path):
                self.scribble2_img = pygame.image.load(scribble2_path)
                self.scribble2_img = pygame.transform.scale(self.scribble2_img, (400, 60))
                print(f"Successfully loaded scribble2 image from {scribble2_path}")
            else:
                print(f"Warning: Scribble2 image not found at {scribble2_path}")
        except Exception as e:
            print(f"Error loading images: {e}")
    
    def setup_buttons(self):
        """Set up the buttons for the tips screen"""
        # Tip 1 buttons
        self.buttons.append({
            "text": "Yes",
            "action": "reveal_tip1",
            "rect": pygame.Rect(self.tip1_buttons_pos[0], self.tip1_buttons_pos[1], 60, 30),
            "hovered": False,
            "enabled": not self.tip1_revealed
        })
        
        self.buttons.append({
            "text": "No",
            "action": "cancel",
            "rect": pygame.Rect(self.tip1_buttons_pos[0] + 80, self.tip1_buttons_pos[1], 60, 30),
            "hovered": False,
            "enabled": True
        })
        
        # Tip 2 buttons
        self.buttons.append({
            "text": "Yes",
            "action": "reveal_tip2",
            "rect": pygame.Rect(self.tip2_buttons_pos[0], self.tip2_buttons_pos[1], 60, 30),
            "hovered": False,
            "enabled": not self.tip2_revealed
        })
        
        self.buttons.append({
            "text": "No",
            "action": "cancel",
            "rect": pygame.Rect(self.tip2_buttons_pos[0] + 80, self.tip2_buttons_pos[1], 60, 30),
            "hovered": False,
            "enabled": True
        })
        
        # Back button
        self.buttons.append({
            "text": "Back to Evidence Board",
            "action": "back",
            "rect": pygame.Rect(self.back_button_pos[0] - 150, self.back_button_pos[1] - 20, 300, 40),
            "hovered": False,
            "enabled": True
        })
    
    def handle_event(self, event):
        """Handle user input events"""
        if self.animating:
            # Don't handle other events during animation
            return False
            
        if event.type == pygame.MOUSEMOTION:
            # Update hover state for buttons
            mouse_pos = pygame.mouse.get_pos()
            self.hovered_button = None
            for button in self.buttons:
                if button["enabled"] and button["rect"].collidepoint(mouse_pos):
                    button["hovered"] = True
                    self.hovered_button = button
                else:
                    button["hovered"] = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button["enabled"] and button["rect"].collidepoint(mouse_pos):
                    self.handle_button_action(button["action"])
                    return True
        
        return False
    
    def handle_button_action(self, action):
        """Handle button actions"""
        if action == "reveal_tip1" and not self.tip1_revealed:
            self.start_reveal_animation(1)
        elif action == "reveal_tip2" and not self.tip2_revealed:
            self.start_reveal_animation(2)
        elif action == "back":
            self.game.change_state("evidence_board")
    
    def start_reveal_animation(self, tip_number):
        """Start the animation to reveal a tip"""
        self.animating = True
        self.current_tip = tip_number
        self.animation_start_time = time.time()
        self.reveal_progress = 0.0
        
        # Set initial pencil position
        if tip_number == 1:
            self.pencil_pos = [self.tip1_content_pos[0], self.tip1_content_pos[1] - 10]  # Moved down
        else:
            self.pencil_pos = [self.tip2_content_pos[0], self.tip2_content_pos[1] - 10]  # Moved down
    
    def update(self):
        """Update the tips screen"""
        if self.animating:
            current_time = time.time()
            elapsed = current_time - self.animation_start_time
            
            # Update reveal progress
            self.reveal_progress = min(1.0, elapsed / self.animation_duration)
            
            # Update pencil position for erasing animation
            self.pencil_direction = -self.pencil_direction if random.random() < 0.1 else self.pencil_direction
            self.pencil_pos[0] += self.pencil_direction * random.uniform(5, 15)
            
            # Keep pencil within bounds of the scribble
            if self.current_tip == 1:
                min_x = self.tip1_content_pos[0] - 20
                max_x = self.tip1_content_pos[0] + 380
            else:
                min_x = self.tip2_content_pos[0] - 20
                max_x = self.tip2_content_pos[0] + 380
                
            self.pencil_pos[0] = max(min_x, min(max_x, self.pencil_pos[0]))
            
            # Add small random vertical movement
            self.pencil_pos[1] += random.uniform(-2, 2)
            
            # Check if animation is complete
            if self.reveal_progress >= 1.0:
                self.animating = False
                if self.current_tip == 1:
                    self.tip1_revealed = True
                    # Disable the Yes button for tip 1
                    for button in self.buttons:
                        if button["action"] == "reveal_tip1":
                            button["enabled"] = False
                else:
                    self.tip2_revealed = True
                    # Disable the Yes button for tip 2
                    for button in self.buttons:
                        if button["action"] == "reveal_tip2":
                            button["enabled"] = False
    
    def draw(self):
        """Draw the tips screen"""
        # Draw background
        self.screen.blit(self.background, (0, 0))
        
        # Draw title
        title_font = self.fonts.get(64, pygame.font.Font(None, 64))
        title_text = title_font.render("Tips", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=self.title_pos)
        self.screen.blit(title_text, title_rect)
        
        # Draw introduction text
        intro_font = self.fonts.get(32, pygame.font.Font(None, 32))
        intro_text = intro_font.render("You can uncover 2 tips, but that's all you get!", True, (0, 0, 0))
        intro_rect = intro_text.get_rect(center=self.intro_text_pos)
        self.screen.blit(intro_text, intro_rect)
        
        # Draw Tip 1 section
        self.draw_tip_section(1)
        
        # Draw Tip 2 section
        self.draw_tip_section(2)
        
        # Draw back button
        self.draw_button(self.buttons[-1])
        
        # Draw pencil animation if active
        if self.animating:
            if self.pencil_img is None:
                print("Warning: Pencil image not loaded, cannot draw animation")
                # End animation if pencil image is missing
                self.finish_animation()
                return
            
            # Rotate the pencil image to be upside down
            rotated_pencil = pygame.transform.rotate(self.pencil_img, 180)
            pencil_rect = rotated_pencil.get_rect(center=(self.pencil_pos[0], self.pencil_pos[1]))
            self.screen.blit(rotated_pencil, pencil_rect)
    
    def draw_tip_section(self, tip_number):
        """Draw a tip section with title, question, and buttons"""
        section_font = self.fonts.get(32, pygame.font.Font(None, 32))
        question_font = self.fonts.get(24, pygame.font.Font(None, 24))
        content_font = self.fonts.get(32, pygame.font.Font(None, 32))
        
        if tip_number == 1:
            # Draw Tip 1 title
            title_text = section_font.render("Tip #1:", True, (0, 0, 0))
            self.screen.blit(title_text, self.tip1_title_pos)
            
            # Draw question
            question_text = question_font.render("Are you sure you want to uncover Tip 1?", True, (0, 0, 0))
            self.screen.blit(question_text, self.tip1_question_pos)
            
            # Draw buttons
            self.draw_button(self.buttons[0])  # Yes button
            self.draw_button(self.buttons[1])  # No button
            
            # Draw tip content (covered or revealed)
            if self.tip1_revealed or (self.animating and self.current_tip == 1):
                # Draw partially or fully revealed tip
                content_text = content_font.render(self.tip1_text, True, (0, 0, 0))
                self.screen.blit(content_text, self.tip1_content_pos)
                
                # Draw scribble with transparency based on reveal progress
                if self.animating and self.current_tip == 1:
                    alpha = int(255 * (1 - self.reveal_progress))
                    if self.scribble1_img is not None:
                        self.scribble1_img.set_alpha(alpha)
                        self.screen.blit(self.scribble1_img, (self.tip1_content_pos[0] - 10, self.tip1_content_pos[1] - 10))
                    else:
                        # Fallback if image not loaded - draw a black rectangle
                        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.tip1_content_pos[0] - 10, self.tip1_content_pos[1] - 10, 400, 60))
            else:
                # Draw fully covered tip
                if self.scribble1_img is not None:
                    self.screen.blit(self.scribble1_img, (self.tip1_content_pos[0] - 10, self.tip1_content_pos[1] - 10))
                else:
                    # Fallback if image not loaded - draw a black rectangle
                    pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.tip1_content_pos[0] - 10, self.tip1_content_pos[1] - 10, 400, 60))
        else:
            # Draw Tip 2 title
            title_text = section_font.render("Tip #2:", True, (0, 0, 0))
            self.screen.blit(title_text, self.tip2_title_pos)
            
            # Draw question
            question_text = question_font.render("Are you sure you want to uncover Tip 2?", True, (0, 0, 0))
            self.screen.blit(question_text, self.tip2_question_pos)
            
            # Draw buttons
            self.draw_button(self.buttons[2])  # Yes button
            self.draw_button(self.buttons[3])  # No button
            
            # Draw tip content (covered or revealed)
            if self.tip2_revealed or (self.animating and self.current_tip == 2):
                # Draw partially or fully revealed tip
                content_text = content_font.render(self.tip2_text, True, (0, 0, 0))
                self.screen.blit(content_text, self.tip2_content_pos)
                
                # Draw scribble with transparency based on reveal progress
                if self.animating and self.current_tip == 2:
                    alpha = int(255 * (1 - self.reveal_progress))
                    if self.scribble2_img is not None:
                        self.scribble2_img.set_alpha(alpha)
                        self.screen.blit(self.scribble2_img, (self.tip2_content_pos[0] - 10, self.tip2_content_pos[1] - 10))
                    else:
                        # Fallback if image not loaded - draw a black rectangle
                        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.tip2_content_pos[0] - 10, self.tip2_content_pos[1] - 10, 400, 60))
            else:
                # Draw fully covered tip
                if self.scribble2_img is not None:
                    self.screen.blit(self.scribble2_img, (self.tip2_content_pos[0] - 10, self.tip2_content_pos[1] - 10))
                else:
                    # Fallback if image not loaded - draw a black rectangle
                    pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.tip2_content_pos[0] - 10, self.tip2_content_pos[1] - 10, 400, 60))
    
    def draw_button(self, button):
        """Draw a button with hover effect"""
        button_font = self.fonts.get(24, pygame.font.Font(None, 24))
        text_color = (0, 0, 0)
        
        # Render button text
        text_surface = button_font.render(button["text"], True, text_color)
        text_rect = text_surface.get_rect(center=button["rect"].center)
        
        # Draw the text
        self.screen.blit(text_surface, text_rect)
        
        # Draw hand-drawn circle if hovered
        if button["hovered"]:
            self.draw_hand_circle(button["rect"].center, max(button["rect"].width, button["rect"].height) // 2 + 5)
    
    def draw_hand_circle(self, center, radius):
        """Draw a hand-drawn circle around a button"""
        num_points = 36
        prev_point = None
        
        for i in range(num_points + 1):
            # Add some randomness to make it look hand-drawn
            angle = 2 * math.pi * i / num_points
            r = radius + random.uniform(-2, 2)
            x = center[0] + r * math.cos(angle)
            y = center[1] + r * math.sin(angle)
            
            if prev_point:
                # Draw slightly wavy line between points
                pygame.draw.line(self.screen, (0, 0, 0), prev_point, (x, y), 2)
            
            prev_point = (x, y)
