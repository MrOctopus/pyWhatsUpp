import os

# We get the top_dir using the __file__ variable to ensure
# the CWD does not affect pathing
TOP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
INPUT_DIR = os.path.join(TOP_DIR, 'input')
OUTPUT_DIR = os.path.join(TOP_DIR, 'output')

