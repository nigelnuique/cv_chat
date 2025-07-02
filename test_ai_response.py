#!/usr/bin/env python3
"""
Test script to simulate AI response and check if suggestion system works
"""

import json
import sys

# Add the system site-packages path so PyYAML can be imported in environments
# where it is installed outside the user's default site-packages directory.
sys.path.append('/usr/lib/python3/dist-packages')
import yaml

# Load the current YAML
with open('working_CV.yaml', 'r', encoding='utf-8') as f:
    current_yaml = f.read()

# Create a modified version with name changed to "Bob Dylan"
yaml_data = yaml.safe_load(current_yaml)
yaml_data['cv']['name'] = 'Bob Dylan'

# Convert back to YAML string
modified_yaml = yaml.dump(yaml_data, default_flow_style=False, sort_keys=False)

# Simulate what the AI should return
ai_response = {
    "chat_response": "I have updated your name from 'Nigel Nuique' to 'Bob Dylan'.",
    "yaml_changes": modified_yaml,
    "explanation": "Changed the name field in the CV from 'Nigel Nuique' to 'Bob Dylan' as requested."
}

print("=== Simulated AI Response ===")
print(json.dumps(ai_response, indent=2))

print("\n=== Current YAML (first 100 chars) ===")
print(current_yaml[:100])

print("\n=== Modified YAML (first 100 chars) ===")
print(modified_yaml[:100])

print("\n=== Are they different? ===")
print(f"Current length: {len(current_yaml)}")
print(f"Modified length: {len(modified_yaml)}")
print(f"Are equal: {current_yaml == modified_yaml}")

# Test the suggestion creation logic
if modified_yaml != current_yaml:
    print("\n✅ YAML changes detected - suggestion should be created")
else:
    print("\n❌ No YAML changes detected - no suggestion should be created") 