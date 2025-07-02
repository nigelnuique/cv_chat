#!/usr/bin/env python3
"""
3-Panel YAML CV Editor with AI Chat and Cursor-Style Suggestions
Left: AI Chat interface with suggestion management
Middle: YAML editor with syntax highlighting and diff highlighting
Right: Fast PDF preview using RenderCV
"""

import os
import yaml
import subprocess
import tempfile
import shutil
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template_string, request, jsonify, send_file
import json
import uuid
import difflib
from concurrent.futures import ThreadPoolExecutor

# AI Integration - you can switch between different providers
try:
    import openai
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    print("⚠️  OpenAI not installed. Install with: pip install openai")

app = Flask(__name__)

class ChatManager:
    def __init__(self):
        self.messages = []
        self.openai_client = None
        self.pending_suggestions = {}  # Store pending suggestions
        self.setup_ai()
    
    def setup_ai(self):
        """Setup AI client - you can modify this for different providers."""
        if AI_AVAILABLE:
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key:
                self.openai_client = openai.OpenAI(api_key=api_key)
            else:
                print("⚠️  OPENAI_API_KEY not found in environment variables")
                print("   Set it with: export OPENAI_API_KEY=your_key_here")
    
    def add_message(self, role, content, yaml_content=None, suggestion_id=None):
        """Add a message to the chat history."""
        message = {
            "id": str(uuid.uuid4()),
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "yaml_content": yaml_content,
            "suggestion_id": suggestion_id
        }
        self.messages.append(message)
        return message
    
    def get_chat_history(self):
        """Get the chat history."""
        return self.messages
    
    def create_suggestion(self, original_yaml, suggested_yaml, explanation):
        """Create a new suggestion with diff information."""
        suggestion_id = str(uuid.uuid4())
        
        print(f"DEBUG: Creating suggestion with ID: {suggestion_id}")
        print(f"DEBUG: Original YAML length: {len(original_yaml)}")
        print(f"DEBUG: Suggested YAML length: {len(suggested_yaml)}")
        print(f"DEBUG: Explanation: {explanation}")
        
        # Ensure suggested_yaml is a string
        if isinstance(suggested_yaml, dict):
            import yaml
            suggested_yaml = yaml.dump(suggested_yaml, default_flow_style=False, sort_keys=False)
            print(f"DEBUG: Converted dict to YAML string, length: {len(suggested_yaml)}")
        
        # Generate diff
        original_lines = original_yaml.splitlines(keepends=True)
        suggested_lines = suggested_yaml.splitlines(keepends=True)
        
        diff = list(difflib.unified_diff(
            original_lines, 
            suggested_lines, 
            fromfile='current', 
            tofile='suggested',
            lineterm=''
        ))
        
        suggestion = {
            "id": suggestion_id,
            "original_yaml": original_yaml,
            "suggested_yaml": suggested_yaml,
            "explanation": explanation,
            "diff": diff,
            "created_at": datetime.now().isoformat(),
            "status": "pending"  # pending, accepted, declined
        }
        
        self.pending_suggestions[suggestion_id] = suggestion
        print(f"DEBUG: Suggestion created and stored. Total suggestions: {len(self.pending_suggestions)}")
        return suggestion
    
    def get_suggestion(self, suggestion_id):
        """Get a specific suggestion."""
        return self.pending_suggestions.get(suggestion_id)
    
    def accept_suggestion(self, suggestion_id):
        """Accept a suggestion."""
        suggestion = self.pending_suggestions.get(suggestion_id)
        if suggestion:
            suggestion["status"] = "accepted"
            return suggestion["suggested_yaml"]
        return None
    
    def decline_suggestion(self, suggestion_id):
        """Decline a suggestion."""
        suggestion = self.pending_suggestions.get(suggestion_id)
        if suggestion:
            suggestion["status"] = "declined"
        return suggestion
    
    async def get_ai_response(self, user_message, current_yaml):
        """Get AI response and potentially modify YAML."""
        if not self.openai_client:
            return {
                "chat_response": "AI is not available. Please set your OPENAI_API_KEY environment variable.",
                "yaml_changes": None,
                "suggestion": None
            }
        
        # Prepare the system prompt
        system_prompt = """You are an AI assistant helping with CV/resume editing. You can:
1. Answer questions about CV writing and formatting
2. Suggest improvements to the CV content  
3. Provide suggestions for YAML modifications

IMPORTANT RULES:
- For general questions, advice, or explanations: Set yaml_changes to null and provide helpful text in chat_response
- For actual CV modifications: Provide the complete modified YAML in yaml_changes field
- NEVER paste the current YAML in chat_response - only provide explanations and advice there
- When making changes, always use the yaml_changes field, not the chat_response field
- CRITICAL: The yaml_changes field must be a YAML string, not a JSON object

The CV uses RenderCV format. Here's the current YAML:

```yaml
{current_yaml}
```

Respond in JSON format:
{{
    "chat_response": "Your explanation, advice, or response (DO NOT include YAML here)",
    "yaml_changes": "Complete modified YAML content as a string (only if making actual changes, otherwise null)",
    "explanation": "Detailed explanation of the changes you're suggesting"
}}

EXAMPLES:
- User asks "How do I improve my CV?": Set yaml_changes to null, provide advice in chat_response
- User asks "Add a new skill": Set yaml_changes to the complete modified YAML string with the new skill added
- User asks "What's wrong with my CV?": Set yaml_changes to null, provide analysis in chat_response
- User asks "Make my CV more professional": Set yaml_changes to the complete modified YAML string with improvements

CRITICAL: The yaml_changes field must be a YAML string, not a JSON object. If you're modifying the CV, return the complete YAML as a string.

Make sure your JSON is properly formatted and valid.
"""

        try:
            messages = [
                {"role": "system", "content": system_prompt.format(current_yaml=current_yaml)},
                {"role": "user", "content": user_message}
            ]
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.3,
                max_tokens=2000
            )
            
            ai_response = response.choices[0].message.content
            
            # Try to parse as JSON, fallback to plain text
            try:
                if ai_response:
                    parsed_response = json.loads(ai_response)
                    yaml_changes = parsed_response.get("yaml_changes")
                    
                    # If there are YAML changes, create a suggestion
                    suggestion = None
                    if yaml_changes and yaml_changes != current_yaml:
                        suggestion = self.create_suggestion(
                            current_yaml, 
                            yaml_changes, 
                            parsed_response.get("explanation", "AI suggested changes")
                        )
                    
                    return {
                        "chat_response": parsed_response.get("chat_response", ai_response),
                        "yaml_changes": yaml_changes,
                        "suggestion": suggestion
                    }
                else:
                    return {
                        "chat_response": "No response from AI",
                        "yaml_changes": None,
                        "suggestion": None
                    }
            except json.JSONDecodeError:
                return {
                    "chat_response": ai_response or "No response from AI",
                    "yaml_changes": None,
                    "suggestion": None
                }
                
        except Exception as e:
            return {
                "chat_response": f"Error getting AI response: {str(e)}",
                "yaml_changes": None,
                "suggestion": None
            }

