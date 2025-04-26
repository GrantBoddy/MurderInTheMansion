import pygame
import random
import math

class Confetti:
    """Confetti particle system for celebration effects"""
    
    def __init__(self, screen_width, screen_height):
        """Initialize the confetti system"""
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.particles = []
        self.colors = [
            (255, 0, 0),     # Red
            (0, 255, 0),     # Green
            (0, 0, 255),     # Blue
            (255, 255, 0),   # Yellow
            (255, 0, 255),   # Magenta
            (0, 255, 255),   # Cyan
            (255, 165, 0),   # Orange
            (128, 0, 128),   # Purple
            (255, 192, 203), # Pink
            (255, 215, 0)    # Gold
        ]
        
        # Start with no particles - they'll be generated when needed
        # We'll generate them when update is first called
    
    def generate_particles(self, count):
        """Generate a batch of confetti particles"""
        for _ in range(count):
            # Random position at the top of the screen
            x = random.randint(0, self.screen_width)
            y = random.randint(-50, 0)
            
            # Random size between 5 and 15 pixels
            size = random.randint(5, 15)
            
            # Random color from our palette
            color = random.choice(self.colors)
            
            # Random horizontal and vertical speed
            speed_x = random.uniform(-1, 1)
            speed_y = random.uniform(2, 5)
            
            # Random rotation and rotation speed
            rotation = random.uniform(0, 360)
            rotation_speed = random.uniform(-5, 5)
            
            # Create particle
            particle = {
                'x': x,
                'y': y,
                'size': size,
                'color': color,
                'speed_x': speed_x,
                'speed_y': speed_y,
                'rotation': rotation,
                'rotation_speed': rotation_speed,
                'alpha': 255,  # Full opacity
                'fade_speed': random.uniform(0.5, 1.5)
            }
            
            self.particles.append(particle)
    
    def update(self):
        """Update all confetti particles"""
        # If we have no particles, generate an initial batch
        if len(self.particles) == 0:
            self.generate_particles(100)
        
        # Add new particles continuously
        if random.random() < 0.2 and len(self.particles) < 300:  # Increased chance and max particles
            self.generate_particles(10)  # Generate more particles at once
        
        # Update existing particles
        particles_to_remove = []
        for i, particle in enumerate(self.particles):
            # Apply gravity and wind
            particle['speed_y'] += 0.1  # Increased gravity
            particle['speed_x'] += random.uniform(-0.05, 0.05)  # Random wind effect
            
            # Update position
            particle['x'] += particle['speed_x']
            particle['y'] += particle['speed_y']
            
            # Update rotation
            particle['rotation'] += particle['rotation_speed']
            
            # Fade out particles gradually
            particle['alpha'] -= particle['fade_speed']
            
            # Mark particles for removal if they're off-screen or fully transparent
            if (particle['y'] > self.screen_height + 50 or 
                particle['x'] < -50 or 
                particle['x'] > self.screen_width + 50 or
                particle['alpha'] <= 0):
                particles_to_remove.append(i)
        
        # Remove particles (in reverse order to avoid index issues)
        for i in sorted(particles_to_remove, reverse=True):
            if i < len(self.particles):  # Safety check
                self.particles.pop(i)
    
    def draw(self, screen):
        """Draw all confetti particles"""
        for particle in self.particles:
            # Create a surface for this particle with alpha channel
            particle_surface = pygame.Surface((particle['size'], particle['size']), pygame.SRCALPHA)
            
            # Set the alpha value for transparency
            alpha = max(0, min(255, int(particle['alpha'])))
            
            # Draw the particle (a small rectangle with rotation)
            color_with_alpha = (*particle['color'], alpha)
            pygame.draw.rect(particle_surface, color_with_alpha, (0, 0, particle['size'], particle['size']))
            
            # Rotate the particle
            rotated_surface = pygame.transform.rotate(particle_surface, particle['rotation'])
            
            # Get the rect for the rotated surface
            rect = rotated_surface.get_rect(center=(particle['x'], particle['y']))
            
            # Draw the rotated particle
            screen.blit(rotated_surface, rect)
