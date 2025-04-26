import pygame

class IntroSequence:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.text_lines = []
        self.current_line = 0
        self.line_timer = 0
        self.line_delay = 1.5  # seconds between lines
        self.font = pygame.font.SysFont('Arial', 48)
        self.continue_font = pygame.font.SysFont('Arial', 36)
        self.continue_text = "Click Mouse or Press Space To Continue"
        self.continue_alpha = 255  # Start fully visible
        self.finished = False
        self.waiting_for_input = True  # Start waiting for input
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
            if self.waiting_for_input:
                self.waiting_for_input = False
            elif self.finished:
                self.game.load_scene("intro")
                self.game.change_state("intro")
            else:
                # Skip animation if not finished
                self.current_line = len(self.text_lines)
                self.finished = True
                
    def update(self):
        if not self.waiting_for_input and not self.finished:
            # Update line timer
            self.line_timer += 1/60  # Assuming 60 FPS
            
            # Show next line if enough time has passed
            if self.line_timer >= self.line_delay and self.current_line < len(self.text_lines):
                self.current_line += 1
                self.line_timer = 0
                
            # Check if all lines are shown
            if self.current_line >= len(self.text_lines):
                self.finished = True
                
    def draw(self):
        # Fill screen with black
        self.screen.fill((0, 0, 0))
        
        # Draw continue text (always visible)
        continue_surface = self.continue_font.render(self.continue_text, True, (255, 255, 255))
        continue_rect = continue_surface.get_rect(centerx=self.screen.get_rect().centerx,
                                                bottom=self.screen.get_rect().bottom - 50)
        self.screen.blit(continue_surface, continue_rect)
        
        # Only draw lines if we're not waiting for input
        if not self.waiting_for_input:
            # Draw each line that should be visible
            for i in range(self.current_line):
                text = self.font.render(self.text_lines[i], True, (255, 255, 255))
                text_rect = text.get_rect(centerx=self.screen.get_rect().centerx,
                                        centery=self.screen.get_rect().centery - 50 + (i * 60))
                self.screen.blit(text, text_rect) 