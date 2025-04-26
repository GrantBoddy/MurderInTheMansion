import os

class IntroSequence:
    """Class to represent a parsed intro sequence"""
    def __init__(self):
        self.lines = []  # List of intro text lines with their properties
        
    def add_line(self, delay, text, font_size='medium', color=(255, 255, 255)):
        """Add a line to the intro sequence"""
        self.lines.append({
            'delay': delay,
            'text': text,
            'font_size': font_size,
            'color': color
        })
        
    def get_lines(self):
        """Get all lines in the sequence"""
        return self.lines

def parse_intro_sequence(file_path):
    """Parse an intro sequence file and return an IntroSequence object"""
    sequence = IntroSequence()
    
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Skip comments and empty lines
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Parse the line
                parts = line.split('|')
                
                # Basic validation
                if len(parts) < 2:
                    print(f"Warning: Invalid line format in intro sequence: {line}")
                    continue
                
                # Extract delay and text (required)
                try:
                    delay = float(parts[0])
                    text = parts[1]
                except ValueError:
                    print(f"Warning: Invalid delay value in intro sequence: {parts[0]}")
                    continue
                
                # Extract font size (optional)
                font_size = 'medium'  # Default
                if len(parts) > 2 and parts[2]:
                    font_size = parts[2]
                
                # Extract color (optional)
                color = (255, 255, 255)  # Default: white
                if len(parts) > 3 and parts[3]:
                    try:
                        rgb = parts[3].split(',')
                        if len(rgb) == 3:
                            color = (int(rgb[0]), int(rgb[1]), int(rgb[2]))
                    except ValueError:
                        print(f"Warning: Invalid color format in intro sequence: {parts[3]}")
                
                # Add the parsed line to the sequence
                sequence.add_line(delay, text, font_size, color)
                
        return sequence
    except Exception as e:
        print(f"Error parsing intro sequence file: {e}")
        return sequence  # Return empty sequence on error

def load_intro_sequence():
    """Load the intro sequence from the default file"""
    file_path = os.path.join('assets', 'intro', 'intro_sequence.txt')
    return parse_intro_sequence(file_path)
