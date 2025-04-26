import pygame
from dsl.parser import load_evidence
import os
import sys

class EvidenceBoard:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        
        # Track viewed evidence for interrogation unlock
        self.viewed_evidence = set()
        self.interrogation_unlocked = False
        self.show_interrogation_alert = False
        self.alert_timer = 0
        
        # Track new evidence alerts
        self.show_new_evidence_alert = False
        self.new_evidence_alert_timer = 0
        
        # Track Lisa interrogation alert
        self.show_lisa_interrogation_alert = False
        self.lisa_alert_timer = 0
        self.lisa_alert_shown = False  # Flag to track if we've already shown the Lisa alert
        
        # Track Alex's second interrogation alert
        self.show_alex2_interrogation_alert = False
        self.alex2_alert_timer = 0
        self.alex2_alert_shown = False  # Flag to track if we've already shown the Alex2 alert
        
        # Track post-Alex-2 evidence alert
        self.show_post_alex2_evidence_alert = False
        self.post_alex2_evidence_alert_timer = 0
        self.post_alex2_evidence_alert_shown = False  # Flag to track if we've already shown the post-Alex2 evidence alert
        
        # Hover effect tracking
        self.hovered_thumbnail_index = -1  # Index of the thumbnail being hovered (-1 means none)
        self.suspects_button_hovered = False
        self.interrogation_button_hovered = False
        self.arrest_button_hovered = False
        
        # Load fonts
        self.load_fonts()
        
        # Load the background image first
        self.background = None
        self.load_background()
        
        # Define multi-page evidence with all PNG pages
        self.financial_pages = [
            'assets/images/evidence/financial_cover.png',  # First page (cover)
            'assets/images/evidence/financial_page_1.png',  # Page 1
            'assets/images/evidence/financial_page_2.png',  # Page 2
            'assets/images/evidence/financial_page_3.png',  # Page 3
            'assets/images/evidence/financial_page_4.png',  # Page 4
        ]
        
        # Define ballistics report pages
        self.ballistics_pages = [
            'assets/images/evidence/ballistics_cover.png',  # Cover page
            'assets/images/evidence/ballistics_report-1.png',  # Page 1
            'assets/images/evidence/ballistics_report-2.png',  # Page 2
            'assets/images/evidence/ballistics_report-3.png',  # Page 3
            'assets/images/evidence/ballistics_report-4.png',  # Page 4
            'assets/images/evidence/ballistics_report-5.png',  # Page 5
            'assets/images/evidence/ballistics_report-6.png',  # Page 6
            'assets/images/evidence/ballistics_report-7.png',  # Page 7
        ]
        
        # Define Alex & Mary's text thread pages
        self.alex_mary_pages = [
            'assets/images/evidence/alex_mary_thread-1.png',  # Page 1
            'assets/images/evidence/alex_mary_thread-2.png',  # Page 2
            'assets/images/evidence/alex_mary_thread-3.png',  # Page 3
            'assets/images/evidence/alex_mary_thread-4.png',  # Page 4
            'assets/images/evidence/alex_mary_thread-5.png',  # Page 5
        ]
        
        # Define Emily & Sarah's text thread pages
        self.emily_sarah_pages = [
            'assets/images/evidence/emily_sarah_thread-1.png',  # Page 1
            'assets/images/evidence/emily_sarah_thread-2.png',  # Page 2
            'assets/images/evidence/emily_sarah_thread-3.png',  # Page 3
        ]
        
        # Define suspect list pages
        self.suspect_pages = [
            'assets/images/evidence/suspect_cover-1.png',  # Cover page
            'assets/images/evidence/suspect_list-1.png',  # Page 1
            'assets/images/evidence/suspect_list-2.png',  # Page 2
            'assets/images/evidence/suspect_list-3.png',  # Page 3
            'assets/images/evidence/suspect_list-4.png',  # Page 4
            'assets/images/evidence/suspect_list-5.png',  # Page 5
        ]
        
        # Vertical scroll position for evidence viewing
        self.evidence_scroll_y = 0
        self.evidence_scroll_speed = 20  # Original scroll speed
        
        # Define fixed positions for each evidence item (scattered around the board)
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        # Create scattered positions for evidence items
        self.evidence_positions = [
            # Ballistics report - top left area
            (screen_width * 0.15, screen_height * 0.2),
            # Financial records - top center area
            (screen_width * 0.45, screen_height * 0.2),
            # Gas receipt - top right area
            (screen_width * 0.75, screen_height * 0.2),
            # Alex & Mary texts - middle left area
            (screen_width * 0.2, screen_height * 0.45),
            # Emily & Sarah texts - middle right area
            (screen_width * 0.7, screen_height * 0.45),
            # Security camera - moved to middle center area
            (screen_width * 0.45, screen_height * 0.45),
            # Witness statement - moved further to the right
            (screen_width * 0.75, screen_height * 0.7),
        ]
        
        # Initial evidence items
        self.initial_evidence_items = [
            # Ballistics report is hidden initially
            # Will be added back after Emily's interrogation
            {
                'id': 'financials',
                'name': 'Financial Records',
                'image': 'assets/images/evidence/financial_cover.png',
                'multi_page': True,
                'current_page': 0,
                'pages': self.financial_pages,
                'available': True
            },
            {
                'id': 'emily_ticket',
                'name': 'Emily\'s Charity Gala Ticket',
                'image': 'assets/images/evidence/emily_ticket.png',
                'multi_page': False,
                'current_page': 0,
                'pages': [],
                'available': True,
                'position': (screen_width * 0.45, screen_height * 0.7)  # Custom position in bottom center
            },
            {
                'id': 'receipt',
                'name': 'Gas Station Receipt',
                'image': 'assets/images/evidence/gas_receipt.png',
                'multi_page': False,
                'current_page': 0,
                'pages': [],
                'available': True
            },
            {
                'id': 'alex_mary_texts',
                'name': 'Alex & Mary Texts',
                'image': 'assets/images/evidence/alex_mary_thread-1.png',
                'multi_page': True,
                'current_page': 0,
                'pages': self.alex_mary_pages,
                'available': True
            },
            {
                'id': 'emily_sarah_texts',
                'name': 'Emily & Sarah Texts',
                'image': 'assets/images/evidence/emily_sarah_thread-1.png',
                'multi_page': True,
                'current_page': 0,
                'pages': self.emily_sarah_pages,
                'available': True
            },
            {
                'id': 'lisa_leaving',
                'name': 'Security Camera Image',
                'image': 'assets/images/evidence/lisa_leaving.png',
                'multi_page': False,
                'current_page': 0,
                'pages': [],
                'available': True
            },
            {
                'id': 'witness_statement',
                'name': "Tom's Witness Statement",
                'image': 'assets/images/evidence/witness_statement-1.png',
                'multi_page': False,
                'current_page': 0,
                'pages': [],
                'available': True
            }
        ]
        
        # Evidence that becomes available after Mary's interrogation
        self.post_mary_evidence = [
            {
                'id': 'anonymous_letter',
                'name': 'Anonymous Letter',
                'image': 'assets/images/evidence/anonymous_letter.png',
                'multi_page': False,
                'current_page': 0,
                'pages': [],
                'available': False,
                'position': (screen_width * 0.35, screen_height * 0.3)  # Custom position up and to the right
            },
            {
                'id': 'alex_gun',
                'name': "Alex's Gun",
                'image': 'assets/images/evidence/alex_gun.png',
                'multi_page': False,
                'current_page': 0,
                'pages': [],
                'available': False,
                'position': (screen_width * 0.85, screen_height * 0.45)  # Custom position moved to the right
            }
        ]
        
        # Evidence that becomes available after Emily's interrogation
        self.post_emily_evidence = [
            {
                'id': 'ballistics',
                'name': 'Ballistics Report',
                'image': 'assets/images/evidence/ballistics_cover.png',
                'multi_page': True,
                'current_page': 0,
                'pages': self.ballistics_pages,
                'available': False,
                'position': (screen_width * 0.65, screen_height * 0.7)  # Moved to where witness statement was
            }
        ]
        
        # Evidence that becomes available after Alex's second interrogation
        self.post_alex2_evidence = [
            {
                'id': 'alex_mary_bed',
                'name': 'Alex & Mary Photo',
                'image': 'assets/images/evidence/alex_mary_bed.png',
                'multi_page': False,
                'current_page': 0,
                'pages': [],
                'available': False,
                'position': (screen_width * 0.25, screen_height * 0.7)  # Custom position bottom left
            },
            {
                'id': 'alex_watch',
                'name': 'Alex\'s Apple Watch GPS',
                'image': 'assets/images/evidence/alex_watch.png',
                'multi_page': False,
                'current_page': 0,
                'pages': [],
                'available': False,
                'position': (screen_width * 0.35, screen_height * 0.55)  # Custom position middle center-left
            }
        ]
        
        # Combine all evidence items
        self.evidence_items = self.initial_evidence_items + self.post_mary_evidence + self.post_emily_evidence + self.post_alex2_evidence
        
        self.selected_evidence = None
        self.thumbnail_size = (180, 140)
        self.padding = 20
        self.scroll_offset = 0
        
    def enter(self):
        """Called when entering the evidence board state"""
        # Reset scroll position to ensure board is always at the top
        self.scroll_offset = 0
        
    def load_fonts(self):
        """Load fonts for the evidence board"""
        # Default fonts (fallback)
        self.title_font = pygame.font.Font(None, 64)
        self.button_font = pygame.font.Font(None, 32)
        self.small_button_font = pygame.font.Font(None, 28)
        self.alert_font = pygame.font.Font(None, 28)
        
        # Try to load typewriter font
        try:
            font_path = os.path.join('assets', 'fonts', 'typewriter.ttf')
            if os.path.exists(font_path):
                print(f"Loading typewriter font from: {font_path}")
                self.button_font = pygame.font.Font(font_path, 30)
                self.small_button_font = pygame.font.Font(font_path, 26)
                self.alert_font = pygame.font.Font(font_path, 26)
                print("Typewriter font loaded successfully!")
            else:
                print(f"Warning: Typewriter font not found at {font_path}")
        except Exception as e:
            print(f"Error loading typewriter font: {e}")
    
    def handle_event(self, event):
        """Handle user input events"""
        # Check for clicks or spacebar to dismiss alerts
        if (self.show_new_evidence_alert or self.show_interrogation_alert or 
            self.show_lisa_interrogation_alert or self.show_alex2_interrogation_alert or
            self.show_post_alex2_evidence_alert) and \
           (event.type == pygame.MOUSEBUTTONDOWN or 
             (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE)):
            self.show_new_evidence_alert = False
            self.show_interrogation_alert = False
            self.show_lisa_interrogation_alert = False
            self.show_alex2_interrogation_alert = False
            self.show_post_alex2_evidence_alert = False
            return True
            
        if self.selected_evidence:
            # Handle evidence view events
            return self.handle_evidence_view_event(event)
        else:
            # Handle evidence board events
            return self.handle_board_event(event)
    
    def handle_board_event(self, event):
        """Handle events when viewing the evidence board"""
        if event.type == pygame.MOUSEMOTION:
            # Track mouse position for hover effects - use event.pos for immediate response
            mouse_pos = event.pos
            
            # Reset all hover states first
            self.hovered_thumbnail_index = -1
            self.suspects_button_hovered = False
            self.arrest_button_hovered = False
            self.interrogation_button_hovered = False
            
            # Define button rectangles once to avoid recalculation
            suspects_rect = pygame.Rect(20, self.screen.get_height() - 60, 180, 50)
            arrest_rect = pygame.Rect(self.screen.get_width() // 2 - 110, self.screen.get_height() - 60, 220, 50)
            interrogation_rect = None
            if self.interrogation_unlocked:
                interrogation_rect = pygame.Rect(self.screen.get_width() - 200, self.screen.get_height() - 60, 180, 50)
            
            # Check button hovers first (they're fewer checks than thumbnails)
            if suspects_rect.collidepoint(mouse_pos):
                self.suspects_button_hovered = True
                return True
            elif arrest_rect.collidepoint(mouse_pos):
                self.arrest_button_hovered = True
                return True
            elif interrogation_rect and interrogation_rect.collidepoint(mouse_pos):
                self.interrogation_button_hovered = True
                return True
            
            # Check for thumbnail hovers
            available_evidence = [e for e in self.evidence_items if e.get('available', True)]
            for i, evidence in enumerate(available_evidence):
                thumb_rect = self.get_thumbnail_rect(i)
                # Skip if thumbnail is off-screen
                if thumb_rect.bottom < 0 or thumb_rect.top > self.screen.get_height():
                    continue
                if thumb_rect.collidepoint(mouse_pos):
                    self.hovered_thumbnail_index = i
                    return True
            
            return True
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                # Check if clicking on help button first
                if hasattr(self, 'help_button_rect') and self.help_button_rect.collidepoint(event.pos):
                    # Transition to help screen
                    self.game.change_state("help_screen")
                    return True
                # Check if clicking on tips button
                if hasattr(self, 'tips_button_rect') and self.tips_button_rect.collidepoint(event.pos):
                    # Transition to tips screen
                    self.game.change_state("tips_screen")
                    return True
                # Otherwise handle other clicks
                self.handle_click(event.pos)
                return True
            # Mouse wheel scrolling disabled for the main evidence board view
            # Only enabled when viewing individual evidence items
        return False
        
    def handle_click(self, pos):
        """Handle mouse clicks on the evidence board"""
        # Check if clicking interrogation button (if unlocked)
        if self.interrogation_unlocked:
            interrogation_rect = pygame.Rect(self.screen.get_width() - 200, self.screen.get_height() - 60, 180, 50)
            if interrogation_rect.collidepoint(pos):
                # Hide the alert when clicking the interrogation button
                self.show_interrogation_alert = False
                self.show_lisa_interrogation_alert = False
                self.alert_timer = 0
                self.lisa_alert_timer = 0
                self.game.change_state("interrogation_menu")
                return
                
        # Check if clicking suspects button
        suspects_rect = pygame.Rect(20, self.screen.get_height() - 60, 180, 50)
        if suspects_rect.collidepoint(pos):
            self.view_suspects()
            return
            
        # Check if clicking Submit Arrest Warrant button
        arrest_rect = pygame.Rect(self.screen.get_width() // 2 - 110, self.screen.get_height() - 60, 220, 50)
        if arrest_rect.collidepoint(pos):
            self.game.change_state("answer_screen")
            return
                
        # Check if clicking on evidence thumbnail
        available_evidence = [e for e in self.evidence_items if e.get('available', True)]
        for i, evidence in enumerate(available_evidence):
            thumb_rect = self.get_thumbnail_rect(i)
            if thumb_rect.collidepoint(pos):
                self.selected_evidence = evidence
                # Add to viewed evidence set
                self.viewed_evidence.add(evidence['id'])
                
                # Check if we've viewed enough evidence to unlock interrogations
                if len(self.viewed_evidence) >= 3 and not self.interrogation_unlocked:
                    self.interrogation_unlocked = True
                    self.show_interrogation_alert = True
                    self.alert_timer = 300  # Show alert for 5 seconds
                
                # Check if we've viewed 6 or more evidence files after Mary's interrogation
                # to unlock Lisa's interrogation
                if (len(self.viewed_evidence) >= 6 and 
                    "mary_interrogation" in self.game.states["interrogation_menu"].completed_interrogations and
                    not self.lisa_alert_shown):  # Only show if we haven't shown it before
                    # Show alert for Lisa's interrogation
                    self.display_lisa_interrogation_alert()
                
                # Check if we're viewing the ballistics report and Emily's interrogation is completed
                # to unlock Alex's second interrogation
                if (evidence['id'] == 'ballistics' and
                    "emily_interrogation" in self.game.states["interrogation_menu"].completed_interrogations and
                    not self.alex2_alert_shown):  # Only show if we haven't shown it before
                    # Show alert for Alex's second interrogation
                    self.display_alex2_interrogation_alert()
                return
        
    def handle_evidence_view_event(self, event):
        """Handle events when viewing a specific evidence item"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                # Check for back button click
                back_rect = pygame.Rect(self.screen.get_width() - 120, 20, 100, 40)
                if back_rect.collidepoint(event.pos):
                    self.selected_evidence = None
                    return True
            # Mouse wheel for scrolling
            elif event.button == 4:  # Scroll up
                self.evidence_scroll_y = min(0, self.evidence_scroll_y + 50)
                return True
            elif event.button == 5:  # Scroll down
                self.evidence_scroll_y -= 50
                return True
        
        elif event.type == pygame.KEYDOWN:
            if self.selected_evidence['multi_page']:
                # Left/right arrows for page navigation
                if event.key == pygame.K_LEFT:
                    self.selected_evidence['current_page'] = max(0, self.selected_evidence['current_page'] - 1)
                    # Reset scroll position when changing pages
                    self.evidence_scroll_y = 0
                    return True
                elif event.key == pygame.K_RIGHT:
                    max_page = len(self.selected_evidence['pages']) - 1
                    self.selected_evidence['current_page'] = min(max_page, self.selected_evidence['current_page'] + 1)
                    # Reset scroll position when changing pages
                    self.evidence_scroll_y = 0
                    return True
            
            # Up/down arrows for scrolling
            if event.key == pygame.K_UP:
                self.evidence_scroll_y = min(0, self.evidence_scroll_y + 50)  # Faster scrolling
                return True
            elif event.key == pygame.K_DOWN:
                self.evidence_scroll_y -= 50  # Faster scrolling
                return True
                
        return False
                
    def get_thumbnail_rect(self, index):
        """Get the rectangle for a thumbnail at the given index using scattered positions"""
        evidence = self.evidence_items[index] if index < len(self.evidence_items) else None
        
        # Check if this evidence has a custom position
        if evidence and 'position' in evidence:
            pos_x, pos_y = evidence['position']
            x = pos_x - self.thumbnail_size[0] / 2  # Center the thumbnail on the position
            y = pos_y - self.thumbnail_size[1] / 2 - self.scroll_offset
        elif index < len(self.evidence_positions):
            # Use the predefined scattered position
            pos_x, pos_y = self.evidence_positions[index]
            x = pos_x - self.thumbnail_size[0] / 2  # Center the thumbnail on the position
            y = pos_y - self.thumbnail_size[1] / 2 - self.scroll_offset
        else:
            # Fallback to grid layout if we have more evidence than positions
            columns = 3
            row = index // columns
            col = index % columns
            x = self.padding + col * (self.thumbnail_size[0] + self.padding)
            y = self.padding + row * (self.thumbnail_size[1] + self.padding * 2) - self.scroll_offset
        
        # Return the rectangle
        return pygame.Rect(x, y, self.thumbnail_size[0], self.thumbnail_size[1])
        
    def load_background(self):
        """Load the bulletin board background"""
        try:
            # Use absolute path to ensure the image is found
            bg_path = 'assets/images/backgrounds/bare_board.png'
            self.background = pygame.image.load(bg_path).convert()
            # Scale to screen size
            self.background = pygame.transform.scale(self.background, 
                                                  (self.screen.get_width(), self.screen.get_height()))
        except Exception as e:
            print(f"Error loading bulletin board background: {e}")
            self.background = None
            
    def update(self):
        """Update evidence board state"""
        # Check if Alex's second interrogation has been completed to show post-Alex2 evidence alert
        if ("alex_2_interrogation" in self.game.states["interrogation_menu"].completed_interrogations and
            not self.post_alex2_evidence_alert_shown):  # Only show if we haven't shown it before
            # Show alert for post-Alex2 evidence
            self.display_post_alex2_evidence_alert()
            
        # Update interrogation alert timer
        if self.show_interrogation_alert and self.alert_timer > 0:
            self.alert_timer -= 1
            if self.alert_timer <= 0:
                self.show_interrogation_alert = False
                
        # Update new evidence alert timer
        if self.show_new_evidence_alert and self.new_evidence_alert_timer > 0:
            self.new_evidence_alert_timer -= 1
            if self.new_evidence_alert_timer <= 0:
                self.show_new_evidence_alert = False
                
        # Update Lisa interrogation alert timer
        if self.show_lisa_interrogation_alert and self.lisa_alert_timer > 0:
            self.lisa_alert_timer -= 1
            if self.lisa_alert_timer <= 0:
                self.show_lisa_interrogation_alert = False
                
        # Update Alex's second interrogation alert timer
        if self.show_alex2_interrogation_alert and self.alex2_alert_timer > 0:
            self.alex2_alert_timer -= 1
            if self.alex2_alert_timer <= 0:
                self.show_alex2_interrogation_alert = False
                
        # Update post-Alex2 evidence alert timer
        if self.show_post_alex2_evidence_alert and self.post_alex2_evidence_alert_timer > 0:
            self.post_alex2_evidence_alert_timer -= 1
            if self.post_alex2_evidence_alert_timer <= 0:
                self.show_post_alex2_evidence_alert = False
        
    def draw(self):
        """Draw the evidence board"""
        # Clear screen first
        self.screen.fill((0, 0, 0))
        
        # Draw background
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            # Fallback to plain background
            self.screen.fill((40, 30, 20))
            
        # Draw evidence items or selected evidence
        if self.selected_evidence:
            self.draw_evidence_view()
        else:
            self.draw_thumbnails()
            
        # Draw alerts on top of everything if needed
        if self.show_interrogation_alert:
            self.draw_interrogation_alert()
            
        if self.show_new_evidence_alert:
            self.draw_new_evidence_alert()
            
        if self.show_lisa_interrogation_alert:
            self.draw_lisa_interrogation_alert()
            
        if self.show_alex2_interrogation_alert:
            self.draw_alex2_interrogation_alert()
            
        if self.show_post_alex2_evidence_alert:
            self.draw_new_evidence_alert()
            
    def draw_thumbnails(self):
        """Draw evidence thumbnails on the board"""
        instruction_font = pygame.font.Font(None, 24)
        
        # Draw the title with typewriter font
        try:
            # Use typewriter font for the title
            font_path = os.path.join('assets', 'fonts', 'typewriter.ttf')
            if os.path.exists(font_path):
                title_font = pygame.font.Font(font_path, 64)
            else:
                title_font = pygame.font.Font(None, 64)
        except Exception:
            title_font = pygame.font.Font(None, 64)
            
        # Define a consistent top margin for all elements
        top_margin = 10  # SIZE OF TOP MARGIN
        
        # Center the title with the new top margin
        title_text = title_font.render("EVIDENCE BOARD", True, (255, 255, 255))
        title_rect = title_text.get_rect(centerx=self.screen.get_width() // 2, top=top_margin)
        self.screen.blit(title_text, title_rect)
        
        # Load button fonts
        try:
            help_font = pygame.font.Font('assets/fonts/typewriter.ttf', 24)
        except Exception as e:
            help_font = pygame.font.Font(None, 24)  # Fallback
            
        # Load lightbulb image for tips button
        self.lightbulb_img = None
        try:
            self.lightbulb_img = pygame.image.load('assets/images/other/light.png')
            self.lightbulb_img = pygame.transform.scale(self.lightbulb_img, (60, 60))  # Increased from 40x40 to 60x60
        except Exception as e:
            # We'll handle rendering without the image if it fails to load
            pass
            
        # Create help button - align with title vertically
        help_button_width = 80
        help_button_height = 30
        help_button_y = top_margin + (title_rect.height - help_button_height) // 2  # Center vertically with title
        self.help_button_rect = pygame.Rect(20, help_button_y, help_button_width, help_button_height)
        help_text = help_font.render("Help?", True, (200, 200, 200))  # Light gray color
        help_text_rect = help_text.get_rect(center=self.help_button_rect.center)
        
        # Create tips button in top-right corner - align with title vertically
        lightbulb_size = 60
        lightbulb_y = top_margin + (title_rect.height - lightbulb_size) // 2  # Center vertically with title
        self.tips_button_rect = pygame.Rect(self.screen.get_width() - 80, lightbulb_y, lightbulb_size, lightbulb_size)
        
        # Check if mouse is hovering over help button
        mouse_pos = pygame.mouse.get_pos()
        if self.help_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, (60, 60, 60), self.help_button_rect)  # Darker background when hovered
        
        # Draw the help button text
        self.screen.blit(help_text, help_text_rect)
        
        # Draw the tips button (lightbulb)
        if self.lightbulb_img:
            # Draw the lightbulb image
            self.screen.blit(self.lightbulb_img, self.tips_button_rect)
            
            # Add a glow effect if hovered
            if self.tips_button_rect.collidepoint(mouse_pos):
                # Create a larger semi-transparent yellow surface for the glow
                glow_surface = pygame.Surface((60, 60), pygame.SRCALPHA)
                pygame.draw.circle(glow_surface, (255, 255, 0, 100), (30, 30), 25)  # Yellow glow
                glow_rect = glow_surface.get_rect(center=self.tips_button_rect.center)
                self.screen.blit(glow_surface, glow_rect)
        else:
            # Fallback if image not loaded
            if self.tips_button_rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, (60, 60, 60), self.tips_button_rect)  # Darker background when hovered
            pygame.draw.circle(self.screen, (255, 255, 0), self.tips_button_rect.center, 15)  # Yellow circle
            pygame.draw.rect(self.screen, (255, 255, 0), pygame.Rect(self.tips_button_rect.centerx - 2, self.tips_button_rect.top + 5, 4, 8))  # Bulb top
        
        # Draw each evidence thumbnail (only if available)
        available_evidence = [e for e in self.evidence_items if e.get('available', True)]
        for i, evidence in enumerate(available_evidence):
            thumb_rect = self.get_thumbnail_rect(i)
            
            # Skip if thumbnail is off-screen
            if thumb_rect.bottom < 0 or thumb_rect.top > self.screen.get_height():
                continue
                
            try:
                # Load and scale the image
                image = pygame.image.load(evidence['image'])
                
                # Calculate scaling to maintain aspect ratio
                original_width, original_height = image.get_size()
                max_width, max_height = self.thumbnail_size
                
                # Calculate new dimensions while maintaining aspect ratio
                if original_width > original_height:
                    # Landscape orientation
                    new_width = max_width
                    new_height = int(original_height * (max_width / original_width))
                else:
                    # Portrait or square orientation
                    new_height = max_height
                    new_width = int(original_width * (max_height / original_height))
                
                # Scale the image maintaining proportions
                image = pygame.transform.scale(image, (new_width, new_height))
                
                # Center the image in the thumbnail area
                image_x = thumb_rect.left + (max_width - new_width) // 2
                image_y = thumb_rect.top + (max_height - new_height) // 2
                
                # Check if this thumbnail is being hovered over
                is_hovered = (i == self.hovered_thumbnail_index)
                
                # Draw a red rectangle around the thumbnail if hovered
                if is_hovered:
                    # Draw a slightly larger rectangle for the hover effect
                    hover_rect = pygame.Rect(
                        image_x - 5, 
                        image_y - 5, 
                        new_width + 10, 
                        new_height + 10
                    )
                    pygame.draw.rect(self.screen, (200, 0, 0), hover_rect, 3)  # Red border, 3px width
                
                # Draw the image
                self.screen.blit(image, (image_x, image_y))
                
                # Draw a pushpin with special handling for specific evidence items
                if 'emily_ticket.png' in evidence['image']:
                    # Special case for emily_ticket.png which needs the thumbtack much lower
                    pygame.draw.circle(self.screen, (200, 0, 0), 
                                      (thumb_rect.centerx, thumb_rect.top + 45), 8)  # Red pushpin
                elif original_width > original_height:  # Other wide images
                    # Place thumbtack for wide images
                    pygame.draw.circle(self.screen, (200, 0, 0), 
                                      (thumb_rect.centerx, thumb_rect.top + 15), 8)  # Red pushpin
                else:  # Tall images (like lisa_leaving.png)
                    # Place thumbtack for tall images
                    pygame.draw.circle(self.screen, (200, 0, 0), 
                                      (thumb_rect.centerx, thumb_rect.top + 20), 8)  # Red pushpin
            except Exception as e:
                print(f"Error loading evidence image: {e}")
                # If image fails to load, draw minimal placeholder
                placeholder_text = instruction_font.render("?", True, (200, 0, 0))
                placeholder_rect = placeholder_text.get_rect(center=thumb_rect.center)
                self.screen.blit(placeholder_text, placeholder_rect)
        
        # Draw interrogation button if unlocked
        if self.interrogation_unlocked:
            button_rect = pygame.Rect(self.screen.get_width() - 220, self.screen.get_height() - 60, 200, 50)
            
            # Grey by default, red when hovered
            if self.interrogation_button_hovered:
                button_color = (200, 0, 0)  # Bright red when hovered
            else:
                button_color = (80, 80, 80)  # Grey by default
                
            pygame.draw.rect(self.screen, button_color, button_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), button_rect, 2)  # White border
            
            # Use the loaded button font
            button_text = self.button_font.render("Interrogations", True, (255, 255, 255))
                
            button_text_rect = button_text.get_rect(center=button_rect.center)
            self.screen.blit(button_text, button_text_rect)

        # Draw the suspects button (always available)
        suspects_rect = pygame.Rect(20, self.screen.get_height() - 60, 200, 50)
        
        # Grey by default, red when hovered
        if self.suspects_button_hovered:
            suspects_color = (200, 0, 0)  # Bright red when hovered
        else:
            suspects_color = (80, 80, 80)  # Grey by default
            
        pygame.draw.rect(self.screen, suspects_color, suspects_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), suspects_rect, 2)  # White border
        
        # Use the loaded button font
        suspects_text = self.button_font.render('Suspects', True, (255, 255, 255))
            
        suspects_text_rect = suspects_text.get_rect(center=suspects_rect.center)
        self.screen.blit(suspects_text, suspects_text_rect)
        
        # Draw the Submit Arrest Warrant button (always available)
        arrest_rect = pygame.Rect(self.screen.get_width() // 2 - 130, self.screen.get_height() - 60, 260, 50)
        
        # Grey by default, red when hovered
        if self.arrest_button_hovered:
            arrest_color = (200, 0, 0)  # Bright red when hovered
        else:
            arrest_color = (80, 80, 80)  # Grey by default
            
        pygame.draw.rect(self.screen, arrest_color, arrest_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), arrest_rect, 2)  # White border
        
        # Use the loaded small button font
        arrest_text = self.small_button_font.render('Submit Arrest Warrant', True, (255, 255, 255))
            
        arrest_text_rect = arrest_text.get_rect(center=arrest_rect.center)
        self.screen.blit(arrest_text, arrest_text_rect)
    def draw_new_evidence_alert(self):
        """Draw the new evidence alert on top of everything"""
        # Semi-transparent background covering the entire screen
        alert_bg = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        alert_bg.fill((0, 0, 0))
        alert_bg.set_alpha(180)  # More transparent
        self.screen.blit(alert_bg, (0, 0))
        
        # Alert box background
        alert_box = pygame.Surface((self.screen.get_width() - 100, 120))
        alert_box.fill((40, 40, 40))
        alert_box_rect = alert_box.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(alert_box, alert_box_rect)
        pygame.draw.rect(self.screen, (0, 100, 0), alert_box_rect, 3)  # Green border
        
        # Alert text with loaded alert font
        alert_text = "New Evidence Files Are Available!"
        alert_text2 = "Check the evidence board for new items."
        
        text1 = self.alert_font.render(alert_text, True, (255, 255, 255))
        text2 = self.alert_font.render(alert_text2, True, (255, 255, 255))
        
        text1_rect = text1.get_rect(centerx=self.screen.get_width() // 2, centery=self.screen.get_height() // 2 - 20)
        text2_rect = text2.get_rect(centerx=self.screen.get_width() // 2, centery=self.screen.get_height() // 2 + 20)
        
        self.screen.blit(text1, text1_rect)
        self.screen.blit(text2, text2_rect)
        
    def draw_lisa_interrogation_alert(self):
        """Draw the Lisa interrogation alert on top of everything"""
        # Semi-transparent background covering the entire screen
        alert_bg = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        alert_bg.fill((0, 0, 0))
        alert_bg.set_alpha(180)  # More transparent
        self.screen.blit(alert_bg, (0, 0))
        
        # Alert box background
        alert_box = pygame.Surface((self.screen.get_width() - 100, 120))
        alert_box.fill((40, 40, 40))
        alert_box_rect = alert_box.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(alert_box, alert_box_rect)
        pygame.draw.rect(self.screen, (150, 0, 0), alert_box_rect, 3)  # Red border
        
        # Alert text with loaded alert font
        alert_text = "Detective! Lisa is here for her interrogation and Emily will be here shortly!"
        alert_text2 = "Please click the 'Interrogations' button to move to the interrogation menu!"
        
        text1 = self.alert_font.render(alert_text, True, (255, 255, 255))
        text2 = self.alert_font.render(alert_text2, True, (255, 255, 255))
        
        text1_rect = text1.get_rect(centerx=self.screen.get_width() // 2, centery=self.screen.get_height() // 2 - 20)
        text2_rect = text2.get_rect(centerx=self.screen.get_width() // 2, centery=self.screen.get_height() // 2 + 20)
        
        self.screen.blit(text1, text1_rect)
        self.screen.blit(text2, text2_rect)
        
    def draw_alex2_interrogation_alert(self):
        """Draw the Alex's second interrogation alert on top of everything"""
        # Semi-transparent background covering the entire screen
        alert_bg = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        alert_bg.fill((0, 0, 0))
        alert_bg.set_alpha(180)  # More transparent
        self.screen.blit(alert_bg, (0, 0))
        
        # Alert box background
        alert_box = pygame.Surface((self.screen.get_width() - 100, 120))
        alert_box.fill((40, 40, 40))
        alert_box_rect = alert_box.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(alert_box, alert_box_rect)
        pygame.draw.rect(self.screen, (150, 0, 0), alert_box_rect, 3)  # Red border
        
        # Alert text with loaded alert font
        alert_text = "Detective! Alex is back for his second interrogation."
        alert_text2 = "Please click the 'Interrogations' button to move to the interrogation menu!"
        
        text1 = self.alert_font.render(alert_text, True, (255, 255, 255))
        text2 = self.alert_font.render(alert_text2, True, (255, 255, 255))
        
        text1_rect = text1.get_rect(centerx=self.screen.get_width() // 2, centery=self.screen.get_height() // 2 - 20)
        text2_rect = text2.get_rect(centerx=self.screen.get_width() // 2, centery=self.screen.get_height() // 2 + 20)
        
        self.screen.blit(text1, text1_rect)
        self.screen.blit(text2, text2_rect)
        
    def draw_interrogation_alert(self):
        """Draw the interrogation unlock alert on top of everything"""
        # Semi-transparent background covering the entire screen
        alert_bg = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        alert_bg.fill((0, 0, 0))
        alert_bg.set_alpha(180)  # More transparent
        self.screen.blit(alert_bg, (0, 0))
        
        # Alert box background
        alert_box = pygame.Surface((self.screen.get_width() - 100, 120))
        alert_box.fill((40, 40, 40))
        alert_box_rect = alert_box.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(alert_box, alert_box_rect)
        pygame.draw.rect(self.screen, (0, 100, 0), alert_box_rect, 3)  # Green border
        
        # Alert text with typewriter font
        alert_text = "Interrogation Unlocked!"
        alert_text2 = "Return to the main menu to begin interrogations."
        
        # Use the loaded alert font
        text1 = self.alert_font.render(alert_text, True, (255, 255, 255))
        text2 = self.alert_font.render(alert_text2, True, (255, 255, 255))
        
        # Position and draw the alert text
        text1_rect = text1.get_rect(centerx=alert_box_rect.centerx, centery=alert_box_rect.centery - 20)
        text2_rect = text2.get_rect(centerx=alert_box_rect.centerx, centery=alert_box_rect.centery + 20)
        self.screen.blit(text1, text1_rect)
        self.screen.blit(text2, text2_rect)
        
    def display_lisa_interrogation_alert(self):
        """Show the Lisa interrogation alert and unlock Lisa's interrogation"""
        self.show_lisa_interrogation_alert = True
        self.lisa_alert_timer = 300  # Show for 5 seconds
        self.lisa_alert_shown = True  # Mark that we've shown the alert
        
        # Make Lisa's interrogation available in the interrogation menu
        for interrogation in self.game.states["interrogation_menu"].interrogations:
            if interrogation["id"] == "lisa_interrogation":
                interrogation["available"] = True
                
        # Force the interrogation menu to update its buttons
        self.game.states["interrogation_menu"].update_buttons()
        
    def display_alex2_interrogation_alert(self):
        """Show the Alex's second interrogation alert and unlock Alex's second interrogation"""
        self.show_alex2_interrogation_alert = True
        self.alex2_alert_timer = 300  # Show for 5 seconds
        self.alex2_alert_shown = True  # Mark that we've shown the alert
        
        # Make Alex's second interrogation available in the interrogation menu
        for interrogation in self.game.states["interrogation_menu"].interrogations:
            if interrogation["id"] == "alex_2_interrogation":
                interrogation["available"] = True
                
        # Force the interrogation menu to update its buttons
        self.game.states["interrogation_menu"].update_buttons()
        
    def display_post_alex2_evidence_alert(self):
        """Show the post-Alex2 evidence alert and make the new evidence available"""
        self.show_post_alex2_evidence_alert = True
        self.post_alex2_evidence_alert_timer = 300  # Show for 5 seconds
        self.post_alex2_evidence_alert_shown = True  # Mark that we've shown the alert
        
        # Make the post-Alex2 evidence available
        for evidence in self.post_alex2_evidence:
            evidence['available'] = True
        
    def view_suspects(self):
        """View the suspects list"""
        # Create a temporary evidence item for the suspects list
        suspects_evidence = {
            'id': 'suspects_list',
            'name': 'Suspects List',
            'image': self.suspect_pages[0],  # Use the cover page
            'multi_page': True,
            'current_page': 0,
            'pages': self.suspect_pages
        }
        
        # Set as the selected evidence to view
        self.selected_evidence = suspects_evidence
        
    def draw_evidence_view(self):
        """Draw the selected evidence in full view"""
        # First draw the background so it remains visible
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            # Fallback to plain background
            self.screen.fill((40, 30, 20))
        
        # Draw semi-transparent overlay to make the background darker
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(150)  # Semi-transparent
        self.screen.blit(overlay, (0, 0))
        
        # Draw evidence image based on current page for multi-page evidence
        try:
            # For multi-page evidence, use the current page
            if self.selected_evidence['multi_page']:
                current_page = self.selected_evidence['current_page']
                image_path = self.selected_evidence['pages'][current_page]
            else:
                # For single-page evidence, use the main image
                image_path = self.selected_evidence['image']
                
            # Load image with pygame's highest quality settings
            image = pygame.image.load(image_path)
            
            # For evidence viewing, we'll make the image larger and allow scrolling
            screen_rect = self.screen.get_rect()
            
            # Make images smaller (60% instead of 70%)
            # to reduce the need for excessive scrolling
            target_width = int(screen_rect.width * 0.6)
            
            # Calculate height proportionally
            image_rect = image.get_rect()
            aspect_ratio = image_rect.height / image_rect.width
            target_height = int(target_width * aspect_ratio)
            
            # Scale image with high quality
            image = pygame.transform.scale(image, (target_width, target_height))
            
            # Create a viewport for the image (area that will be visible)
            viewport_height = screen_rect.height - 150  # Leave space for UI elements
            
            # Position image centered horizontally, with vertical scrolling
            image_x = (screen_rect.width - target_width) // 2
            image_y = 80 + self.evidence_scroll_y  # Start below the title with scroll offset
            
            # Limit scrolling - don't allow scrolling past the bottom of the image
            min_scroll = min(0, viewport_height - target_height - 80)
            if self.evidence_scroll_y < min_scroll:
                self.evidence_scroll_y = min_scroll
            
            # Create a clipping rectangle for the viewport
            viewport_rect = pygame.Rect(0, 80, screen_rect.width, viewport_height)
            old_clip = self.screen.get_clip()
            self.screen.set_clip(viewport_rect)
            
            # Draw the image with scroll position
            self.screen.blit(image, (image_x, image_y))
            
            # Restore original clipping rectangle
            self.screen.set_clip(old_clip)
            
            # Draw scroll indicators if image is larger than viewport
            if target_height > viewport_height:
                scroll_font = pygame.font.Font(None, 22)
                # Place scroll instructions under the back button
                scroll_text_lines = ["Scroll Using", "Mouse or", "Up/Down", "Keys"]
                
                # Calculate position (under back button)
                scroll_x = self.screen.get_width() - 90  # Center under back button
                scroll_y = 70  # Start below back button
                
                # Draw each line of text
                for line in scroll_text_lines:
                    text = scroll_font.render(line, True, (200, 200, 200))
                    text_rect = text.get_rect(centerx=scroll_x, top=scroll_y)
                    self.screen.blit(text, text_rect)
                    scroll_y += 22  # Move down for next line
        except Exception as e:
            print(f"Error displaying evidence image: {e}")
            # If image fails to load, draw placeholder
            placeholder_rect = pygame.Rect(0, 0, 400, 300)
            placeholder_rect.center = self.screen.get_rect().center
            pygame.draw.rect(self.screen, (60, 60, 60), placeholder_rect)
    def draw_evidence_view(self):
        """Draw the selected evidence in full view"""
        try:
            # Draw back button (replacing the close button)
            back_rect = pygame.Rect(self.screen.get_width() - 120, 20, 100, 40)
            pygame.draw.rect(self.screen, (200, 0, 0), back_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), back_rect, 2)  # White border
            font = pygame.font.Font(None, 36)
            text = font.render('Back', True, (255, 255, 255))
            text_rect = text.get_rect(center=back_rect.center)
            self.screen.blit(text, text_rect)
        
            # Draw evidence name with background
            name_font = pygame.font.Font(None, 36)
            name_text = name_font.render(self.selected_evidence['name'], True, (255, 255, 255))
            name_rect = name_text.get_rect(centerx=self.screen.get_rect().centerx, top=20)
            
            # Background for name
            name_bg_rect = name_rect.copy()
            name_bg_rect.inflate_ip(20, 10)  # Make background slightly larger
            pygame.draw.rect(self.screen, (40, 40, 40), name_bg_rect)
            pygame.draw.rect(self.screen, (200, 0, 0), name_bg_rect, 2)  # Red border
            self.screen.blit(name_text, name_rect)
            
            # For multi-page evidence, show page navigation info
            if self.selected_evidence['multi_page']:
                current_page = self.selected_evidence['current_page'] + 1
                total_pages = len(self.selected_evidence['pages'])
                page_text = f"Page {current_page} of {total_pages}"
                    
                page_font = pygame.font.Font(None, 24)
                page_render = page_font.render(page_text, True, (255, 255, 255))
                page_rect = page_render.get_rect(centerx=self.screen.get_rect().centerx, 
                                               bottom=self.screen.get_rect().bottom - 20)
                self.screen.blit(page_render, page_rect)
                    
                # Add navigation hint
                if total_pages > 1:
                    nav_text = "Use Left/Right Arrow Keys to Navigate Pages"
                    nav_render = page_font.render(nav_text, True, (200, 200, 200))
                    nav_rect = nav_render.get_rect(right=self.screen.get_rect().width - 20, 
                                                 bottom=page_rect.top - 5)
                    self.screen.blit(nav_render, nav_rect)
            
            # Draw evidence image based on current page for multi-page evidence
            try:
                # For multi-page evidence, use the current page
                if self.selected_evidence['multi_page']:
                    current_page = self.selected_evidence['current_page']
                    image_path = self.selected_evidence['pages'][current_page]
                else:
                    # For single-page evidence, use the main image
                    image_path = self.selected_evidence['image']
                    
                # Load image with pygame's highest quality settings
                image = pygame.image.load(image_path)
                
                # For evidence viewing, we'll make the image larger and allow scrolling
                screen_rect = self.screen.get_rect()
                
                # Make images smaller (80% of screen width)
                target_width = int(screen_rect.width * 0.8)
                
                # Calculate height proportionally
                image_rect = image.get_rect()
                aspect_ratio = image_rect.height / image_rect.width
                target_height = int(target_width * aspect_ratio)
                
                # Scale image with high quality
                image = pygame.transform.scale(image, (target_width, target_height))
                
                # Create a viewport for the image (area that will be visible)
                viewport_height = screen_rect.height - 150  # Leave space for UI elements
                
                # Position image centered horizontally, with vertical scrolling
                image_x = (screen_rect.width - target_width) // 2
                image_y = 80 + self.evidence_scroll_y  # Start below the title with scroll offset
                
                # Limit scrolling - don't allow scrolling past the bottom of the image
                min_scroll = min(0, viewport_height - target_height - 80)
                if self.evidence_scroll_y < min_scroll:
                    self.evidence_scroll_y = min_scroll
                
                # Create a clipping rectangle for the viewport
                viewport_rect = pygame.Rect(0, 80, screen_rect.width, viewport_height)
                old_clip = self.screen.get_clip()
                self.screen.set_clip(viewport_rect)
                
                # Draw the image with scroll position
                self.screen.blit(image, (image_x, image_y))
                
                # Restore original clipping rectangle
                self.screen.set_clip(old_clip)
                
                # Draw scroll indicators if image is larger than viewport
                if target_height > viewport_height:
                    scroll_font = pygame.font.Font(None, 22)
                    # Place scroll instructions under the back button
                    scroll_text_lines = ["Scroll Using", "Mouse or", "Up/Down", "Keys"]
                    
                    # Calculate position (under back button)
                    scroll_x = self.screen.get_width() - 90  # Center under back button
                    scroll_y = 70  # Start below back button
                    
                    # Draw each line of text
                    for line in scroll_text_lines:
                        text = scroll_font.render(line, True, (200, 200, 200))
                        text_rect = text.get_rect(centerx=scroll_x, top=scroll_y)
                        self.screen.blit(text, text_rect)
                        scroll_y += 22  # Move down for next line
            except Exception as e:
                print(f"Error displaying evidence image: {e}")
                # If image fails to load, draw placeholder
                placeholder_rect = pygame.Rect(0, 0, 400, 300)
                placeholder_rect.center = self.screen.get_rect().center
                pygame.draw.rect(self.screen, (60, 60, 60), placeholder_rect)
                font = pygame.font.Font(None, 36)
                text = font.render('Image not available', True, (255, 255, 255))
                text_rect = text.get_rect(center=placeholder_rect.center)
                self.screen.blit(text, text_rect)
        except Exception as e:
            print(f"Error in draw_evidence_view: {e}")
