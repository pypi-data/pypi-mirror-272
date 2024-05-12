# __init__.py

from .main import run_setup, run_feedback, run_help, run_version, run_preview
import argparse
import sys
import aim_flask.Interpreter.interpreter as interpret_aim_command

def main():
    parser = argparse.ArgumentParser(description="AIM CLI for environment setup and installation")
    parser.add_argument("command", choices=[":cli", ":version", ":setup", ":feedback", ":help", ":verbose", ":preview"], help="Command to execute")
    args = parser.parse_args()
    args.command == sys.argv[1] if len(sys.argv) > 1 else None

    if args.command == ":version":
        run_version()
    elif args.command == ":setup":
        run_setup(verbose=True)
    elif args.command == ":feedback":
        feedback_message = input("Enter your feedback message: ")
        run_feedback(feedback_message)
    elif args.command == ":help":
        run_help()
    elif args.command == ":verbose":
        print("Verbose mode enabled.")
        run_setup(verbose=True)
    elif args.command == ":preview":
        print("Verbose mode enabled.")
        run_preview(verbose=True)
    

if __name__ == "__main__":
    main()

# Make sure only necessary functions are exported
__all__ = ["run_setup", "run_feedback", "run_help", "run_version", "main", "run_preview", "interpret_aim_command"]
