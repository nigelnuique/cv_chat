# CV Chat - AI-Powered CV Editor

A Python-based CV editor that uses AI to help you create and edit professional CVs in YAML format, with real-time rendering capabilities.

## Features

- **AI-Powered Editing**: Chat with AI to edit your CV content
- **YAML Format**: Clean, structured CV data format
- **Multiple Output Formats**: Generate PDF, HTML, Markdown, and PNG versions
- **Real-time Preview**: See changes instantly as you edit
- **Simple Interface**: Easy-to-use command-line interface

## Prerequisites

- Python 3.7+
- OpenAI API key (for AI features)
- rendercv (for CV rendering)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/nigelnuique/cv_chat.git
cd cv_chat
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
```bash
python setup_ai_editor.py
```

Or manually set the environment variable:
```bash
# Windows
set OPENAI_API_KEY=your_api_key_here

# Linux/Mac
export OPENAI_API_KEY=your_api_key_here

# Windows PowerShell
$env:OPENAI_API_KEY="your_api_key_here"
```

## Usage

### Simple Editor
Run the simple YAML editor:
```bash
python simple_yaml_editor.py
```

### AI Setup
Set up AI features:
```bash
python setup_ai_editor.py
```

### Quick Start
Use the batch file (Windows):
```bash
start_simple_editor.bat
```

## Project Structure

```
cv_chat/
├── simple_yaml_editor.py    # Main editor application
├── setup_ai_editor.py       # AI setup utility
├── requirements.txt         # Python dependencies
├── working_CV.yaml         # Example CV template
├── utils/                  # Utility functions
├── rendercv_output/        # Generated CV outputs
└── temp_renders/          # Temporary render directories
```

## Features

### AI Chat Integration
- Chat with AI to edit CV content
- Natural language editing commands
- Context-aware suggestions

### CV Rendering
- Multiple output formats (PDF, HTML, Markdown, PNG)
- Professional templates
- Real-time preview

### YAML Structure
- Clean, readable CV format
- Easy to edit and maintain
- Version control friendly

## Known Issues

- **Chat Editing**: AI chat editing functionality is currently not working properly
- Some features may require additional setup

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions, please open an issue on GitHub. 