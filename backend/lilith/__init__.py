"""
----------------------
Main logic for backend Lilith operations
----------------------
"""

from .answer_pipeline import lilith_process_answer
from .core import Core

__all__ = [
    "lilith_process_answer",
    "Core"
]