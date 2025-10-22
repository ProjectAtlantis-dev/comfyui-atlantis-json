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
                return {"ui": {"images": []}}

        if json.strip() == '':
            print("No JSON specified to save! JSON is empty.")
            return {"ui": {"images": []}}

        # Validate JSON if requested
        if validate_json:
            try:
                json_module.loads(json)
            except json_module.JSONDecodeError as e:
                print(f"Warning: Invalid JSON detected: {e}")

        # Generate filename with counter
        filename = self.generate_filename(output_dir, filename_prefix, filename_delimiter, filename_number_padding)
        filepath = os.path.join(output_dir, filename)

        # Save the file
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(json)
            print(f"JSON saved to: {filepath}")
            
            # Return UI data following SaveImage pattern - ALL files use "images" key
            results = [{
                "filename": filename,
                "subfolder": "transcriptions",
                "type": "output"
            }]
            
            return {"ui": {"images": results}}
            
        except Exception as e:
            error_msg = f"Error saving JSON file: {e}"
            print(error_msg)
            return {"ui": {"images": []}}

    def generate_filename(self, path, prefix, delimiter, number_padding):
        """Generate filename with automatic numbering"""
        extension = ".json"
        
        if number_padding == 0:
            filename = f"{prefix}{extension}"
        else:
            # Look for existing files with the same pattern
            import re
            if delimiter:
                pattern = f"{re.escape(prefix)}{re.escape(delimiter)}(\\d{{{number_padding}}}){re.escape(extension)}"
            else:
                pattern = f"{re.escape(prefix)}(\\d{{{number_padding}}}){re.escape(extension)}"

            existing_counters = []
            if os.path.exists(path):
                for filename in os.listdir(path):
                    match = re.match(pattern, filename)
                    if match and filename.endswith(extension):
                        existing_counters.append(int(match.group(1)))
            
            existing_counters.sort()
            counter = existing_counters[-1] + 1 if existing_counters else 1
            
            if delimiter:
                filename = f"{prefix}{delimiter}{counter:0{number_padding}}{extension}"
            else:
                filename = f"{prefix}{counter:0{number_padding}}{extension}"
        
        return filename

# Required for ComfyUI to recognize the node
NODE_CLASS_MAPPINGS = {
    "SaveJSON": SaveJSON
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveJSON": "Save JSON File"
}