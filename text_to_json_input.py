"""
Text to JSON Node with Text Input
Converts plain text into JSON format with configurable structure
"""

import json
import re

class TextToJsonInput:
    """
    A ComfyUI node that converts plain text input into JSON format.
    Takes regular text and structures it as JSON.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
                "format_type": (["simple", "lines_array", "key_value", "structured"], {
                    "default": "simple"
                }),
            },
            "optional": {
                "key_name": ("STRING", {"default": "text"}),
                "pretty_print": ("BOOLEAN", {"default": True}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("json_output",)
    FUNCTION = "convert_text_to_json"
    CATEGORY = "utils/text"
    OUTPUT_NODE = False
    
    def convert_text_to_json(self, text, format_type, key_name="text", pretty_print=True):
        """
        Convert plain text input to JSON format
        
        Args:
            text: Plain text input
            format_type: How to structure the JSON
            key_name: Key name for simple format
            pretty_print: Whether to format JSON with indentation
            
        Returns:
            tuple: (json_string,)
        """
        try:
            if format_type == "simple":
                # Simple format: {"text": "content"}
                json_data = {key_name: text}
                
            elif format_type == "lines_array":
                # Split text into lines and create array
                lines = [line.strip() for line in text.split('\n') if line.strip()]
                json_data = {"lines": lines}
                
            elif format_type == "key_value":
                # Try to parse key:value or key=value pairs
                lines = [line.strip() for line in text.split('\n') if line.strip()]
                json_data = {}
                
                for line in lines:
                    # Try different separators
                    if ':' in line:
                        key, value = line.split(':', 1)
                        json_data[key.strip()] = value.strip()
                    elif '=' in line:
                        key, value = line.split('=', 1)
                        json_data[key.strip()] = value.strip()
                    else:
                        # If no separator, use line number as key
                        json_data[f"line_{len(json_data) + 1}"] = line
                        
            elif format_type == "structured":
                # More advanced structure with metadata
                lines = [line.strip() for line in text.split('\n') if line.strip()]
                word_count = len(text.split())
                char_count = len(text)
                
                json_data = {
                    "content": text,
                    "lines": lines,
                    "metadata": {
                        "line_count": len(lines),
                        "word_count": word_count,
                        "character_count": char_count,
                        "has_numbers": bool(re.search(r'\d', text)),
                        "has_special_chars": bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', text))
                    }
                }
            
            # Convert to JSON string
            if pretty_print:
                json_output = json.dumps(json_data, indent=2, ensure_ascii=False)
            else:
                json_output = json.dumps(json_data, ensure_ascii=False)
            
            return (json_output,)
            
        except Exception as e:
            # Return error as JSON
            error_output = json.dumps({
                "error": "Conversion failed",
                "message": str(e),
                "original_text": text
            }, indent=2 if pretty_print else None)
            
            return (error_output,)

# Required for ComfyUI to recognize the node
NODE_CLASS_MAPPINGS = {
    "TextToJsonInput": TextToJsonInput
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TextToJsonInput": "Text to JSON (with Input)"
}