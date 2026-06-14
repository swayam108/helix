"""System resource monitoring and management"""

import psutil
from dataclasses import dataclass
from typing import Optional
from helix.utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class ResourceUsage:
    """Snapshot of current resource usage"""
    cpu_percent: float
    memory_percent: float
    memory_mb: float
    disk_percent: float
    gpu_memory_used: Optional[float] = None
    gpu_memory_available: Optional[float] = None


class ResourceMonitor:
    """Monitor and manage system resources"""

    def __init__(self, max_memory_percent: float = 80.0, max_cpu_percent: float = 90.0):
        self.max_memory_percent = max_memory_percent
        self.max_cpu_percent = max_cpu_percent
        self.process = psutil.Process()

    def get_usage(self) -> ResourceUsage:
        """Get current resource usage"""
        cpu = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        return ResourceUsage(
            cpu_percent=cpu,
            memory_percent=memory.percent,
            memory_mb=memory.used / (1024 ** 2),
            disk_percent=disk.percent,
        )

    def is_resource_constrained(self) -> bool:
        """Check if system is resource constrained"""
        usage = self.get_usage()
        return (
            usage.cpu_percent > self.max_cpu_percent or
            usage.memory_percent > self.max_memory_percent
        )

    def get_available_capacity(self) -> float:
        """Get available capacity as a percentage (0-1)"""
        usage = self.get_usage()
        cpu_available = max(0, (100 - usage.cpu_percent) / 100)
        memory_available = max(0, (100 - usage.memory_percent) / 100)
        return min(cpu_available, memory_available)

    def log_usage(self) -> None:
        """Log current resource usage"""
        usage = self.get_usage()
        logger.info(
            f"Resources - CPU: {usage.cpu_percent:.1f}%, "
            f"Memory: {usage.memory_percent:.1f}% ({usage.memory_mb:.0f}MB), "
            f"Disk: {usage.disk_percent:.1f}%"
        )
