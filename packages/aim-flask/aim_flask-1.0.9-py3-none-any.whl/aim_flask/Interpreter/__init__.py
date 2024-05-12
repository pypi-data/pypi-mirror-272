# __init__.py

# import argparse
from .interpreter import interpret_aim_command

if __name__ == "__main__":
    pass

# Make sure only necessary functions are exported
__all__ = ["interpret_aim_command"]
