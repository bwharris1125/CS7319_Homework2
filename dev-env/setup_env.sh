#!/bin/bash
# setup_env.sh: Set up Python virtual environment and install dependencies for CS7319 Homework 2
# Usage: bash setup_env.sh
# *Gitlab Copilot Used to assist in creation of this script*

set -e

# Name of the virtual environment directory
VENV_DIR=".venv"

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 and rerun this script."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment in $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
else
    echo "Virtual environment already exists in $VENV_DIR."
    exit 1
fi

# Activate the virtual environment
source "$VENV_DIR/bin/activate"

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing required Python packages..."
pip install notebook pandas numpy matplotlib

echo "Setup complete! To activate the environment, run:"
echo "  source $VENV_DIR/bin/activate"
echo "To start Jupyter Notebook, run:"
echo "  jupyter notebook"
