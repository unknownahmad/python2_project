import sys
import os

# Gets the absolute path of the current file's directory.
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Adds the project root to Python's import path so modules can be imported easily.
sys.path.insert(0, PROJECT_ROOT)
