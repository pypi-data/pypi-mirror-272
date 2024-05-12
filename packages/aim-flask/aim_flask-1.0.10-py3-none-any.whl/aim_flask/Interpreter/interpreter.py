import json
import logging
import os

current_dir = os.getcwd()

# Configure logging
logging.basicConfig(filename=f'{current_dir}/setup.log', level=logging.ERROR)

def interpret_aim_command(aim_command):
    """
    Interpret AIM command and execute corresponding action.
    """
    try:
        parts = [part.strip() for part in aim_command.split(':') if part.strip()]
        action = parts[0]
        logging.info("AIM Command: %s %s", parts[0], parts[1])
        if action == 'create':
            if len(parts) < 3:
                return "Invalid create action: Insufficient arguments"
            element_type = parts[1].strip()
            properties = json.loads(':'.join(parts[2:]).strip())
            return create_action(element_type, properties)
        else:
            return f"Unknown action: {action}"
    except Exception as e:
        logging.error("Error interpreting AIM command: %s", e)
        return "Error interpreting AIM command: {}".format(e)

def create_action(element_type, properties):
    """
    Execute create action based on provided arguments.
    """
    # Generate HTML/CSS code based on element type and properties
    try:
        if element_type == 'text':
            return generate_text_element(properties)
        else:
            return f"Unsupported element type: {element_type}"
    except Exception as e:
        logging.error("Error executing create action: %s", e)
        return "Error executing create action: {}".format(e)

def generate_text_element(properties):
    """
    Generate HTML/CSS code for a text element based on provided properties.
    """
    # Example: Generate HTML code for a text element
    try:
        html = f'<div style="font-family: {properties["font-family"]}; font-size: {properties["font-size"]}px; ' \
               f'color: {properties["color"]}; text-align: {properties["align"]}">{properties["text"]}</div>'
        return html
    except Exception as e:
        logging.error("Error generating text element: %s", e)
        return "Error generating text element: {}".format(e)
