# Cursor-Style AI Suggestions for YAML CV Editor

## Overview

The YAML CV Editor now features a cursor-style suggestion system that allows users to review, accept, or decline AI-generated changes with visual diff highlighting.

## Features

### 🤖 AI Suggestion Interface
- **Visual Diff Display**: Changes are shown with red highlighting for removed lines and green highlighting for added lines
- **Accept/Decline Buttons**: Users can accept (✓) or decline (✗) suggestions with a single click
- **Status Tracking**: Suggestions show their current status (pending, accepted, declined)
- **Detailed Explanations**: Each suggestion includes an explanation of what the AI is suggesting

### 🎨 Visual Design
- **Dark Theme**: Consistent with the existing editor theme
- **Diff Viewer**: Compact, scrollable diff display with syntax highlighting
- **Status Indicators**: Color-coded status badges for easy identification
- **Responsive Layout**: Suggestions integrate seamlessly with the chat interface

### 🔧 Technical Implementation

#### Backend Changes
- **Suggestion Management**: New `ChatManager` methods for creating, accepting, and declining suggestions
- **Diff Generation**: Uses Python's `difflib` to generate unified diffs
- **API Endpoints**: New REST endpoints for suggestion operations:
  - `GET /api/suggestion/<id>` - Get suggestion details
  - `POST /api/suggestion/<id>/accept` - Accept a suggestion
  - `POST /api/suggestion/<id>/decline` - Decline a suggestion

#### Frontend Changes
- **Suggestion Components**: JavaScript functions to create and manage suggestion UI elements
- **Diff Rendering**: Client-side diff display with proper styling
- **Event Handling**: Accept/decline button functionality with immediate feedback
- **Status Updates**: Real-time status updates when suggestions are acted upon

## How It Works

1. **User Request**: User asks AI to modify their CV
2. **AI Analysis**: AI analyzes the current YAML and generates suggestions
3. **Suggestion Creation**: System creates a suggestion with diff information
4. **Visual Display**: Suggestion appears in chat with diff viewer and action buttons
5. **User Decision**: User can accept or decline the suggestion
6. **Application**: If accepted, changes are applied to the editor and CV is re-rendered

## Usage Example

1. Open the YAML CV Editor
2. In the chat panel, ask the AI to make changes (e.g., "Improve my skills section")
3. AI will respond with a suggestion showing:
   - Explanation of the changes
   - Visual diff of what will be changed
   - Accept (✓) and Decline (✗) buttons
4. Click "Accept" to apply the changes or "Decline" to reject them
5. The suggestion status will update accordingly

## Benefits

- **User Control**: Users maintain full control over what changes are applied
- **Transparency**: Clear visibility into what the AI is suggesting
- **Efficiency**: Quick accept/decline actions without manual editing
- **Learning**: Users can see exactly what improvements the AI suggests
- **Safety**: No automatic changes without user approval

## Technical Details

### Suggestion Data Structure
```json
{
  "id": "uuid",
  "original_yaml": "original content",
  "suggested_yaml": "modified content", 
  "explanation": "What the AI is suggesting",
  "diff": ["diff lines"],
  "created_at": "timestamp",
  "status": "pending|accepted|declined"
}
```

### CSS Classes
- `.suggestion-container` - Main suggestion wrapper
- `.diff-line.removed` - Red highlighting for removed lines
- `.diff-line.added` - Green highlighting for added lines
- `.suggestion-status.pending` - Yellow status badge
- `.suggestion-status.accepted` - Green status badge
- `.suggestion-status.declined` - Red status badge

## Future Enhancements

- **Suggestion History**: Persistent storage of suggestions across sessions
- **Batch Operations**: Accept/decline multiple suggestions at once
- **Custom Diff Views**: Different diff formats (side-by-side, inline)
- **Suggestion Categories**: Different types of suggestions (content, formatting, etc.)
- **Undo/Redo**: Ability to undo accepted suggestions 