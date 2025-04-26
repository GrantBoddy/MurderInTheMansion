import os
import re

def load_suspense_text(file_path):
    """
    Load suspense text from a file.
    
    Format:
    #FONT:[size] - Set font size for following lines
    [time_to_appear_seconds]|[x_position_percent]|[y_position_percent]|[text]|[color_rgb]
    
    Returns a list of suspense text entries.
    """
    suspense_lines = []
    current_font_size = 28  # Default font size
    
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Strip whitespace
                line = line.strip()
                
                # Skip empty lines
                if not line:
                    continue
                
                # Check for font size directive
                font_match = re.match(r'#FONT:(\d+)', line)
                if font_match:
                    current_font_size = int(font_match.group(1))
                    continue
                
                # Skip other comments
                if line.startswith('#'):
                    continue
                
                # Parse the line
                parts = line.split('|')
                if len(parts) != 5:
                    print(f"Warning: Invalid suspense text format: {line}")
                    continue
                
                try:
                    time_to_appear = float(parts[0])
                    x_position = float(parts[1]) / 100.0  # Convert percentage to decimal
                    y_position = float(parts[2]) / 100.0  # Convert percentage to decimal
                    text = parts[3]
                    
                    # Parse color
                    color_parts = parts[4].split(',')
                    if len(color_parts) != 3:
                        print(f"Warning: Invalid color format: {parts[4]}")
                        color = (255, 255, 255)  # Default to white
                    else:
                        color = (int(color_parts[0]), int(color_parts[1]), int(color_parts[2]))
                    
                    suspense_lines.append({
                        'time': time_to_appear,
                        'x_pos': x_position,
                        'y_pos': y_position,
                        'text': text,
                        'color': color,
                        'font_size': current_font_size,  # Store the current font size
                        'current_text': '',  # For typewriter effect
                        'visible': False,    # Whether this line should be visible yet
                        'complete': False,   # Whether typewriter effect is complete
                        'complete_time': 0,  # When the typewriter effect completed
                        'fade_start_time': 0,  # When to start fading out
                        'fade_duration': 2.0,  # How long the fade takes
                        'alpha': 255  # Current alpha value for fading
                    })
                    
                except ValueError as e:
                    print(f"Warning: Error parsing suspense text: {line}, {e}")
                    continue
                    
            # Sort by time to appear
            suspense_lines.sort(key=lambda x: x['time'])
            
    except Exception as e:
        print(f"Error loading suspense text: {e}")
        
    return suspense_lines

def get_default_suspense_text_path():
    """Get the default path to the suspense text file"""
    return os.path.join('assets', 'suspense', 'suspense_text.txt')