class SimpleYAMLEditor:
    def __init__(self):
        self.working_cv_file = "working_CV.yaml"
        self.temp_dir = "temp_renders"
        self.ensure_directories()
        self.current_render = None
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.pending_renders = {}
    
    def ensure_directories(self):
        """Ensure required directories exist."""
        os.makedirs(self.temp_dir, exist_ok=True)
    
    def load_yaml(self):
        """Load YAML content from file."""
        try:
            if os.path.exists(self.working_cv_file):
                with open(self.working_cv_file, 'r', encoding='utf-8') as file:
                    return file.read()
            else:
                return """# Create your CV YAML here
cv:
  name: Your Name
  email: your.email@example.com
  phone: "+1 (555) 123-4567"
  location: Your City, State
  
  sections:
    welcome_to_RenderCV!:
      - RenderCV is a LaTeX-based CV/resume framework.
      - You can edit this YAML file to create your CV.
      - Ask the AI assistant to help you improve your CV!
    
    experience:
      - company: Your Company
        position: Your Position
        start_date: 2020-01
        end_date: present
        highlights:
          - Describe your achievements here
          - Use bullet points for clarity
          
    education:
      - institution: Your University
        degree: Your Degree
        start_date: 2016-09
        end_date: 2020-06
        
    skills:
      - label: Programming Languages
        details: Python, JavaScript, Java
      - label: Technologies
        details: React, Node.js, PostgreSQL
        
design:
  theme: engineeringresumes
  font: Source Sans 3
  font_size: 10pt
  page_size: letterpaper
  color: rgb(0,79,144)
  disable_page_numbering: false
  page_numbering_style: NAME - Page PAGE_NUMBER of TOTAL_PAGES
  disable_last_updated_date: false
  last_updated_date_style: Last updated in TODAY
  header_separator: none
  use_icons_for_connections: true
  margins:
    page:
      top: 0.7 in
      bottom: 0.7 in  
      left: 0.7 in
      right: 0.7 in
    section_title:
      top: 0.3 in
      bottom: 0.2 in
    entry_area:
      left_and_right: 0.2 in
      vertical_between: 0.2 in
      date_and_location_width: 4.5 cm
      education_degree_width: 1 cm
    highlights:
      top: 0.10 in
      left: 0.4 in
      vertical_between_bullet_points: 0.10 in
    header:
      vertical_between_name_and_connections: 0.3 in
      bottom: 0.3 in
      horizontal_between_connections: 0.5 in"""
        except Exception as e:
            return f"# Error loading file: {str(e)}"
    
    def save_yaml(self, yaml_content):
        """Save YAML and start rendering in the background."""
        try:
            # Validate YAML syntax
            yaml.safe_load(yaml_content)

            # Save to file
            with open(self.working_cv_file, 'w', encoding='utf-8') as file:
                file.write(yaml_content)

            # Start background render
            render_info = self.start_render(yaml_content)

            return {
                "success": True,
                "render": render_info
            }
        except yaml.YAMLError as e:
            return {"error": f"Invalid YAML: {str(e)}"}
        except Exception as e:
            return {"error": f"Error: {str(e)}"}

    def start_render(self, yaml_content):
        """Begin rendering asynchronously and return info."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        future = self.executor.submit(self.render_pdf, yaml_content, timestamp)
        self.pending_renders[timestamp] = future
        return {"started": True, "pdf_url": f"/pdf/{timestamp}", "timestamp": timestamp}
    
    def render_pdf(self, yaml_content, timestamp):
        """Render CV to PDF using RenderCV."""
        try:
            # Create unique temp directory
            temp_render_dir = os.path.join(self.temp_dir, f"render_{timestamp}")
            os.makedirs(temp_render_dir, exist_ok=True)
            
            # Create temp YAML file
            temp_yaml = os.path.join(temp_render_dir, "temp_cv.yaml")
            with open(temp_yaml, 'w', encoding='utf-8') as file:
                file.write(yaml_content)
            
            # Use RenderCV to render PDF (without --pdf-path as it may not be supported)
            # Use just the filename since we're setting cwd to the temp directory
            yaml_filename = "temp_cv.yaml"
            cmd = ["python", "-m", "rendercv", "render", yaml_filename]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15, cwd=temp_render_dir)
            
            # Debug: Print render result
            print(f"RenderCV return code: {result.returncode}")
            print(f"RenderCV stdout: {result.stdout}")
            print(f"RenderCV stderr: {result.stderr}")
            
            # RenderCV creates PDF in a rendercv_output subdirectory
            # Look for PDF files in the rendercv_output directory
            rendercv_output_dir = os.path.join(temp_render_dir, "rendercv_output")
            if os.path.exists(rendercv_output_dir):
                pdf_files = [f for f in os.listdir(rendercv_output_dir) if f.endswith('.pdf')]
                print(f"Found {len(pdf_files)} PDF files in rendercv_output: {pdf_files}")
            else:
                # Fallback: look in the main temp directory
                pdf_files = [f for f in os.listdir(temp_render_dir) if f.endswith('.pdf')]
                rendercv_output_dir = temp_render_dir
                print(f"Found {len(pdf_files)} PDF files in temp dir: {pdf_files}")
            
            if result.returncode == 0 and pdf_files:
                # Use the first PDF found (there should be only one)
                pdf_file = pdf_files[0]
                pdf_path = os.path.join(rendercv_output_dir, pdf_file)

                self.current_render = {
                    "pdf_path": pdf_path,
                    "timestamp": timestamp,
                    "temp_dir": temp_render_dir
                }

                # Mark render as finished
                self.pending_renders.pop(timestamp, None)

                return {
                    "success": True,
                    "pdf_url": f"/pdf/{timestamp}",
                    "timestamp": timestamp
                }
            else:
                error_msg = result.stderr or result.stdout or 'Unknown error'
                print(f"RenderCV failed with error: {error_msg}")
                print(f"Temp directory contents: {os.listdir(temp_render_dir)}")
                if os.path.exists(rendercv_output_dir):
                    print(f"rendercv_output contents: {os.listdir(rendercv_output_dir)}")
                self.pending_renders.pop(timestamp, None)
                return {
                    "error": f"RenderCV failed: {error_msg}"
                }
                
        except subprocess.TimeoutExpired:
            self.pending_renders.pop(timestamp, None)
            return {"error": "Rendering timed out"}
        except Exception as e:
            self.pending_renders.pop(timestamp, None)
            return {"error": f"Render error: {str(e)}"}

editor = SimpleYAMLEditor()
chat_manager = ChatManager()

# HTML Template for the 3-panel editor
EDITOR_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI-Powered YAML CV Editor</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/codemirror.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/mode/yaml/yaml.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/codemirror.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/theme/darcula.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #1e1e1e;
            color: #ffffff;
            height: 100vh;
            overflow: hidden;
        }
        
        .header {
            background: #2d2d2d;
            padding: 10px 20px;
            border-bottom: 1px solid #404040;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .header h1 {
            font-size: 18px;
            font-weight: 600;
        }
        
        .status {
            font-size: 14px;
            padding: 4px 8px;
            border-radius: 4px;
            background: #007acc;
        }
        
        .status.error {
            background: #d73a49;
        }
        
        .status.success {
            background: #28a745;
        }
        
        .main {
            display: flex;
            height: calc(100vh - 60px);
        }
        
        .chat-panel {
            width: 30%;
            border-right: 1px solid #404040;
            display: flex;
            flex-direction: column;
            background: #2d2d2d;
        }
        
        .chat-header {
            padding: 15px;
            border-bottom: 1px solid #404040;
            background: #363636;
        }
        
        .chat-header h3 {
            font-size: 16px;
            color: #ffffff;
            margin: 0;
        }
        
        .chat-messages {
            flex: 1;
            overflow-y: auto;
            padding: 10px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        
        .message {
            max-width: 85%;
            padding: 8px 12px;
            border-radius: 8px;
            word-wrap: break-word;
            font-size: 14px;
            line-height: 1.4;
        }
        
        .message.user {
            align-self: flex-end;
            background: #007acc;
            color: white;
        }
        
        .message.ai {
            align-self: flex-start;
            background: #404040;
            color: #ffffff;
        }
        
        .message.system {
            align-self: center;
            background: #2d2d2d;
            color: #888;
            font-style: italic;
            font-size: 12px;
        }
        
        .chat-input-area {
            border-top: 1px solid #404040;
            padding: 15px;
            background: #363636;
        }
        
        .chat-input-container {
            display: flex;
            gap: 10px;
        }
        
        .chat-input {
            flex: 1;
            padding: 8px 12px;
            border: 1px solid #555;
            border-radius: 6px;
            background: #2d2d2d;
            color: #ffffff;
            font-size: 14px;
            resize: none;
            min-height: 36px;
            max-height: 100px;
        }
        
        .chat-input:focus {
            outline: none;
            border-color: #007acc;
        }
        
        .send-button {
            padding: 8px 16px;
            background: #007acc;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            white-space: nowrap;
        }
        
        .send-button:hover {
            background: #005a8c;
        }
        
        .send-button:disabled {
            background: #555;
            cursor: not-allowed;
        }
        
        .editor-panel {
            width: 40%;
            border-right: 1px solid #404040;
            position: relative;
        }
        
        .preview-panel {
            width: 30%;
            background: #f8f9fa;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            position: relative;
        }
        
        .CodeMirror {
            height: 100% !important;
            font-size: 14px;
            line-height: 1.5;
        }
        
        .pdf-preview {
            width: 100%;
            height: 100%;
            border: none;
        }
        
        .preview-message {
            text-align: center;
            color: #666;
            font-size: 16px;
        }
        
        .loading {
            display: flex;
            align-items: center;
            justify-content: center;
            color: #007acc;
            font-size: 16px;
        }
        
        .loading::after {
            content: '...';
            animation: dots 1.5s steps(4, end) infinite;
        }
        
        @keyframes dots {
            0%, 20% { content: '.'; }
            40% { content: '..'; }
            60% { content: '...'; }
            80%, 100% { content: ''; }
        }
        
        .typing-indicator {
            align-self: flex-start;
            background: #404040;
            color: #888;
            padding: 8px 12px;
            border-radius: 8px;
            font-style: italic;
            font-size: 12px;
        }
        
        .typing-indicator::after {
            content: '...';
            animation: dots 1.5s steps(4, end) infinite;
        }
        
        /* Scrollbar styling */
        .chat-messages::-webkit-scrollbar {
            width: 6px;
        }
        
        .chat-messages::-webkit-scrollbar-track {
            background: #2d2d2d;
        }
        
        .chat-messages::-webkit-scrollbar-thumb {
            background: #555;
            border-radius: 3px;
        }
        
        .chat-messages::-webkit-scrollbar-thumb:hover {
            background: #666;
        }
        
        /* Suggestion styles */
        .suggestion-container {
            background: #2d2d2d;
            border: 1px solid #404040;
            border-radius: 8px;
            margin: 10px 0;
            overflow: hidden;
        }
        
        .suggestion-header {
            background: #363636;
            padding: 12px 15px;
            border-bottom: 1px solid #404040;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .suggestion-title {
            font-size: 14px;
            font-weight: 600;
            color: #ffffff;
        }
        
        .suggestion-actions {
            display: flex;
            gap: 8px;
        }
        
        .suggestion-btn {
            padding: 6px 12px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            font-weight: 500;
            transition: all 0.2s;
        }
        
        .suggestion-btn.accept {
            background: #28a745;
            color: white;
        }
        
        .suggestion-btn.accept:hover {
            background: #218838;
        }
        
        .suggestion-btn.decline {
            background: #dc3545;
            color: white;
        }
        
        .suggestion-btn.decline:hover {
            background: #c82333;
        }
        
        .suggestion-content {
            padding: 15px;
        }
        
        .suggestion-explanation {
            color: #cccccc;
            font-size: 13px;
            line-height: 1.4;
            margin-bottom: 15px;
        }
        
        .diff-viewer {
            background: #1e1e1e;
            border: 1px solid #404040;
            border-radius: 6px;
            overflow: hidden;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 12px;
            line-height: 1.4;
        }
        
        .diff-header {
            background: #363636;
            padding: 8px 12px;
            border-bottom: 1px solid #404040;
            font-size: 11px;
            color: #888;
            font-weight: 600;
        }
        
        .diff-content {
            max-height: 300px;
            overflow-y: auto;
            padding: 0;
        }
        
        .diff-line {
            padding: 2px 12px;
            white-space: pre;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
        }
        
        .diff-line.removed {
            background: rgba(220, 53, 69, 0.2);
            color: #dc3545;
            text-decoration: line-through;
        }
        
        .diff-line.added {
            background: rgba(40, 167, 69, 0.2);
            color: #28a745;
        }
        
        .diff-line.context {
            color: #888;
        }
        
        .diff-line.header {
            background: #2d2d2d;
            color: #666;
            font-weight: 600;
        }
        
        /* CodeMirror diff highlighting */
        .CodeMirror-line.diff-removed {
            background: rgba(220, 53, 69, 0.1);
            text-decoration: line-through;
            color: #dc3545;
        }
        
        .CodeMirror-line.diff-added {
            background: rgba(40, 167, 69, 0.1);
            color: #28a745;
        }
        
        .suggestion-status {
            font-size: 11px;
            padding: 4px 8px;
            border-radius: 3px;
            font-weight: 500;
        }
        
        .suggestion-status.pending {
            background: #ffc107;
            color: #212529;
        }
        
        .suggestion-status.accepted {
            background: #28a745;
            color: white;
        }
        
        .suggestion-status.declined {
            background: #dc3545;
            color: white;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 AI-Powered YAML CV Editor</h1>
        <div class="status" id="status">Ready</div>
    </div>
    
    <div class="main">
        <div class="chat-panel">
            <div class="chat-header">
                <h3>💬 AI Assistant</h3>
            </div>
            <div class="chat-messages" id="chat-messages">
                <div class="message system">
                    Welcome! I'm your AI assistant. I can help you improve your CV, answer questions about resume writing, and directly modify your YAML content. Just ask me anything!
                </div>
            </div>
            <div class="chat-input-area">
                <div class="chat-input-container">
                    <textarea 
                        class="chat-input" 
                        id="chat-input" 
                        placeholder="Ask me to help with your CV..."
                        rows="1"
                    ></textarea>
                    <button class="send-button" id="send-button">Send</button>
                </div>
            </div>
        </div>
        
        <div class="editor-panel">
            <textarea id="yaml-editor">{{ yaml_content }}</textarea>
        </div>
        
        <div class="preview-panel">
            <div class="preview-message" id="preview-message">
                Start editing to see your CV preview
            </div>
            <iframe class="pdf-preview" id="pdf-preview" style="display: none;"></iframe>
        </div>
    </div>

    <script>
        // Initialize CodeMirror
        const editor = CodeMirror.fromTextArea(document.getElementById('yaml-editor'), {
            mode: 'yaml',
            theme: 'darcula',
            lineNumbers: true,
            lineWrapping: true,
            indentUnit: 2,
            tabSize: 2,
            autoCloseBrackets: true,
            matchBrackets: true
        });
        
        const statusEl = document.getElementById('status');
        const previewMessage = document.getElementById('preview-message');
        const pdfPreview = document.getElementById('pdf-preview');
        const chatMessages = document.getElementById('chat-messages');
        const chatInput = document.getElementById('chat-input');
        const sendButton = document.getElementById('send-button');
        
        let saveTimeout;
        let isRendering = false;
        let isChatting = false;
        
        function setStatus(message, type = 'info') {
            statusEl.textContent = message;
            statusEl.className = 'status ' + type;
        }
        
        function showPreviewMessage(message) {
            previewMessage.textContent = message;
            previewMessage.style.display = 'block';
            pdfPreview.style.display = 'none';
        }
        
        function showPDF(url, attempts = 0) {
            fetch(url, { method: 'HEAD' })
                .then(resp => {
                    if (resp.ok) {
                        pdfPreview.src = url + '?t=' + Date.now();
                        pdfPreview.style.display = 'block';
                        previewMessage.style.display = 'none';
                        setStatus('Rendered successfully', 'success');
                    } else if (attempts < 10) {
                        setTimeout(() => showPDF(url, attempts + 1), 1000);
                    } else {
                        setStatus('Render error', 'error');
                        showPreviewMessage('❌ Render timed out');
                    }
                })
                .catch(() => {
                    if (attempts < 10) {
                        setTimeout(() => showPDF(url, attempts + 1), 1000);
                    } else {
                        setStatus('Render error', 'error');
                        showPreviewMessage('❌ Network error');
                    }
                });
        }
        
        function addMessage(role, content, suggestion = null) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${role}`;
            messageDiv.textContent = content;
            chatMessages.appendChild(messageDiv);
            
            // If there's a suggestion, add it after the message
            if (suggestion) {
                const suggestionDiv = createSuggestionElement(suggestion);
                chatMessages.appendChild(suggestionDiv);
            }
            
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
        
        function createSuggestionElement(suggestion) {
            const container = document.createElement('div');
            container.className = 'suggestion-container';
            container.id = `suggestion-${suggestion.id}`;
            
            const header = document.createElement('div');
            header.className = 'suggestion-header';
            
            const title = document.createElement('div');
            title.className = 'suggestion-title';
            title.textContent = '🤖 AI Suggestion';
            
            const status = document.createElement('span');
            status.className = `suggestion-status ${suggestion.status}`;
            status.textContent = suggestion.status;
            
            const actions = document.createElement('div');
            actions.className = 'suggestion-actions';
            
            if (suggestion.status === 'pending') {
                const acceptBtn = document.createElement('button');
                acceptBtn.className = 'suggestion-btn accept';
                acceptBtn.textContent = '✓ Accept';
                acceptBtn.onclick = () => acceptSuggestion(suggestion.id);
                
                const declineBtn = document.createElement('button');
                declineBtn.className = 'suggestion-btn decline';
                declineBtn.textContent = '✗ Decline';
                declineBtn.onclick = () => declineSuggestion(suggestion.id);
                
                actions.appendChild(acceptBtn);
                actions.appendChild(declineBtn);
            }
            
            header.appendChild(title);
            header.appendChild(status);
            header.appendChild(actions);
            
            const content = document.createElement('div');
            content.className = 'suggestion-content';
            
            const explanation = document.createElement('div');
            explanation.className = 'suggestion-explanation';
            explanation.textContent = suggestion.explanation;
            
            const diffViewer = createDiffViewer(suggestion.diff);
            
            content.appendChild(explanation);
            content.appendChild(diffViewer);
            
            container.appendChild(header);
            container.appendChild(content);
            
            return container;
        }
        
        function createDiffViewer(diff) {
            const container = document.createElement('div');
            container.className = 'diff-viewer';
            
            const header = document.createElement('div');
            header.className = 'diff-header';
            header.textContent = 'Changes Preview';
            
            const content = document.createElement('div');
            content.className = 'diff-content';
            
            diff.forEach(line => {
                const lineDiv = document.createElement('div');
                lineDiv.className = 'diff-line';
                
                if (line.startsWith('---') || line.startsWith('+++') || line.startsWith('@@')) {
                    lineDiv.className += ' header';
                } else if (line.startsWith('-')) {
                    lineDiv.className += ' removed';
                } else if (line.startsWith('+')) {
                    lineDiv.className += ' added';
                } else {
                    lineDiv.className += ' context';
                }
                
                lineDiv.textContent = line;
                content.appendChild(lineDiv);
            });
            
            container.appendChild(header);
            container.appendChild(content);
            
            return container;
        }
        
        function acceptSuggestion(suggestionId) {
            fetch(`/api/suggestion/${suggestionId}/accept`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update the editor with the accepted YAML
                    editor.setValue(data.yaml_content);
                    
                    // Update suggestion status
                    const suggestionEl = document.getElementById(`suggestion-${suggestionId}`);
                    if (suggestionEl) {
                        const statusEl = suggestionEl.querySelector('.suggestion-status');
                        statusEl.textContent = 'accepted';
                        statusEl.className = 'suggestion-status accepted';
                        
                        // Remove action buttons
                        const actionsEl = suggestionEl.querySelector('.suggestion-actions');
                        if (actionsEl) {
                            actionsEl.innerHTML = '';
                        }
                    }
                    
                    // Trigger save and render
                    clearTimeout(saveTimeout);
                    saveTimeout = setTimeout(() => {
                        saveAndRender();
                    }, 500);
                    
                    addMessage('system', '✅ Suggestion accepted and applied');
                } else {
                    addMessage('system', '❌ Error accepting suggestion: ' + data.error);
                }
            })
            .catch(error => {
                addMessage('system', '❌ Network error: ' + error.message);
            });
        }
        
        function declineSuggestion(suggestionId) {
            fetch(`/api/suggestion/${suggestionId}/decline`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update suggestion status
                    const suggestionEl = document.getElementById(`suggestion-${suggestionId}`);
                    if (suggestionEl) {
                        const statusEl = suggestionEl.querySelector('.suggestion-status');
                        statusEl.textContent = 'declined';
                        statusEl.className = 'suggestion-status declined';
                        
                        // Remove action buttons
                        const actionsEl = suggestionEl.querySelector('.suggestion-actions');
                        if (actionsEl) {
                            actionsEl.innerHTML = '';
                        }
                    }
                    
                    addMessage('system', '❌ Suggestion declined');
                } else {
                    addMessage('system', '❌ Error declining suggestion: ' + data.error);
                }
            })
            .catch(error => {
                addMessage('system', '❌ Network error: ' + error.message);
            });
        }
        
        function addTypingIndicator() {
            const typingDiv = document.createElement('div');
            typingDiv.className = 'typing-indicator';
            typingDiv.id = 'typing-indicator';
            typingDiv.textContent = 'AI is thinking';
            chatMessages.appendChild(typingDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
            return typingDiv;
        }
        
        function removeTypingIndicator() {
            const typingIndicator = document.getElementById('typing-indicator');
            if (typingIndicator) {
                typingIndicator.remove();
            }
        }
        
        function saveAndRender() {
            if (isRendering) return;
            
            isRendering = true;
            setStatus('Rendering...', 'info');
            showPreviewMessage('🔄 Rendering CV...');
            
            const yamlContent = editor.getValue();
            
            fetch('/api/save', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ yaml: yamlContent })
            })
            .then(response => response.json())
            .then(data => {
                isRendering = false;

                if (data.success) {
                    if (data.render && data.render.started) {
                        showPDF(data.render.pdf_url);
                    } else if (data.render && data.render.error) {
                        setStatus('Render error', 'error');
                        showPreviewMessage('❌ ' + data.render.error);
                    }
                } else {
                    setStatus('Error: ' + data.error, 'error');
                    showPreviewMessage('❌ ' + data.error);
                }
            })
            .catch(error => {
                isRendering = false;
                setStatus('Network error', 'error');
                showPreviewMessage('❌ Network error: ' + error.message);
            });
        }
        
        function sendChatMessage() {
            const message = chatInput.value.trim();
            if (!message || isChatting) return;
            
            // Add user message
            addMessage('user', message);
            chatInput.value = '';
            
            // Show typing indicator
            const typingIndicator = addTypingIndicator();
            
            isChatting = true;
            sendButton.disabled = true;
            
            const yamlContent = editor.getValue();
            
            fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    message: message,
                    yaml_content: yamlContent
                })
            })
            .then(response => response.json())
            .then(data => {
                removeTypingIndicator();
                
                if (data.success) {
                    // Add AI response with suggestion if available
                    addMessage('ai', data.response, data.suggestion);
                    
                    // Debug logging
                    console.log('AI Response:', data);
                    
                    // If AI provided YAML changes but no suggestion, this shouldn't happen
                    // as the backend should always create a suggestion when there are changes
                    if (data.yaml_changes && !data.suggestion) {
                        addMessage('system', '⚠️ AI provided changes but no suggestion was created');
                        console.log('YAML changes without suggestion:', data.yaml_changes);
                    }
                } else {
                    addMessage('system', '❌ Error: ' + data.error);
                }
                
                isChatting = false;
                sendButton.disabled = false;
            })
            .catch(error => {
                removeTypingIndicator();
                addMessage('system', '❌ Network error: ' + error.message);
                isChatting = false;
                sendButton.disabled = false;
            });
        }
        
        // Chat event listeners
        sendButton.addEventListener('click', sendChatMessage);
        
        chatInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendChatMessage();
            }
        });
        
        // Auto-resize chat input
        chatInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 100) + 'px';
        });
        
        // Auto-save with debouncing
        editor.on('change', function() {
            setStatus('Editing...', 'info');
            
            clearTimeout(saveTimeout);
            saveTimeout = setTimeout(() => {
                saveAndRender();
            }, 1500); // 1.5 second delay after stopping typing
        });
        
        // Load chat history
        fetch('/api/chat/history')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    data.messages.forEach(msg => {
                        if (msg.role !== 'system') {
                            // Load suggestion if available
                            let suggestion = null;
                            if (msg.suggestion_id) {
                                // For now, we'll load suggestions from the server
                                // In a full implementation, you might want to store suggestions in localStorage
                                // or implement a proper suggestion loading mechanism
                            }
                            addMessage(msg.role, msg.content, suggestion);
                        }
                    });
                }
            });
        
        // Initial render
        setTimeout(() => {
            saveAndRender();
        }, 500);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Serve the main editor page."""
    yaml_content = editor.load_yaml()
    return render_template_string(EDITOR_HTML, yaml_content=yaml_content)

