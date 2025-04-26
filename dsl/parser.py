import yaml
import os

class Scene:
    def __init__(self, data):
        self.background = data.get('background', '')
        self.characters = data.get('characters', [])
        self.dialogue = data.get('dialogue', [])
        self.evidence = data.get('evidence', [])
        self.next_scene = data.get('next_scene', None)

class Evidence:
    def __init__(self, data):
        self.id = data.get('id', '')
        self.name = data.get('name', '')
        self.description = data.get('description', '')
        self.image = data.get('image', '')
        self.relevant = data.get('relevant', True)

class Character:
    def __init__(self, data):
        self.id = data.get('id', '')
        self.name = data.get('name', '')
        self.image = data.get('image', '')
        self.position = data.get('position', (0, 0))
        self.dialogue = data.get('dialogue', {})

def load_scene(scene_name):
    """Load a scene from the YAML file"""
    try:
        scene_path = os.path.join('assets', 'data', 'scenes', f'{scene_name}.yaml')
        with open(scene_path, 'r') as file:
            scene_data = yaml.safe_load(file)
            return Scene(scene_data)
    except Exception as e:
        print(f"Error loading scene {scene_name}: {e}")
        return None

def load_evidence(evidence_id):
    """Load evidence data from YAML file"""
    try:
        evidence_path = os.path.join('assets', 'data', 'evidence', f'{evidence_id}.yaml')
        with open(evidence_path, 'r') as file:
            evidence_data = yaml.safe_load(file)
            return Evidence(evidence_data)
    except Exception as e:
        print(f"Error loading evidence {evidence_id}: {e}")
        return None

def load_character(character_id):
    """Load character data from YAML file"""
    try:
        character_path = os.path.join('assets', 'data', 'characters', f'{character_id}.yaml')
        with open(character_path, 'r') as file:
            character_data = yaml.safe_load(file)
            return Character(character_data)
    except Exception as e:
        print(f"Error loading character {character_id}: {e}")
        return None 