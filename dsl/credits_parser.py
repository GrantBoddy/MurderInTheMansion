import pygame
import os
import re

def load_credits_text(file_path='assets/text/credits.txt'):
    """
    Load and parse credits text from a DSL file
    
    The DSL supports the following commands:
    #FONT:size - Set font size
    #COLOR:r,g,b - Set text color
    #DELAY:seconds - Set typing delay
    #PAUSE:seconds - Set pause after line
    #ALIGN:left/center/right - Set text alignment
    #SPACING:pixels - Set line spacing
    """
    credits_lines = []
    
    try:
        # Default values
        current_font_size = 36
        current_color = (255, 255, 255)  # White
        current_delay = 0.05  # 50ms between characters
        current_pause = 1.0  # 1 second pause after line
        current_align = "center"  # Center alignment
        current_spacing = 10  # 10 pixels between lines
        
        if not os.path.exists(file_path):
            print(f"Credits file not found: {file_path}")
            # Return some default credits if file not found
            credits_lines.append({
                "text": "Credits",
                "font_size": 48,
                "color": (255, 255, 255),
                "delay": 0.05,
                "pause": 1.0,
                "align": "center",
                "spacing": 20
            })
            credits_lines.append({
                "text": "Thanks for playing!",
                "font_size": 36,
                "color": (200, 200, 200),
                "delay": 0.05,
                "pause": 1.0,
                "align": "center",
                "spacing": 10
            })
            return credits_lines
        
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                
                # Skip empty lines
                if not line:
                    continue
                
                # Parse commands
                if line.startswith('#'):
                    # Font size command
                    font_match = re.match(r'#FONT:(\d+)', line)
                    if font_match:
                        current_font_size = int(font_match.group(1))
                        continue
                    
                    # Color command
                    color_match = re.match(r'#COLOR:(\d+),(\d+),(\d+)', line)
                    if color_match:
                        r = int(color_match.group(1))
                        g = int(color_match.group(2))
                        b = int(color_match.group(3))
                        current_color = (r, g, b)
                        continue
                    
                    # Delay command
                    delay_match = re.match(r'#DELAY:([\d.]+)', line)
                    if delay_match:
                        current_delay = float(delay_match.group(1))
                        continue
                    
                    # Pause command
                    pause_match = re.match(r'#PAUSE:([\d.]+)', line)
                    if pause_match:
                        current_pause = float(pause_match.group(1))
                        continue
                    
                    # Alignment command
                    align_match = re.match(r'#ALIGN:(left|center|right)', line)
                    if align_match:
                        current_align = align_match.group(1)
                        continue
                    
                    # Spacing command
                    spacing_match = re.match(r'#SPACING:(\d+)', line)
                    if spacing_match:
                        current_spacing = int(spacing_match.group(1))
                        continue
                
                # Regular text line
                credits_lines.append({
                    "text": line,
                    "font_size": current_font_size,
                    "color": current_color,
                    "delay": current_delay,
                    "pause": current_pause,
                    "align": current_align,
                    "spacing": current_spacing
                })
    
    except Exception as e:
        print(f"Error loading credits text: {e}")
        # Return a simple error message as credits
        credits_lines.append({
            "text": "Error loading credits",
            "font_size": 36,
            "color": (255, 0, 0),
            "delay": 0.05,
            "pause": 1.0,
            "align": "center",
            "spacing": 10
        })
    
    return credits_lines