@app.route('/api/save', methods=['POST'])  
def save_yaml():
    """Save YAML and render PDF."""
    data = request.get_json()
    yaml_content = data.get('yaml', '')
    
    result = editor.save_yaml(yaml_content)
    return jsonify(result)

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages with AI."""
    data = request.get_json()
    user_message = data.get('message', '')
    yaml_content = data.get('yaml_content', '')
    
    if not user_message:
        return jsonify({"success": False, "error": "No message provided"})
    
    # Add user message to chat history
    chat_manager.add_message("user", user_message)
    
    try:
        # Get AI response (this is a simplified synchronous version)
        # In production, you might want to make this async
        import asyncio
        
        # For now, we'll use a simple synchronous approach
        if not chat_manager.openai_client:
            ai_result = {
                "chat_response": "AI is not available. Please set your OPENAI_API_KEY environment variable.",
                "yaml_changes": None,
                "suggestion": None
            }
        else:
            # Simplified synchronous call - in production, consider async
            try:
                system_prompt = f"""You are an AI assistant helping with CV/resume editing. You can:
1. Answer questions about CV writing and formatting
2. Suggest improvements to the CV content  
3. Provide suggestions for YAML modifications

IMPORTANT RULES:
- For general questions, advice, or explanations: Set yaml_changes to null and provide helpful text in chat_response
- For actual CV modifications: Provide the complete modified YAML in yaml_changes field
- NEVER paste the current YAML in chat_response - only provide explanations and advice there
- When making changes, always use the yaml_changes field, not the chat_response field
- CRITICAL: The yaml_changes field must be a YAML string, not a JSON object

