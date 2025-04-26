import pygame
from ui.menu import Menu
from ui.evidence_board import EvidenceBoard
from ui.dialogue_box import DialogueBox
from ui.scene_transition import SceneTransition
from ui.intro_screen import IntroScreen
from ui.welcome_screen import WelcomeScreen
from ui.interrogation_menu import InterrogationMenu
from ui.interrogation_screen import InterrogationScreen
from ui.answer_screen import AnswerScreen
from ui.suspense_screen import SuspenseScreen
from ui.winning_screen import WinningScreen
from ui.losing_screen import LosingScreen
from ui.explain_screen import ExplainScreen
from ui.help_screen import HelpScreen
from ui.credits_screen import CreditsScreen
from ui.tips_screen import TipsScreen
from dsl.parser import load_scene, load_character

class Game:
    def __init__(self, screen, click_sound=None):
        self.screen = screen
        self.click_sound = click_sound  # Store the click sound
        self.current_state = "menu"  # Initial state
        self.states = {
            "menu": Menu(self),
            "intro": IntroScreen(self),
            "welcome_screen": WelcomeScreen(self),
            "evidence_board": EvidenceBoard(self),
            "dialogue": DialogueBox(self),
            "interrogation_menu": InterrogationMenu(self),
            "interrogation_screen": InterrogationScreen(self),
            "answer_screen": AnswerScreen(self),
            "suspense_screen": SuspenseScreen(self),
            "winning_screen": WinningScreen(self),
            "losing_screen": LosingScreen(self),
            "explain_screen": ExplainScreen(self),
            "help_screen": HelpScreen(self),
            "credits_screen": CreditsScreen(self),
            "tips_screen": TipsScreen(self)
        }
        
        # Initialize scene transition
        self.transition = SceneTransition(self)
        
        # Game data
        self.evidence = []
        self.characters = []  # Initialize characters list
        
        # Initialize game state
        self.current_scene = None
        
    def handle_event(self, event):
        """Handle pygame events based on current state"""
        # Play click sound for mouse clicks (except scroll wheel) or key presses (space, enter, and arrow keys)
        # But don't play on suspense screen or during transitions
        if self.click_sound and self.current_state != "suspense_screen" and not self.transition.transitioning:
            # For mouse clicks, only play for left/right clicks (buttons 1, 3), not scroll wheel (buttons 4, 5)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button in [1, 3]:
                self.click_sound.play()
            # For key presses, play for space, enter, and arrow keys
            elif event.type == pygame.KEYDOWN and event.key in [pygame.K_SPACE, pygame.K_RETURN, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                self.click_sound.play()
            
        if self.transition.transitioning:
            self.transition.handle_event(event)
        elif self.current_state in self.states and self.states[self.current_state]:
            self.states[self.current_state].handle_event(event)
            
    def update(self):
        """Update game state"""
        if self.transition.transitioning:
            self.transition.update()
        elif self.current_state in self.states and self.states[self.current_state]:
            self.states[self.current_state].update()
            
    def draw(self):
        """Draw current game state"""
        if self.current_state in self.states and self.states[self.current_state]:
            self.states[self.current_state].draw()
            
        # Draw transition effect on top if transitioning
        if self.transition.transitioning:
            self.transition.draw()
            
    def change_state(self, new_state):
        """Change the current game state immediately without transition"""
        if new_state in self.states:
            if self.current_state != new_state:  # Only change if state is actually changing
                # Special handling for suspense screen
                if new_state == "suspense_screen":
                    # Get the player's selection from the answer screen
                    player_selection = self.states["answer_screen"].selected_character
                    # Initialize the suspense screen with the player's selection
                    self.states["suspense_screen"].enter(player_selection)
                    
                self.current_state = new_state
                
                # Call enter method if it exists (for initialization)
                if hasattr(self.states[self.current_state], 'enter'):
                    self.states[self.current_state].enter()
            
    def load_scene(self, scene_name):
        """Load a scene from the DSL files"""
        self.current_scene = load_scene(scene_name)
        if self.current_scene:
            # Clear previous state
            self.characters = []
            
            # Add any evidence from the scene
            for evidence_data in self.current_scene.evidence:
                print("Loading evidence:", evidence_data)  # Debug print
                self.add_evidence(evidence_data)
                
            # Load characters and start dialogue
            for character_data in self.current_scene.characters:
                character = load_character(character_data['id'])
                if character:
                    self.characters.append(character)
                    if 'dialogue' in character_data:
                        # Start dialogue directly from scene data
                        dialogue_lines = character_data['dialogue']
                        if isinstance(dialogue_lines, list) and dialogue_lines:
                            # Initialize dialogue state with scene background
                            self.states['dialogue'].start_dialogue(
                                dialogue_lines,
                                {
                                    'image': character.image,
                                    'position': character_data['position']
                                },
                                self.current_scene.background
                            )
                            # Change state after dialogue is initialized
                            self.change_state('dialogue')
                            break  # Only start dialogue with first character
                
    def start_dialogue(self, character_id, dialogue_data):
        """Start a dialogue sequence with a character"""
        character = next((c for c in self.characters if c.id == character_id), None)
        if character:
            # Get character data from the current scene
            scene_character = next((c for c in self.current_scene.characters if c['id'] == character_id), None)
            if scene_character:
                self.states["dialogue"].start_dialogue(
                    dialogue_data,
                    {
                        'image': character.image,
                        'position': scene_character['position']  # Use position from scene
                    },
                    self.current_scene.background
                )
                self.change_state("dialogue")
            
    def add_evidence(self, evidence_item):
        """Add a new piece of evidence to the collection"""
        self.evidence.append(evidence_item)
        
    def get_evidence(self):
        """Get all collected evidence"""
        return self.evidence
        
    def start_interrogation(self, interrogation_id):
        """Start an interrogation sequence"""
        # Load the interrogation dialogue
        self.states["interrogation_screen"].load_interrogation(interrogation_id)
        # Change to the interrogation screen
        self.change_state("interrogation_screen")