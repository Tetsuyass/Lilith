"""
----------------------
Main logic for backend Lilith operations
----------------------
"""

from .answer_pipeline import lilith_process_answer
from .core import Core
from .core_instance import lilith_core

__all__ = [
    "lilith_process_answer",
    "Core",
    "lilith_core"
]