"""
Save JSON Node
Saves JSON text to output/transcriptions folder with timestamped filenames
"""

import json as json_module
import os
from datetime import datetime

class SaveJSON:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "json": ("STRING", {"forceInput": True}),
                "filename_prefix": ("STRING", {"default": "transcription"}),
                "filename_delimiter": ("STRING", {"default": "_"}),
                "filename_number_padding": ("INT", {"default": 4, "min": 0, "max": 9, "step": 1}),
            },
            "optional": {
                "validate_json": ("BOOLEAN", {"default": True}),
            }
        }

    OUTPUT_NODE = True
    RETURN_TYPES = ()
    FUNCTION = "save_json_file"
    CATEGORY = "utils/text"

    def save_json_file(self, json, filename_prefix="transcription", filename_delimiter="_", 
                       filename_number_padding=4, validate_json=True):
        
        # Create transcriptions directory if it doesn't exist
        output_dir = os.path.join("output", "transcriptions")
        if not os.path.exists(output_dir):
            print(f"Creating directory: {output_dir}")
            try:
                os.makedirs(output_dir, exist_ok=True)
            except OSError as e:
                print(f"Could not create directory {output_dir}: {e}")
                return ()

        if json.strip() == '':
            print("No JSON specified to save! JSON is empty.")
            return ()

        # Validate JSON if requested
        if validate_json:
            try:
                json_module.loads(json)
            except json_module.JSONDecodeError as e:
                print(f"Warning: Invalid JSON detected: {e}")

        # Generate timestamped filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename_prefix}{filename_delimiter}{timestamp}.json"
        filepath = os.path.join(output_dir, filename)

        # Save the file
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(json)
            print(f"JSON saved to: {filepath}")
        except Exception as e:
            print(f"Error saving JSON file: {e}")

        return ()

# Required for ComfyUI to recognize the node
NODE_CLASS_MAPPINGS = {
    "SaveJSON": SaveJSON
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveJSON": "Save JSON File"
}