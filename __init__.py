"""
Atlantis JSON Nodes
Custom ComfyUI nodes for JSON processing and transcription workflows
"""

from .text_to_json_input import NODE_CLASS_MAPPINGS as text_to_json_mappings, NODE_DISPLAY_NAME_MAPPINGS as text_to_json_display
from .srt_to_json import NODE_CLASS_MAPPINGS as srt_to_json_mappings, NODE_DISPLAY_NAME_MAPPINGS as srt_to_json_display
from .save_json import NODE_CLASS_MAPPINGS as save_json_mappings, NODE_DISPLAY_NAME_MAPPINGS as save_json_display

# Combine all node mappings
NODE_CLASS_MAPPINGS = {}
NODE_CLASS_MAPPINGS.update(text_to_json_mappings)
NODE_CLASS_MAPPINGS.update(srt_to_json_mappings)
NODE_CLASS_MAPPINGS.update(save_json_mappings)

# Combine all display name mappings
NODE_DISPLAY_NAME_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS.update(text_to_json_display)
NODE_DISPLAY_NAME_MAPPINGS.update(srt_to_json_display)
NODE_DISPLAY_NAME_MAPPINGS.update(save_json_display)

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']