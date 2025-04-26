import pygame
import os

# Initialize Pygame
pygame.init()

# Colors
BLACK = (0, 0, 0)
DARK_GRAY = (40, 40, 40)
GRAY = (80, 80, 80)
RED = (200, 0, 0)
WHITE = (255, 255, 255)

def create_character_placeholder(name, size=(200, 300)):
    """Create a placeholder image for a character"""
    surface = pygame.Surface(size)
    surface.fill(DARK_GRAY)
    
    # Draw character silhouette
    pygame.draw.rect(surface, GRAY, (50, 50, 100, 200))
    pygame.draw.circle(surface, GRAY, (100, 50), 30)
    
    # Draw name
    font = pygame.font.Font(None, 24)
    text = font.render(name, True, WHITE)
    text_rect = text.get_rect(centerx=size[0]//2, bottom=size[1]-10)
    surface.blit(text, text_rect)
    
    return surface

def create_evidence_placeholder(name, size=(300, 200)):
    """Create a placeholder image for evidence"""
    surface = pygame.Surface(size)
    surface.fill(DARK_GRAY)
    
    # Draw evidence frame
    pygame.draw.rect(surface, GRAY, (20, 20, size[0]-40, size[1]-40), 2)
    
    # Draw name
    font = pygame.font.Font(None, 24)
    text = font.render(name, True, WHITE)
    text_rect = text.get_rect(centerx=size[0]//2, centery=size[1]//2)
    surface.blit(text, text_rect)
    
    return surface

def create_background_placeholder(name, size=(1280, 720)):
    """Create a placeholder image for a background"""
    surface = pygame.Surface(size)
    surface.fill(BLACK)
    
    # Draw grid pattern
    for x in range(0, size[0], 50):
        pygame.draw.line(surface, DARK_GRAY, (x, 0), (x, size[1]))
    for y in range(0, size[1], 50):
        pygame.draw.line(surface, DARK_GRAY, (0, y), (size[0], y))
    
    # Draw name
    font = pygame.font.Font(None, 48)
    text = font.render(name, True, WHITE)
    text_rect = text.get_rect(centerx=size[0]//2, centery=size[1]//2)
    surface.blit(text, text_rect)
    
    return surface

def save_image(surface, path):
    """Save a surface as a PNG image"""
    pygame.image.save(surface, path)

def main():
    # Create directories if they don't exist
    os.makedirs("assets/images/characters", exist_ok=True)
    os.makedirs("assets/images/evidence", exist_ok=True)
    os.makedirs("assets/images/backgrounds", exist_ok=True)
    
    # Create character placeholders
    characters = [
        "detective_graves",
        "suspect_mary"
    ]
    for char in characters:
        img = create_character_placeholder(char)
        save_image(img, f"assets/images/characters/{char}.png")
    
    # Create evidence placeholders
    evidence = [
        "crime_scene_photo",
        "phone_records",
        "old_receipt"
    ]
    for ev in evidence:
        img = create_evidence_placeholder(ev)
        save_image(img, f"assets/images/evidence/{ev}.png")
    
    # Create background placeholders
    backgrounds = [
        "crime_scene",
        "police_station",
        "grave_site"
    ]
    for bg in backgrounds:
        img = create_background_placeholder(bg)
        save_image(img, f"assets/images/backgrounds/{bg}.png")
    
    print("Placeholder images created successfully!")

if __name__ == "__main__":
    main() 