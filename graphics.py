import pygame

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 740
SCREEN_HEIGHT = 650
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
FONT = pygame.font.Font(None, 28)  # Default font

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def draw_image(image_path, position=None, center=False):
    """ Loads and draws an image onto the screen, optionally centering it. """
    image = pygame.image.load(image_path)
    if center:
        position = ((SCREEN_WIDTH - image.get_width()) // 2, (SCREEN_HEIGHT - image.get_height()) // 2)
    elif position is None:
        position = (0, 0)

    screen.blit(image, position)

"""
def draw_image(image_path, position=(0, 0)):
    Loads and draws an image onto the screen. 
    image = pygame.image.load(image_path)
    screen.blit(image, position)
"""

def draw_text(text, position, color=(255, 255, 255)):
    """ Renders and displays text on screen. """
    text_surface = FONT.render(text, True, color)
    screen.blit(text_surface, position)

def update_display():
    """ Updates the screen after drawing. """
    pygame.display.flip()
