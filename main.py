import pygame
import sys
import os
import io
import re
import traceback

# Set the working directory to the executable's location when running as a frozen executable
if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))
    print(f"Running from executable in: {os.getcwd()}")

# Make sure assets directory exists
assets_dir = os.path.join(os.getcwd(), 'assets')
if not os.path.exists(assets_dir):
    print(f"Warning: Assets directory not found at {assets_dir}")
    print(f"Current directory contents: {os.listdir(os.getcwd())}")

# Hide pygame welcome message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"

# Import game after setting up environment
from game import Game

# Create a custom filter for stderr to suppress libpng warnings
class PngWarningFilter(io.TextIOBase):
    def __init__(self, original_stderr):
        self.original_stderr = original_stderr
        self.png_warning_pattern = re.compile(r'libpng warning: iCCP')
        
    def write(self, text):
        # Only write to stderr if it's not a libpng warning
        if not self.png_warning_pattern.search(text):
            # Check if original_stderr is None (can happen when frozen)
            if self.original_stderr is not None:
                return self.original_stderr.write(text)
        return len(text)  # Pretend we wrote the text
    
    def flush(self):
        # Check if original_stderr is None (can happen when frozen)
        if self.original_stderr is not None:
            return self.original_stderr.flush()
        return None

# Only apply our custom filter if stderr exists (when not frozen)
if sys.stderr is not None:
    sys.stderr = PngWarningFilter(sys.stderr)

# Initialize pygame
pygame.init()
pygame.mixer.init()  # Initialize the mixer for audio

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Colors
BLACK = (0, 0, 0)
DARK_GRAY = (40, 40, 40)
GRAY = (80, 80, 80)
RED = (200, 0, 0)
WHITE = (255, 255, 255)

# Global variable to track if we've already loaded the background music
background_music_loaded = False

# Function to ensure background music is playing without restarting it
def ensure_background_music():
    global background_music_loaded
    try:
        # Only load and start the music if it's not already loaded
        if not background_music_loaded:
            pygame.mixer.music.load('assets/sounds/background.mp3')
            pygame.mixer.music.set_volume(0.3)  # Set volume to 30%
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely
            background_music_loaded = True
            print("Started background music")
        # If music is loaded but not playing, unpause it
        elif not pygame.mixer.music.get_busy():
            pygame.mixer.music.unpause()
            print("Unpaused background music")
    except Exception as e:
        print(f"Error with background music: {e}")

def main():
    # Create a window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Murder Mystery")
    
    # Create a clock to control frame rate
    clock = pygame.time.Clock()
    
    # Load click sound
    click_sound = None
    try:
        click_sound_path = 'assets/sounds/click.mp3'  # Changed from .wav to .mp3
        if os.path.exists(click_sound_path):
            click_sound = pygame.mixer.Sound(click_sound_path)
            click_sound.set_volume(0.4)  # Set volume to 40%
            print("Click sound loaded successfully")
        else:
            print(f"Click sound file not found at {click_sound_path}")
    except Exception as e:
        print(f"Error loading click sound: {e}")
    
    # Create game instance with error handling
    try:
        print("Creating Game instance...")
        game = Game(screen, click_sound)
        print("Game instance created successfully")
    except Exception as e:
        print(f"Error creating game instance: {e}")
        traceback.print_exc()
        pygame.quit()
        sys.exit(1)
    
    # Print welcome message
    print("Enjoy The Game!")
    
    # Start background music immediately
    try:
        ensure_background_music()
    except Exception as e:
        print(f"Error starting background music: {e}")

    # Variables for music check timing
    last_music_check_time = pygame.time.get_ticks()
    music_check_interval = 5000  # Check every 5 seconds (in milliseconds)
    
    # Main game loop
    running = True
    while running:
        current_time = pygame.time.get_ticks()
        
        # Periodically check if music is playing
        if current_time - last_music_check_time > music_check_interval:
            ensure_background_music()
            last_music_check_time = current_time
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_event(event)

        # Update game state
        game.update()

        # Draw everything
        screen.fill(BLACK)
        game.draw()
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Safe error handling that works even when stdout/stderr are None
        error_msg = f"Fatal error: {str(e)}"
        
        # Try to print to console, but don't crash if it fails
        try:
            print(error_msg)
            traceback.print_exc()
        except:
            pass
            
        # Show an error message box that will work in the executable
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            messagebox.showerror("Murder Mystery Error", 
                               f"The game encountered an error and needs to close.\n\nError: {str(e)}")
            root.destroy()
        except:
            # If tkinter fails, at least try to keep console open
            if getattr(sys, 'frozen', False):
                try:
                    input("\nPress Enter to exit...")
                except:
                    pass
                    
        # Clean exit
        try:
            pygame.quit()
        except:
            pass
            
        sys.exit(1)
