
import re

def convert_to_script_lines(conversation_text):
    """
    Converts a conversation text into a list of tuples in the format:
    script_lines = [(speaker, dialogue), ...]
    """
    # Split the text into lines and remove empty lines
    lines = [line.strip() for line in conversation_text.split("\n") if line.strip()]
    
    # Regex to match the speaker and dialogue
    pattern = r"^(.*?):\s*\((.*?)\)\s*(.*)$"
    
    script_lines = []
    for line in lines:
        match = re.match(pattern, line)
        if match:
            speaker = match.group(1).strip()
            dialogue = match.group(3).strip()
            script_lines.append((speaker, dialogue))
    
    return script_lines

def fix_encoding(text):
    """
    Fixes text that has been misinterpreted due to encoding issues.
    Converts characters like â€™ into proper UTF-8 characters.
    """
    return text.encode('latin1').decode('utf-8')