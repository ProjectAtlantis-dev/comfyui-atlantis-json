# Atlantis JSON Nodes

Custom ComfyUI nodes for JSON processing and transcription workflows.

## Nodes Included

### Text to JSON (with Input)
- **Category**: utils/text
- **Function**: Converts plain text into structured JSON format
- **Input**: Text (from other nodes)
- **Output**: JSON string
- **Formats**: simple, lines_array, key_value, structured

### SRT to JSON Converter  
- **Category**: utils/text
- **Function**: Converts SRT subtitle format to structured JSON
- **Input**: SRT text (from WhisperSRT or other nodes)
- **Output**: JSON string with timestamps and text separated
- **Formats**: array, object_by_index, flat_list

### Save JSON File
- **Category**: utils/text  
- **Function**: Saves JSON data to output/transcriptions folder
- **Input**: JSON string (from converter nodes)
- **Output**: File saved to ComfyUI/output/transcriptions/
- **Features**: Timestamped filenames, JSON validation

## Usage

1. Use WhisperSRT to transcribe audio
2. Connect SRT output to "SRT to JSON Converter" 
3. Connect JSON output to "Save JSON File"
4. Run workflow to save structured JSON transcriptions

## Installation

### Via ComfyUI Manager (Recommended)
1. Open ComfyUI Manager
2. Search for "Atlantis JSON Nodes"
3. Click Install

### Manual Installation
1. Navigate to your ComfyUI custom_nodes directory
2. Clone this repository:
```bash
git clone https://github.com/YOUR_USERNAME/atlantis-json-nodes.git
```
3. Restart ComfyUI

## Requirements

- ComfyUI
- Python 3.8+

## License

MIT License