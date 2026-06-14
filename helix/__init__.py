"""HELIX: Local-First Multi-Agent AI Operating System"""

__version__ = "0.1.0"
__author__ = "HELIX Contributors"
__license__ = "MIT"

from helix.core.commander import Commander
from helix.core.executor import Executor
from helix.utils.logger import setup_logger

__all__ = ["Commander", "Executor", "setup_logger"]
