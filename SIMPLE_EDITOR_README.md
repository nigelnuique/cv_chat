# AI-Powered YAML CV Editor

> 🤖 A smart, 3-panel editor for RenderCV YAML files with AI assistant, live YAML editing, and real-time PDF preview.

[![Flask](https://img.shields.io/badge/Flask-2.3+-blue.svg)](https://flask.palletsprojects.com/)
[![RenderCV](https://img.shields.io/badge/RenderCV-Compatible-orange.svg)](https://rendercv.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-green.svg)](https://openai.com/)
[![Real-time](https://img.shields.io/badge/Preview-Real--time-green.svg)]()

## Overview

The AI-Powered YAML CV Editor provides an intelligent, 3-panel interface for editing your resume YAML files. It features an AI assistant that can help improve your CV content, answer questions about resume writing, and directly modify your YAML content based on your requests.

## Key Features

### 🤖 **AI Assistant Panel**
- **Left Panel**: Chat interface with OpenAI GPT-4o-mini
- **Smart CV Help**: Ask questions about resume writing and formatting
- **Direct YAML Editing**: AI can modify your CV content directly
- **Real-time Suggestions**: Get instant feedback on your CV improvements

### 🖥️ **3-Panel Interface**
- **Left Panel**: AI chat assistant for CV help and modifications
- **Middle Panel**: YAML editor with full syntax highlighting  
- **Right Panel**: Live PDF preview that updates as you type
- **Clean Design**: Streamlined interface optimized for productivity

### ⚡ **Real-Time Updates**
- **Auto-save**: Saves changes automatically after 1.5 seconds of inactivity
- **Instant Rendering**: PDF regenerates immediately using RenderCV
- **Live Preview**: See your changes reflected in real-time
- **Chat Memory**: AI remembers your conversation throughout the session

### 🎨 **Modern Experience**
- **Dark Theme**: Comfortable editing for extended sessions
- **Syntax Highlighting**: Full YAML syntax support with color coding
- **Status Indicators**: Clear feedback on rendering progress and errors
- **Responsive Design**: Optimized layout for different screen sizes

## Quick Start

### Prerequisites
- Python 3.7+
- OpenAI API Key (for AI features)

### Option 1: Auto-Setup Script
```bash
python start_simple_editor.py
```

### Option 2: Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key
export OPENAI_API_KEY=your_api_key_here  # Linux/Mac
# or
set OPENAI_API_KEY=your_api_key_here     # Windows CMD
# or
$env:OPENAI_API_KEY="your_api_key_here"  # Windows PowerShell

# Start the editor
python simple_yaml_editor.py
```

### Option 3: Double-Click Launch (Windows)
```bash
start_simple_editor.bat
```

**Access URL**: `http://localhost:5000`

## Installation & Setup

### Getting an OpenAI API Key
1. Visit [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Create a new account or sign in
3. Click "Create new secret key"
4. Copy your API key
5. Set it as an environment variable (see above)

### Automatic Setup
The startup scripts will automatically:
- ✅ Check for required dependencies
- ✅ Install missing packages if needed
- ✅ Create a sample CV if `working_CV.yaml` doesn't exist
- ✅ Launch your default browser
- ✅ Start the Flask development server
- ⚠️ **Note**: You still need to set your OpenAI API key manually

### Manual Setup
```bash
# Install dependencies
pip install flask pyyaml "rendercv[full]" openai

# Set OpenAI API key
export OPENAI_API_KEY=your_api_key_here

# Create initial CV file (optional)
cp master_CV_template.yaml working_CV.yaml

# Start editor
python simple_yaml_editor.py
```

## How It Works

### Workflow
1. **Start Editor** → Automatically opens browser at `http://localhost:5000`
2. **Chat with AI** → Ask for CV help or request modifications in left panel
3. **Edit YAML** → Type in middle panel with syntax highlighting
4. **AI Modifications** → AI can directly update your YAML content
5. **Auto-Save** → Changes saved to `working_CV.yaml` after 1.5s pause
6. **Live Preview** → PDF updates automatically in right panel
7. **Download** → Access final PDF from the preview panel

### AI Assistant Capabilities
- **CV Writing Help**: Get advice on resume structure, content, and formatting
- **Content Improvement**: Ask for suggestions to enhance specific sections
- **Direct Editing**: Request specific changes and the AI will modify your YAML
- **Industry Guidance**: Get tailored advice for your field or target roles
- **Error Fixing**: Help resolve YAML syntax errors or RenderCV issues

### File Management
- **Working File**: `working_CV.yaml` (auto-created if missing)
- **Temp Renders**: `temp_renders/` directory (auto-cleaned)
- **Auto-Save**: Every 1.5 seconds after typing stops
- **Chat History**: Stored in memory during session (resets on restart)

## Sample CV Generation

If `working_CV.yaml` doesn't exist, the editor creates a comprehensive sample CV featuring:

### Professional Template
- **Software Engineer Profile**: Complete with modern tech stack
- **Industry-Standard Sections**: Experience, education, skills, projects
- **RenderCV Theme**: Uses `engineeringresumes` theme for professional appearance
- **Proper Structure**: Valid YAML formatting with all required fields
- **AI-Ready**: Includes helpful comments for AI interaction

### Sample Content
- **Work Experience**: Multiple realistic software engineering roles
- **Technical Skills**: Modern programming languages and frameworks
- **Projects**: Portfolio-worthy projects with descriptions
- **Education**: Computer science degree with relevant coursework
- **Contact Information**: Placeholder data ready for customization

## AI Chat Examples

### Getting Help
```
"Can you help me improve the summary section of my CV?"
"What are the best practices for listing technical skills?"
"How should I format my work experience for a senior role?"
```

### Direct Modifications
```
"Add a new skill section for cloud technologies including AWS and Docker"
"Update my job title to Senior Software Engineer"
"Rewrite my summary to focus more on leadership experience"
"Add a new project about machine learning"
```

### Content Improvement
```
"Make my bullet points more impactful and quantified"
"Improve the descriptions in my experience section"
"Help me tailor this CV for a data science position"
```

## Advanced Features

### Editor Capabilities
- **Full YAML Support**: Complete syntax highlighting and validation
- **Error Detection**: Highlights YAML formatting issues
- **Auto-Indentation**: Maintains proper YAML structure
- **Find/Replace**: Standard text editor functionality
- **Real-time Validation**: Immediate feedback on YAML syntax

### AI Features
- **Context Awareness**: AI sees your current YAML content
- **Smart Modifications**: Preserves formatting and structure
- **Multiple Providers**: Easy to switch between AI providers
- **Error Handling**: Graceful handling of AI service issues
- **Conversation Memory**: Maintains context throughout session

### Rendering Features
- **Multiple Formats**: PDF primary, with HTML/PNG support via RenderCV
- **Theme Support**: Compatible with all RenderCV themes
- **Error Handling**: Graceful handling of rendering failures
- **Performance**: Optimized for fast preview updates

## Troubleshooting

### Common Issues

**AI Not Working**
```bash
# Check if OpenAI package is installed
pip install openai

# Verify API key is set
echo $OPENAI_API_KEY  # Linux/Mac
echo %OPENAI_API_KEY%  # Windows CMD
echo $env:OPENAI_API_KEY  # Windows PowerShell

# Check if API key is valid by testing a simple request
```

**Port 5000 Already in Use**
```bash
# Edit simple_yaml_editor.py, change the last line:
app.run(debug=True, host='0.0.0.0', port=5001)  # Use different port
```

**RenderCV Not Found**
```bash
# Install full RenderCV package
pip install "rendercv[full]"

# Verify installation
python -m rendercv --version
```

**Browser Doesn't Open**
```bash
# Manually navigate to:
http://localhost:5000

# Or try different port if changed:
http://localhost:5001
```

**YAML Syntax Errors**
- Check indentation (use spaces, not tabs)
- Ensure proper YAML structure
- Look for unescaped special characters
- Validate required fields are present
- Ask the AI assistant for help fixing errors!

**PDF Not Updating**
- Check browser console for errors
- Verify `working_CV.yaml` is being saved
- Ensure RenderCV can process the YAML
- Check `temp_renders/` directory for error files

### Debug Mode

Enable detailed logging:
```bash
# Run with debug output
python simple_yaml_editor.py --debug

# Check Flask logs in terminal
# Monitor temp_renders/ directory for render attempts
# Check browser console for JavaScript errors
```

## Configuration

### AI Configuration
```python
# Edit simple_yaml_editor.py to change AI provider
# Currently supports OpenAI, easily extensible to other providers

# Change model
model="gpt-4o-mini"  # or gpt-4, gpt-3.5-turbo, etc.

# Adjust creativity
temperature=0.3  # Lower = more focused, Higher = more creative
```

### Port Configuration
```python
# Edit simple_yaml_editor.py
app.run(debug=True, host='0.0.0.0', port=5000)  # Change port here
```

### Auto-Save Timing
```javascript
// Edit the JavaScript in simple_yaml_editor.py template
let saveTimeout;
const SAVE_DELAY = 1500;  # Change delay in milliseconds
```

### Theme Selection
```yaml
# In your YAML file, change the theme:
design:
  theme: engineeringresumes  # or sb2nov, classic, etc.
```

## Privacy & Security

- **Local Processing**: YAML editing and PDF rendering happen locally
- **AI Privacy**: Only the YAML content and your messages are sent to OpenAI
- **No Data Storage**: Chat history is not permanently stored
- **API Key Security**: Keep your OpenAI API key secure and never share it
- **Network**: The app runs locally on your machine

## Contributing

Feel free to contribute improvements:
- Add support for other AI providers (Anthropic, Cohere, etc.)
- Improve the chat interface
- Add more CV writing features
- Enhance error handling
- Add tests

## Dependencies

- **Flask**: Web framework for the interface
- **PyYAML**: YAML parsing and validation
- **RenderCV**: CV rendering engine
- **OpenAI**: AI assistant functionality
- **CodeMirror**: Enhanced text editing with syntax highlighting

---

**Happy CV editing! 🚀** 
