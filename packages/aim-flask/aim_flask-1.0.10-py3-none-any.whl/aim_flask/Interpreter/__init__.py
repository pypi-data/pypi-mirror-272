# __init__.py

# import argparse
from .interpreter import interpret_aim_command

# Make sure only necessary functions are exported
__all__ = ["interpret_aim_command"]
