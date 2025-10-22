"""
SRT to JSON Converter Node
Converts SRT subtitle format to structured JSON for easy parsing
"""

import json
import re

class SRTToJson:
    """
    A ComfyUI node that converts SRT subtitle text to structured JSON format.
    Makes it easy to parse timestamps and text separately.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "srt_text": ("STRING", {"forceInput": True}),
                "output_format": (["array", "object_by_index", "flat_list"], {
                    "default": "array"
                }),
            },
            "optional": {
                "include_timestamps_ms": ("BOOLEAN", {"default": False}),
                "pretty_print": ("BOOLEAN", {"default": True}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("json_output",)
    FUNCTION = "convert_srt_to_json"
    CATEGORY = "utils/text"
    OUTPUT_NODE = False
    
    def parse_timestamp_to_ms(self, timestamp):
        """Convert SRT timestamp to milliseconds"""
        # Format: HH:MM:SS,mmm
        time_parts = timestamp.split(':')
        hours = int(time_parts[0])
        minutes = int(time_parts[1])
        seconds_parts = time_parts[2].split(',')
        seconds = int(seconds_parts[0])
        milliseconds = int(seconds_parts[1])
        
        total_ms = (hours * 3600 + minutes * 60 + seconds) * 1000 + milliseconds
        return total_ms
    
    def convert_srt_to_json(self, srt_text, output_format, include_timestamps_ms=False, pretty_print=True):
        """
        Convert SRT text to JSON format
        
        Args:
            srt_text: SRT subtitle text input
            output_format: How to structure the JSON output
            include_timestamps_ms: Whether to include millisecond timestamps
            pretty_print: Whether to format JSON with indentation
            
        Returns:
            tuple: (json_string,)
        """
        try:
            # Split SRT text into blocks (separated by double newlines)
            blocks = [block.strip() for block in srt_text.split('\n\n') if block.strip()]
            
            subtitles = []
            
            for block in blocks:
                lines = [line.strip() for line in block.split('\n') if line.strip()]
                
                if len(lines) < 3:
                    continue  # Skip incomplete blocks
                
                # Parse each block
                try:
                    index = int(lines[0])
                    
                    # Parse timestamp line (format: start --> end)
                    timestamp_match = re.match(r'(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})', lines[1])
                    if not timestamp_match:
                        continue
                    
                    start_time = timestamp_match.group(1)
                    end_time = timestamp_match.group(2)
                    
                    # Join remaining lines as text (subtitle can be multi-line)
                    text = '\n'.join(lines[2:])
                    
                    subtitle_entry = {
                        "index": index,
                        "start_time": start_time,
                        "end_time": end_time,
                        "text": text
                    }
                    
                    # Add millisecond timestamps if requested
                    if include_timestamps_ms:
                        subtitle_entry["start_ms"] = self.parse_timestamp_to_ms(start_time)
                        subtitle_entry["end_ms"] = self.parse_timestamp_to_ms(end_time)
                        subtitle_entry["duration_ms"] = subtitle_entry["end_ms"] - subtitle_entry["start_ms"]
                    
                    subtitles.append(subtitle_entry)
                    
                except (ValueError, IndexError):
                    # Skip malformed blocks
                    continue
            
            # Format output based on selected format
            if output_format == "array":
                json_data = subtitles
                
            elif output_format == "object_by_index":
                # Create object with index as key
                json_data = {str(sub["index"]): sub for sub in subtitles}
                
            elif output_format == "flat_list":
                # Flatten to simple list of text with timestamps
                json_data = []
                for sub in subtitles:
                    json_data.append({
                        "time_range": f"{sub['start_time']} --> {sub['end_time']}",
                        "text": sub["text"]
                    })
            
            # Add metadata
            if output_format == "array":
                result = {
                    "subtitles": json_data,
                    "metadata": {
                        "total_count": len(subtitles),
                        "total_duration": f"{subtitles[-1]['end_time']}" if subtitles else "00:00:00,000",
                        "format": "srt_converted"
                    }
                }
            else:
                result = json_data
            
            # Convert to JSON string
            if pretty_print:
                json_output = json.dumps(result, indent=2, ensure_ascii=False)
            else:
                json_output = json.dumps(result, ensure_ascii=False)
            
            return (json_output,)
            
        except Exception as e:
            # Return error as JSON
            error_output = json.dumps({
                "error": "SRT conversion failed",
                "message": str(e),
                "original_text": srt_text[:500] + "..." if len(srt_text) > 500 else srt_text
            }, indent=2 if pretty_print else None)
            
            return (error_output,)

# Required for ComfyUI to recognize the node
NODE_CLASS_MAPPINGS = {
    "SRTToJson": SRTToJson
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SRTToJson": "SRT to JSON Converter"
}