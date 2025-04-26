import pygame
import time

class LosingScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        
        # Jumpscare variables
        self.start_time = None
        self.jumpscare_delay = 0.5  # 0.5 second delay before jumpscare starts
        self.jumpscare_started = False
        self.jumpscare_complete = False
        self.current_image_index = 0
        self.image_scale = 0.1  # Starting scale (10% of original size)
        self.scale_speed = 0.03  # How fast the image grows
        
        # Music delay variables
        self.music_delay = 5.0  # 5 seconds after arriving on screen
        self.music_started = False
        
        # Button variables
        self.buttons = [
            {"text": "Learn The Truth??", "action": "explain", "rect": None, "hovered": False},
            {"text": "Return Home....", "action": "menu", "rect": None, "hovered": False}
        ]
        self.selected_button = None
        
        # Load bloody font for buttons
        try:
            self.button_font = pygame.font.Font('assets/fonts/bloody.ttf', 48)
            print("Loaded bloody font for losing screen buttons")
        except Exception as e:
            print(f"Error loading bloody font: {e}")
            self.button_font = pygame.font.Font(None, 48)  # Fallback
        
        # Load jumpscare images
        self.jumpscare_images = []
        try:
            self.jumpscare_images = [
                pygame.image.load(f'assets/images/characters/lisa_scary_{i}.png') for i in range(1, 5)
            ]
            print(f"Loaded {len(self.jumpscare_images)} jumpscare images")
        except Exception as e:
            print(f"Error loading jumpscare images: {e}")
            
        # Load jumpscare sound
        try:
            self.jumpscare_sound = pygame.mixer.Sound('assets/sounds/jumpscare.mp3')
            self.jumpscare_sound.set_volume(1.0)  # Maximum volume
            print("Loaded jumpscare sound")
        except Exception as e:
            print(f"Error loading jumpscare sound: {e}")
            self.jumpscare_sound = None
        
    def enter(self):
        """Called when entering this state"""
        # Reset jumpscare state
        self.start_time = None
        self.jumpscare_started = False
        self.jumpscare_complete = False
        self.current_image_index = 0
        self.image_scale = 0.1
        
        # Stop background music completely
        pygame.mixer.music.stop()  # Stop music entirely
        pygame.mixer.music.set_volume(0.0)  # Ensure volume is 0
        self.music_started = False
        
        # Reset button states
        for button in self.buttons:
            button["hovered"] = False
        
    def handle_event(self, event):
        """Handle user input events"""
        # Block all input during the jumpscare
        if not self.jumpscare_complete:
            return True
            
        # Handle mouse movement for button hover effects
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button["rect"] and button["rect"].collidepoint(mouse_pos):
                    button["hovered"] = True
                else:
                    button["hovered"] = False
                    
        # Handle button clicks
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button["rect"] and button["rect"].collidepoint(mouse_pos):
                    # Stop the jumpscare sound if it's still playing
                    if self.jumpscare_sound:
                        self.jumpscare_sound.stop()
                    
                    # Restore background music
                    pygame.mixer.music.load('assets/sounds/background.mp3')
                    pygame.mixer.music.play(-1)  # Loop indefinitely
                    pygame.mixer.music.set_volume(0.3)  # Back to 30%
                    
                    # Perform the button action
                    if button["action"] == "menu":
                        self.game.change_state("menu")
                    elif button["action"] == "explain":
                        self.game.change_state("explain_screen")
                    return True
                    
        return True
        
    def update(self):
        """Update game state"""
        # Initialize start time if not set
        if self.start_time is None:
            self.start_time = time.time()
            return
            
        # Calculate elapsed time
        current_time = time.time()
        elapsed = current_time - self.start_time
        
        # Check if it's time to start the jumpscare
        if not self.jumpscare_started and elapsed >= self.jumpscare_delay:
            self.jumpscare_started = True
            # Play jumpscare sound
            if self.jumpscare_sound:
                self.jumpscare_sound.play()
            return
            
        # Check if it's time to start the background music (5 seconds after arriving)
        if self.jumpscare_complete and not self.music_started and elapsed >= self.music_delay:
            self.music_started = True
            # Start background music at low volume
            try:
                pygame.mixer.music.load('assets/sounds/background.mp3')  # Correct path to background music
                pygame.mixer.music.play(-1)  # Play on loop
                pygame.mixer.music.set_volume(0.2)  # 20% volume
            except Exception as e:
                print(f"Error reloading background music: {e}")
            
        # If jumpscare hasn't started yet or is complete, do nothing more with jumpscare
        if not self.jumpscare_started or self.jumpscare_complete:
            return
            
        # Update the image scale (make it grow)
        self.image_scale += self.scale_speed
        
        # Check if it's time to switch to the next image
        if self.image_scale >= 0.4 and self.current_image_index < len(self.jumpscare_images) - 1:
            self.current_image_index += 1
            self.image_scale = 0.2  # Reset scale for next image
            
        # Check if the jumpscare is complete (last image fills the screen)
        if self.current_image_index == len(self.jumpscare_images) - 1 and self.image_scale >= 1.5:
            self.jumpscare_complete = True
        
    def draw(self):
        """Draw the losing screen"""
        # Black background
        self.screen.fill((0, 0, 0))
        
        # If jumpscare hasn't started yet, just show black screen
        if not self.jumpscare_started:
            return
            
        # If we have jumpscare images and the jumpscare has started but not complete
        if self.jumpscare_images and not self.jumpscare_complete:
            # Get the current image
            current_image = self.jumpscare_images[self.current_image_index]
            
            # Calculate the scaled size
            original_width = current_image.get_width()
            original_height = current_image.get_height()
            new_width = int(original_width * self.image_scale)
            new_height = int(original_height * self.image_scale)
            
            # Scale the image
            scaled_image = pygame.transform.scale(current_image, (new_width, new_height))
            
            # Center the image on screen
            image_rect = scaled_image.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            
            # Draw the image
            self.screen.blit(scaled_image, image_rect)
        
        # If jumpscare is complete, show the "YOU LOSE" message and buttons
        if self.jumpscare_complete:
            # Draw a simple message
            try:
                title_font = pygame.font.Font('assets/fonts/bloody.ttf', 72)
            except:
                title_font = pygame.font.Font(None, 72)
                
            text = title_font.render("YOU LOSE!", True, (255, 0, 0))
            text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 3))
            self.screen.blit(text, text_rect)
            
            # Draw buttons
            screen_center_x = self.screen.get_width() // 2
            button_y_start = self.screen.get_height() // 2 + 50
            button_spacing = 120  # Increased spacing between buttons
            
            for i, button in enumerate(self.buttons):
                # Set button color based on hover state
                color = (255, 0, 0) if button["hovered"] else (150, 150, 150)
                
                # Render button text
                text_surface = self.button_font.render(button["text"], True, color)
                
                # Position button
                button_y = button_y_start + (i * button_spacing)
                text_rect = text_surface.get_rect(center=(screen_center_x, button_y))
                
                # Store the rect for collision detection
                button["rect"] = text_rect
                
                # Draw the button
                self.screen.blit(text_surface, text_rect)
