import pygame
import os

class InterrogationScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        
        # Load background
        self.background = None
        self.load_background()
        
        # Load typewriter font
        try:
            font_path = os.path.join('assets', 'fonts', 'typewriter.ttf')
            self.dialogue_font = pygame.font.Font(font_path, 28)  # Slightly smaller than default 32
            self.instruction_font = pygame.font.Font(font_path, 22)  # Slightly smaller than default 24
        except Exception as e:
            print(f"Error loading typewriter font: {e}")
            # Fallback to default font
            self.dialogue_font = pygame.font.Font(None, 32)
            self.instruction_font = pygame.font.Font(None, 24)
            
        # Character name colors
        self.detective_color = (0, 100, 255)  # Blue for detective
        self.character_color = (200, 0, 0)    # Red for other characters
        
        # Dialogue data
        self.dialogue_lines = []
        self.current_line_index = 0
        self.current_interrogation_id = None
        self.show_instructions = True
        
        # Text box dimensions - larger and at the bottom of the screen
        self.text_box_rect = pygame.Rect(
            50, 
            self.screen.get_height() - 250, 
            self.screen.get_width() - 100, 
            220
        )
        
    def load_background(self):
        """Load the interrogation room background"""
        try:
            bg_path = 'assets/images/backgrounds/interrogation_room.png'
            self.background = pygame.image.load(bg_path).convert()
            # Scale to screen size
            self.background = pygame.transform.scale(self.background, 
                                                  (self.screen.get_width(), self.screen.get_height()))
        except Exception as e:
            print(f"Error loading interrogation room background: {e}")
            self.background = None
    
    def load_interrogation(self, interrogation_id):
        """Load the dialogue for a specific interrogation"""
        self.current_interrogation_id = interrogation_id
        self.current_line_index = 0
        self.show_instructions = True
        self.dialogue_lines = []
        
        # Try to load the dialogue from a text file
        try:
            file_path = f"assets/interrogations/{interrogation_id}.txt"
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                
                for line in lines:
                    line = line.strip()
                    if not line:  # Skip empty lines
                        continue
                        
                    # Split the line at the first colon
                    parts = line.split(':', 1)
                    if len(parts) >= 2:
                        speaker = parts[0].strip()
                        text = parts[1].strip()
                        self.dialogue_lines.append({"speaker": speaker, "text": text})
                    else:
                        # If no colon found, treat the whole line as text with no speaker
                        self.dialogue_lines.append({"speaker": "", "text": line})
                        
            print(f"Loaded {len(self.dialogue_lines)} lines of dialogue from {file_path}")
            
        except Exception as e:
            print(f"Error loading interrogation {interrogation_id}: {e}")
            # Fallback to a default message if file can't be loaded
            self.dialogue_lines = [
                {"speaker": "DETECTIVE", "text": f"There was an error loading the interrogation file for {interrogation_id}."},
                {"speaker": "DETECTIVE", "text": f"Error: {e}"}
            ]
    
    def handle_event(self, event):
        """Handle user input events"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 or \
           (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
            
            # If showing instructions, hide them and start dialogue
            if self.show_instructions:
                self.show_instructions = False
                return
                
            # Advance to next line of dialogue
            self.current_line_index += 1
            
            # If we've reached the end of the dialogue, return to interrogation menu
            if self.current_line_index >= len(self.dialogue_lines):
                # Check if we just completed Mary's interrogation
                if self.current_interrogation_id == "mary_interrogation":
                    # Make new evidence available
                    self.unlock_new_evidence_after_mary()
                    
                # Check if we just completed Emily's interrogation
                elif self.current_interrogation_id == "emily_interrogation":
                    # Make ballistics report available
                    self.unlock_ballistics_report()
                    
                # Return to interrogation menu
                self.game.change_state("interrogation_menu")
    
    def update(self):
        """Update interrogation screen state"""
        pass
    
    def draw(self):
        """Draw the interrogation screen"""
        # Draw background
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            # Fallback to plain background
            self.screen.fill((30, 30, 30))
        
        # If showing instructions, display them
        if self.show_instructions:
            instruction_text = "Click Mouse or Press Space To Continue Through Interrogation"
            instruction_surface = self.instruction_font.render(instruction_text, True, (255, 255, 255))
            instruction_rect = instruction_surface.get_rect(
                centerx=self.screen.get_width() // 2,
                bottom=self.screen.get_height() - 270  # Position above the text box
            )
            self.screen.blit(instruction_surface, instruction_rect)
            return
        
        # If we have dialogue to display
        if self.current_line_index < len(self.dialogue_lines):
            current_line = self.dialogue_lines[self.current_line_index]
            
            # Draw text box background
            pygame.draw.rect(self.screen, (0, 0, 0), self.text_box_rect)
            pygame.draw.rect(self.screen, (200, 200, 200), self.text_box_rect, 2)  # Border
            
            # Draw speaker name with appropriate color
            speaker_text = current_line["speaker"] + ":"
            
            # Determine text color based on speaker
            if current_line["speaker"].upper() == "DETECTIVE":
                text_color = self.detective_color  # Blue for detective
            else:
                text_color = self.character_color  # Red for other characters
                
            speaker_surface = self.dialogue_font.render(speaker_text, True, text_color)
            self.screen.blit(speaker_surface, (self.text_box_rect.x + 10, self.text_box_rect.y + 10))
            
            # Draw dialogue text (with word wrapping)
            dialogue_text = current_line["text"]
            self.draw_wrapped_text(dialogue_text, self.text_box_rect.x + 20, self.text_box_rect.y + 50)
    
    def unlock_new_evidence_after_mary(self):
        """Make new evidence available after Mary's interrogation"""
        evidence_board = self.game.states["evidence_board"]
        
        # Make the new evidence items available
        for evidence in evidence_board.post_mary_evidence:
            evidence['available'] = True
        
        # Show alert when returning to evidence board
        evidence_board.show_new_evidence_alert = True
        evidence_board.new_evidence_alert_timer = 300  # Show for 5 seconds
        
    def unlock_ballistics_report(self):
        """Make ballistics report available after Emily's interrogation"""
        evidence_board = self.game.states["evidence_board"]
        
        # Make the ballistics report available
        for evidence in evidence_board.post_emily_evidence:
            evidence['available'] = True
        
        # Show alert when returning to evidence board
        evidence_board.show_new_evidence_alert = True
        evidence_board.new_evidence_alert_timer = 300  # Show for 5 seconds
    
    def draw_wrapped_text(self, text, x, y):
        """Draw text with word wrapping"""
        words = text.split(' ')
        max_width = self.text_box_rect.width - 40
        line = ""
        y_offset = 0
        
        for word in words:
            test_line = line + word + " "
            test_width = self.dialogue_font.size(test_line)[0]
            
            if test_width > max_width:
                text_surface = self.dialogue_font.render(line, True, (255, 255, 255))
                self.screen.blit(text_surface, (x, y + y_offset))
                line = word + " "
                y_offset += self.dialogue_font.get_linesize()
            else:
                line = test_line
        
        # Draw the last line
        if line:
            text_surface = self.dialogue_font.render(line, True, (255, 255, 255))
            self.screen.blit(text_surface, (x, y + y_offset))