The CV uses RenderCV format. Here's the current YAML:

```yaml
{yaml_content}
```

Respond in JSON format:
{{
    "chat_response": "Your explanation, advice, or response (DO NOT include YAML here)",
    "yaml_changes": "Complete modified YAML content as a string (only if making actual changes, otherwise null)",
    "explanation": "Detailed explanation of the changes you're suggesting"
}}

EXAMPLES:
- User asks "How do I improve my CV?": Set yaml_changes to null, provide advice in chat_response
- User asks "Add a new skill": Set yaml_changes to the complete modified YAML string with the new skill added
- User asks "What's wrong with my CV?": Set yaml_changes to null, provide analysis in chat_response
- User asks "Make my CV more professional": Set yaml_changes to the complete modified YAML string with improvements

CRITICAL: The yaml_changes field must be a YAML string, not a JSON object. If you're modifying the CV, return the complete YAML as a string.

Make sure your JSON is properly formatted and valid.
"""
                
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ]
                
                response = chat_manager.openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    temperature=0.3,
                    max_tokens=2000
                )
                
                ai_response = response.choices[0].message.content
                
                # Try to parse as JSON, fallback to plain text
                try:
                    if ai_response:
                        print(f"DEBUG: Raw AI response: {ai_response[:200]}...")  # First 200 chars
                        parsed_response = json.loads(ai_response)
                        yaml_changes = parsed_response.get("yaml_changes")
                        
                        print(f"DEBUG: Parsed yaml_changes type: {type(yaml_changes)}")
                        print(f"DEBUG: yaml_changes is None: {yaml_changes is None}")
                        
                        # If there are YAML changes, create a suggestion
                        suggestion = None
                        if yaml_changes and yaml_changes != yaml_content:
                            print(f"DEBUG: Creating suggestion - changes detected")
                            suggestion = chat_manager.create_suggestion(
                                yaml_content, 
                                yaml_changes, 
                                parsed_response.get("explanation", "AI suggested changes")
                            )
                        elif yaml_changes:
                            # Debug: YAML changes were provided but they're identical to current content
                            print(f"DEBUG: YAML changes provided but identical to current content")
                            print(f"DEBUG: yaml_changes length: {len(yaml_changes) if yaml_changes else 0}")
                            print(f"DEBUG: yaml_content length: {len(yaml_content) if yaml_content else 0}")
                            print(f"DEBUG: Are they equal? {yaml_changes == yaml_content}")
                        else:
                            print(f"DEBUG: No yaml_changes provided")
                        
                        ai_result = {
                            "chat_response": parsed_response.get("chat_response", ai_response),
                            "yaml_changes": yaml_changes,
                            "suggestion": suggestion
                        }
                    else:
                        ai_result = {
                            "chat_response": "No response from AI",
                            "yaml_changes": None,
                            "suggestion": None
                        }
                except json.JSONDecodeError as e:
                    print(f"DEBUG: JSON decode error: {e}")
                    print(f"DEBUG: Failed to parse: {ai_response}")
                    ai_result = {
                        "chat_response": ai_response or "No response from AI", 
                        "yaml_changes": None,
                        "suggestion": None
                    }
                    
            except Exception as e:
                ai_result = {
                    "chat_response": f"Error getting AI response: {str(e)}",
                    "yaml_changes": None,
                    "suggestion": None
                }
        
        # Add AI response to chat history
        suggestion_id = ai_result["suggestion"]["id"] if ai_result["suggestion"] else None
        chat_manager.add_message("ai", ai_result["chat_response"], ai_result["yaml_changes"], suggestion_id)
        
        return jsonify({
            "success": True,
            "response": ai_result["chat_response"],
            "yaml_changes": ai_result["yaml_changes"],
            "suggestion": ai_result["suggestion"]
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/chat/history')
def chat_history():
    """Get chat history."""
    return jsonify({
        "success": True,
        "messages": chat_manager.get_chat_history()
    })

@app.route('/api/suggestion/<suggestion_id>')
def get_suggestion(suggestion_id):
    """Get a specific suggestion."""
    suggestion = chat_manager.get_suggestion(suggestion_id)
    if suggestion:
        return jsonify({
            "success": True,
            "suggestion": suggestion
        })
    return jsonify({"success": False, "error": "Suggestion not found"}), 404

@app.route('/api/suggestion/<suggestion_id>/accept', methods=['POST'])
def accept_suggestion(suggestion_id):
    """Accept a suggestion."""
    accepted_yaml = chat_manager.accept_suggestion(suggestion_id)
    if accepted_yaml:
        return jsonify({
            "success": True,
            "yaml_content": accepted_yaml
        })
    return jsonify({"success": False, "error": "Suggestion not found"}), 404

@app.route('/api/suggestion/<suggestion_id>/decline', methods=['POST'])
def decline_suggestion(suggestion_id):
    """Decline a suggestion."""
    suggestion = chat_manager.decline_suggestion(suggestion_id)
    if suggestion:
        return jsonify({
            "success": True,
            "message": "Suggestion declined"
        })
    return jsonify({"success": False, "error": "Suggestion not found"}), 404

@app.route('/pdf/<timestamp>')
def serve_pdf(timestamp):
    """Serve the rendered PDF."""
    if editor.current_render and editor.current_render['timestamp'] == timestamp:
        pdf_path = editor.current_render['pdf_path']
        if os.path.exists(pdf_path):
            return send_file(pdf_path, mimetype='application/pdf')
    
    return "PDF not found", 404

if __name__ == '__main__':
    print("🚀 Starting AI-Powered YAML CV Editor")
    print("📝 Open your browser to: http://localhost:5000")
    print("💬 Chat with AI on the left, edit YAML in the middle, see PDF on the right")
    print("⚡ Auto-saves and renders after 1.5 seconds of inactivity")
    
    if not AI_AVAILABLE:
        print("\n⚠️  AI features require OpenAI package: pip install openai")
    elif not os.getenv('OPENAI_API_KEY'):
        print("\n⚠️  Set OPENAI_API_KEY environment variable for AI features")
        print("   Example: export OPENAI_API_KEY=your_key_here")
    else:
        print("🤖 AI assistant is ready!")
    
    print("\nPress Ctrl+C to stop")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 