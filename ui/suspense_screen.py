import pygame
import time
import random
from dsl.suspense_parser import load_suspense_text, get_default_suspense_text_path

class SuspenseScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        
        # Timer for automatic transition
        self.start_time = None
        self.duration = 33  # 33 seconds of suspense
        self.black_screen_time = 30  # Time when screen goes completely black (seconds)
        
        # Store the player's selection to determine the next screen
        self.player_selection = None
        
        # Load heartbeat sound
        try:
            self.heartbeat_sound = pygame.mixer.Sound('assets/sounds/heartbeat.mp3')
            self.heartbeat_sound.set_volume(0.7)  # 70% volume
        except Exception as e:
            print(f"Error loading heartbeat sound: {e}")
            self.heartbeat_sound = None
            
        # Load custom fonts with different sizes
        self.fonts = {}
        self.load_fonts()
        
        # Default font size
        self.default_font_size = 28
            
        # Load suspense text
        self.suspense_text_path = get_default_suspense_text_path()
        self.suspense_lines = load_suspense_text(self.suspense_text_path)
        
        # Typewriter effect settings
        self.last_char_time = 0
        self.char_delay = 0.05  # Seconds between characters
        self.typewriter_sound = None  # Could add typewriter sound effect later
        
        # Text fade settings
        self.display_time = 2.0  # Seconds to display text before fading
        
        # Strobe effect settings
        self.strobe_intensity = 0.0  # Current strobe intensity (0.0 to 1.0)
        self.strobe_direction = 1  # 1 for increasing, -1 for decreasing
        self.initial_strobe_speed = 0.8  # Initial speed of the strobe effect
        self.strobe_speed = self.initial_strobe_speed  # Current speed (will increase)
        self.max_strobe_speed = 3.0  # Maximum speed the strobe will reach
        self.strobe_acceleration = 0.02  # How quickly the strobe speed increases
        self.strobe_min = 0.0  # Minimum strobe intensity
        self.strobe_max = 0.4  # Maximum strobe intensity (0.4 = 40% brighter)
        
    def enter(self, player_selection=None):
        """Called when entering this state"""
        # Start the timer
        self.start_time = time.time()
        # Store the player's selection
        self.player_selection = player_selection
        
        # Play the heartbeat sound once (not looping)
        if self.heartbeat_sound:
            self.heartbeat_sound.play(0)  # Play once (0 = no loops)
            
        # Reset suspense text state
        for line in self.suspense_lines:
            line['current_text'] = ''
            line['visible'] = False
            line['complete'] = False
            
        # Reset typewriter effect timer
        self.last_char_time = time.time()
        
    def load_fonts(self):
        """Load fonts with different sizes"""
        font_path = 'assets/fonts/typewriter.ttf'
        font_sizes = [24, 28, 32, 36, 42, 48, 54, 60, 72, 80, 96]
        
        # Try to load the custom font
        try:
            for size in font_sizes:
                self.fonts[size] = pygame.font.Font(font_path, size)
        except Exception as e:
            # Fallback to default font
            for size in font_sizes:
                self.fonts[size] = pygame.font.Font(None, size)
    
    def handle_event(self, event):
        """Handle user input events"""
        # Block all input events during suspense screen
        # No way to skip the suspense screen
        return True
        
    def update(self):
        """Update game state"""
        # Check if time is up
        if self.start_time and time.time() - self.start_time >= self.duration:
            self.transition_to_result()
            return
            
        # Calculate elapsed time since suspense screen started
        current_time = time.time()
        elapsed = current_time - self.start_time
        
        # Update which lines should be visible based on their appearance time
        for line in self.suspense_lines:
            if not line['visible'] and elapsed >= line['time']:
                line['visible'] = True
        
        # Update typewriter effect for visible lines
        if current_time - self.last_char_time >= self.char_delay:
            self.last_char_time = current_time
            
            # Process each visible line that's not complete
            for line in self.suspense_lines:
                if line['visible'] and not line['complete']:
                    full_text = line['text']
                    current_text = line['current_text']
                    
                    # Add one more character
                    if len(current_text) < len(full_text):
                        line['current_text'] = full_text[:len(current_text) + 1]
                        
                        # Play typewriter sound if we have one
                        if self.typewriter_sound:
                            self.typewriter_sound.play()
                    else:
                        line['complete'] = True
                        line['complete_time'] = current_time
                        line['fade_start_time'] = current_time + self.display_time
        
        # Update fading for completed lines
        for line in self.suspense_lines:
            if line['complete'] and current_time >= line['fade_start_time']:
                # Calculate fade progress
                fade_elapsed = current_time - line['fade_start_time']
                fade_progress = min(1.0, fade_elapsed / line['fade_duration'])
                
                # Update alpha value (255 to 0)
                line['alpha'] = max(0, int(255 * (1.0 - fade_progress)))
        
        # Calculate how far through the suspense we are (0.0 to 1.0)
        progress = min(1.0, elapsed / self.duration)
        
        # Check if we've reached the black screen phase
        if elapsed >= self.black_screen_time:
            # Set strobe intensity to 0 during black screen phase
            self.strobe_intensity = 0.0
            return
            
        # Gradually increase strobe speed based on progress
        target_speed = self.initial_strobe_speed + (self.max_strobe_speed - self.initial_strobe_speed) * progress
        self.strobe_speed = min(self.max_strobe_speed, self.strobe_speed + self.strobe_acceleration * 0.01)
        
        # Update strobe effect with current speed
        self.strobe_intensity += self.strobe_direction * self.strobe_speed * 0.01
        
        # Reverse direction if reaching limits
        if self.strobe_intensity >= self.strobe_max:
            self.strobe_intensity = self.strobe_max
            self.strobe_direction = -1
        elif self.strobe_intensity <= self.strobe_min:
            self.strobe_intensity = self.strobe_min
            self.strobe_direction = 1
            
    def transition_to_result(self):
        """Transition to the appropriate result screen"""
        # Stop the heartbeat sound
        if self.heartbeat_sound:
            self.heartbeat_sound.stop()
        
        # Get the player selection from the answer screen
        player_selection = self.game.states["answer_screen"].selected_character
        
        # Transition to the appropriate screen
        if player_selection == 'lisa':
            self.game.change_state("winning_screen")
            # Restore background music volume only for winning screen
            pygame.mixer.music.set_volume(0.3)  # Back to 30%
        else:
            # For losing screen, keep music muted - it will handle its own music
            pygame.mixer.music.set_volume(0.0)  # Completely mute
            self.game.change_state("losing_screen")
            
    def draw(self):
        """Draw the suspense screen"""
        # Black background
        self.screen.fill((0, 0, 0))
        
        # Calculate elapsed time
        elapsed = time.time() - self.start_time
        
        # If we've reached the black screen phase, don't draw anything else
        if elapsed >= self.black_screen_time:
            return
            
        # Apply strobe effect by creating a semi-transparent white overlay
        if self.strobe_intensity > 0:
            # Create a white surface with alpha for the strobe effect
            strobe_surface = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
            strobe_surface.fill((255, 255, 255))  # White surface
            strobe_surface.set_alpha(int(self.strobe_intensity * 255))  # Apply intensity as alpha
            self.screen.blit(strobe_surface, (0, 0))  # Draw the strobe effect
        
        # Draw each visible line of suspense text with typewriter effect and fading
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        for line in self.suspense_lines:
            if line['visible'] and line['alpha'] > 0:  # Only draw if visible and not fully faded
                # Get the font for this line's size
                font_size = line['font_size']
                font = self.fonts.get(font_size, self.fonts.get(self.default_font_size))
                
                # Render the text with typewriter effect
                text_surface = font.render(line['current_text'], True, line['color'])
                
                # Apply alpha for fading
                text_surface.set_alpha(line['alpha'])
                
                # Calculate position - use left alignment for typewriter effect
                # First calculate where the center of the full text would be
                full_text_width = font.size(line['text'])[0]
                center_x = line['x_pos'] * screen_width
                center_y = line['y_pos'] * screen_height
                
                # Calculate the left position for the full text if it was centered
                left_pos = center_x - (full_text_width / 2)
                
                # Position the current text at that same left position
                text_rect = text_surface.get_rect(topleft=(left_pos, center_y - font_size/2))
                self.screen.blit(text_surface, text_rect)
