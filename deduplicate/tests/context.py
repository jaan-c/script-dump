"""
Give relative context for easy import in tests.

from .context import deduplicate
"""

import os
import sys

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_dir)

from deduplicate import *
