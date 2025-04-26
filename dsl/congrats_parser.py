import os
import pygame

def load_congrats_text(file_path='assets/text/congrats.txt'):
    """
    Load congratulatory text from a DSL file.
    
    Format:
    - Regular lines are displayed as is
    - Lines starting with #DELAY: set the delay between characters (e.g., #DELAY:0.05)
    - Lines starting with #PAUSE: set a pause after the line (e.g., #PAUSE:1.5)
    - Lines starting with #FONT: set the font size (e.g., #FONT:32)
    - Lines starting with #COLOR: set the text color (e.g., #COLOR:255,255,255)
    
    Returns a list of text objects with their properties.
    """
    if not os.path.exists(file_path):
        print(f"Warning: Congrats text file not found at {file_path}")
        # Return default congratulatory text
        return [
            {"text": "Congratulations, Detective!", "delay": 0.05, "pause": 1.0, "font_size": 36, "color": (255, 255, 255)},
            {"text": "You've successfully solved the case.", "delay": 0.05, "pause": 0.5, "font_size": 32, "color": (200, 200, 200)},
            {"text": "Lisa has been arrested for the murder.", "delay": 0.05, "pause": 0.5, "font_size": 32, "color": (200, 200, 200)},
            {"text": "Justice has been served.", "delay": 0.05, "pause": 1.0, "font_size": 32, "color": (200, 200, 200)},
            {"text": "Press any key to return to the menu.", "delay": 0.05, "pause": 0.0, "font_size": 24, "color": (150, 150, 150)}
        ]
    
    try:
        congrats_lines = []
        current_delay = 0.05  # Default delay between characters
        current_pause = 0.5   # Default pause after each line
        current_font_size = 32  # Default font size
        current_color = (255, 255, 255)  # Default color (white)
        
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:  # Skip empty lines
                    continue
                
                # Process DSL commands
                if line.startswith('#DELAY:'):
                    try:
                        current_delay = float(line.split(':', 1)[1])
                        print(f"Set delay to {current_delay}")
                    except (ValueError, IndexError):
                        print(f"Warning: Invalid delay format in line: {line}")
                    continue
                
                elif line.startswith('#PAUSE:'):
                    try:
                        current_pause = float(line.split(':', 1)[1])
                        print(f"Set pause to {current_pause}")
                    except (ValueError, IndexError):
                        print(f"Warning: Invalid pause format in line: {line}")
                    continue
                
                elif line.startswith('#FONT:'):
                    try:
                        current_font_size = int(line.split(':', 1)[1])
                        print(f"Set font size to {current_font_size}")
                    except (ValueError, IndexError):
                        print(f"Warning: Invalid font size format in line: {line}")
                    continue
                
                elif line.startswith('#COLOR:'):
                    try:
                        color_values = line.split(':', 1)[1].split(',')
                        if len(color_values) == 3:
                            r = int(color_values[0].strip())
                            g = int(color_values[1].strip())
                            b = int(color_values[2].strip())
                            current_color = (r, g, b)
                        else:
                            print(f"Warning: Invalid color format in line: {line}")
                    except (ValueError, IndexError):
                        print(f"Warning: Invalid color format in line: {line}")
                    continue
                
                # Check if this is a continuation of the previous line
                if congrats_lines and line.endswith('\\'):
                    # This is a line continuation, append to the previous line
                    congrats_lines[-1]["text"] += "\n" + line[:-1].strip()
                elif congrats_lines and congrats_lines[-1]["text"].endswith('\\'):
                    # Previous line ended with continuation marker, append this line
                    congrats_lines[-1]["text"] = congrats_lines[-1]["text"][:-1] + "\n" + line
                else:
                    # Add regular text line with current properties
                    congrats_lines.append({
                        "text": line,
                        "delay": current_delay,
                        "pause": current_pause,
                        "font_size": current_font_size,
                        "color": current_color
                    })
        
        return congrats_lines
    
    except Exception as e:
        print(f"Error loading congrats text: {e}")
        # Return default congratulatory text
        return [
            {"text": "Congratulations, Detective!", "delay": 0.05, "pause": 1.0, "font_size": 36, "color": (255, 255, 255)},
            {"text": "You've successfully solved the case.", "delay": 0.05, "pause": 0.5, "font_size": 32, "color": (200, 200, 200)},
            {"text": "Lisa has been arrested for the murder.", "delay": 0.05, "pause": 0.5, "font_size": 32, "color": (200, 200, 200)},
            {"text": "Justice has been served.", "delay": 0.05, "pause": 1.0, "font_size": 32, "color": (200, 200, 200)},
            {"text": "Press any key to return to the menu.", "delay": 0.05, "pause": 0.0, "font_size": 24, "color": (150, 150, 150)}
        ]
