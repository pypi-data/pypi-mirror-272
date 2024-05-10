import argparse
import os
import subprocess
import platform
import logging

# aim_flask.py

__version__ = "1.0.4"

# Configure logging
logging.basicConfig(filename='../setup.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# GitHub repository URL for feedback and logs
GITHUB_REPO_URL = "https://github.com/MrMayami/AIM.git"

def log(message):
    print(message)
    logger.info(message)

def setup_python(verbose=False):
    log("Setting up Python...")
    try:
        subprocess.run(["python", "--version"], check=True, capture_output=verbose)
        log("Python is already installed.")
    except FileNotFoundError:
        log("Python is not installed.")
        exit(1)

def create_virtualenv(verbose=False):
    log("Creating a virtual environment...")
    try:
        subprocess.run(["python", "-m", "venv", "venv"], check=True, capture_output=verbose)
        log("Virtual environment created successfully.")
    except subprocess.CalledProcessError:
        log("Failed to create virtual environment.")
        exit(1)

    log("Activating virtual environment...")
    if platform.system() == "Windows":
        activate_script = os.path.join("venv", "Scripts", "activate")
    elif platform.system() == "Linux" or platform.system() == "Darwin":
        activate_script = os.path.join("venv", "bin", "activate")
    else:
        log("Unsupported platform.")
        exit(1)

    try:
        subprocess.run([activate_script], shell=True, check=True, capture_output=verbose)
        log("Virtual environment activated successfully.")
    except subprocess.CalledProcessError:
        log("Failed to activate virtual environment.")
        exit(1)

def create_project_structure(verbose=False):
    log("Creating project structure...")
    directories = ["app", "app/static", "app/templates"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    log("Project structure created successfully.")

    # Create __init__.py in app directory
    with open("../app/__init__.py", "w") as f:
        f.write("# This file initializes the app package.")

    # Create routes.py in app directory
    with open("../app/routes.py", "w") as f:
        f.write("# This file defines the application routes.")

    # Create run.py in project root
    with open("../run.py", "w") as f:
        f.write("# This file is used to run the application.")

def install_flask(verbose=False):
    log("Installing Flask...")
    try:
        subprocess.run(["pip", "install", "Flask"], check=True, capture_output=verbose)
        log("Flask installed successfully.")
    except subprocess.CalledProcessError:
        log("Failed to install Flask.")
        exit(1)

def install_pyyaml(verbose=False):
    log("Installing PyYAML...")
    try:
        subprocess.run(["pip", "install", "pyyaml"], check=True, capture_output=verbose)
        log("PyYAML installed successfully.")
    except subprocess.CalledProcessError:
        log("Failed to install PyYAML.")
        exit(1)

def create_workflow_file(verbose=False):
    log("Creating workflow file...")
    os.makedirs(".github/workflows", exist_ok=True)
    workflow_content = """
name: CI/CD Pipeline

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v2

    - name: Setup Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.x

    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest

    - name: Run tests
      run: pytest --collect-only

    - name: Build and Deploy
      run: python aim_flask.py :setup
"""
    with open("../.github/workflows/ci-cd.yml", "w") as wf:
        wf.write(workflow_content)
    log("Workflow file created successfully.")

def print_help():
    help_text = """
    AIM CLI - Environment Setup and Installation

    Available Commands:
    aim:setup        - Setup the environment for AIM
    aim:help         - Show this help message
    aim:verbose      - Enable verbose mode

    Usage:
    To setup the environment, run:
    aim:setup

    To enable verbose mode, run:
    aim:verbose

    For help, run:
    aim:help
    """
    print(help_text)

def integrate_bootstrap(verbose=False):
    log("Bootstrap integration is pending. Please integrate Bootstrap manually.")

def create_requirements_file(verbose=False):
    log("Creating requirements.txt...")
    with open("../requirements.txt", "w") as f:
        f.write("# Installed dependencies\n")
        # Add other dependencies as needed
    log("requirements.txt created successfully.")

    log("Installing dependencies from requirements.txt...")
    try:
        subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True, capture_output=verbose)
        log("Dependencies installed successfully.")
    except subprocess.CalledProcessError:
        log("Failed to install dependencies.")
        exit(1)

def is_git_installed():
    try:
        subprocess.run(["git", "--version"], check=True)
        return True
    except FileNotFoundError:
        return False

def print_version():
    # print(f"AIM Flask version {__version__}")
    log(f"AIM Flask version {__version__}")

def setup_git(verbose=False):
    log("Setting up Git...")
    try:
        subprocess.run(["git", "init"], check=True, capture_output=verbose)
        subprocess.run(["git", "remote", "add", "origin", GITHUB_REPO_URL], check=True, capture_output=verbose)
        log("Git initialized and remote repository set up successfully.")
    except subprocess.CalledProcessError:
        log("Failed to set up Git.")
        exit(1)

def cli(verbose=False):                                          
    with open("../pyproject.toml", "w") as f:
        f.write(f"""
    
[build-system]
requires = ["setuptools>=42", "wheel"]
build-backend = "setuptools.build_meta"

[tool.poetry.scripts]
aim = "aim_flask:print_version"

[tool.poetry]
name = "aim_flask"
version = "{__version__}"
description = "Front-end Development Framework for UI/UX designers and Front-end developers."
authors = ["Joe Mayami <pr.mayami@gmail.com>"]

[tool.poetry.dependencies]
python = "^3.12"

    """)

def setup(verbose=False):
    log("Welcome to the AIM setup CLI.")

    setup_python(verbose=verbose)
    create_virtualenv(verbose=verbose)
    create_project_structure(verbose=verbose)
    install_flask(verbose=verbose)
    install_pyyaml(verbose=verbose)
    import yaml
    integrate_bootstrap(verbose=verbose)
    create_workflow_file(verbose=verbose)
    create_requirements_file(verbose=verbose)
    if not is_git_installed():
        setup_git(verbose=verbose)
    else:
        log("Git is already installed.")

    log("Setup completed successfully.")

def feedback(message):
    log("Saving feedback to file...")
    with open("../feedback.txt", "a") as f:
        f.write(message + "\n")
    log("Feedback saved successfully.")

    log("Pushing feedback to GitHub...")
    try:
        subprocess.run(["git", "add", "feedback.txt"], check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Added feedback"], check=True, capture_output=True)
        subprocess.run(["git", "push"], check=True, capture_output=True)
        log("Feedback pushed successfully.")
    except subprocess.CalledProcessError as e:
        log(f"Failed to push feedback to GitHub: {e}")

def print_help():
    log("Usage: aim <command>")
    log("Commands:")
    log("  version    : Version AIM environment")
    log("  setup    : Setup AIM environment")
    log("  feedback : Send feedback")
    log("  help     : Display this help message")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AIM CLI for environment setup and installation")
    parser.add_argument("command", choices=[":cli", ":version", ":setup", ":feedback", ":help", ":verbose"], help="Command to execute")
    args = parser.parse_args()

    if args.command == ":version":
        print_version()
    elif args.command == ":setup":
        setup(verbose=True)
    elif args.command == ":feedback":
        feedback_message = input("Enter your feedback message: ")
        feedback(feedback_message)
    elif args.command == ":help":
        print_help()
    elif args.command == ":verbose":
        print("Verbose mode enabled.")
        setup(verbose=True)
    elif args.command == ":cli":
        print("Verbose mode enabled.")
        cli(verbose=True)
