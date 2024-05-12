# interpreter.py

import json

def interpret_aim_command(aim_command):
    """
    Interpret AIM command and execute corresponding action.
    """
    parts = [part.strip() for part in aim_command.split(':') if part.strip()]
    action = parts[0]
    print("Test Print: ", action)
    if action == 'create':
        if len(parts) < 3:
            return "Invalid create action: Insufficient arguments"
        element_type = parts[1].strip()
        properties = json.loads(':'.join(parts[2:]).strip())
        return create_action(element_type, properties)
    else:
        return f"Unknown action: {action}"

def create_action(element_type, properties):
    """
    Execute create action based on provided arguments.
    """
    # Generate HTML/CSS code based on element type and properties
    if element_type == 'text':
        return generate_text_element(properties)
    else:
        return f"Unsupported element type: {element_type}"

def generate_text_element(properties):
    """
    Generate HTML/CSS code for a text element based on provided properties.
    """
    # Example: Generate HTML code for a text element
    html = f'<div style="font-family: {properties["font-family"]}; font-size: {properties["font-size"]}px; ' \
           f'color: {properties["color"]}; text-align: {properties["align"]}">{properties["text"]}</div>'
    return html
