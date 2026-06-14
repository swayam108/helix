"""Safety and permission management system"""

from typing import Dict, Set, List, Optional
from enum import Enum
from dataclasses import dataclass
from helix.utils.logger import get_logger

logger = get_logger(__name__)


class PermissionLevel(Enum):
    """Permission levels"""
    DENY = 0
    READ_ONLY = 1
    EXECUTE = 2
    FULL = 3


@dataclass
class Permission:
    """Represents a single permission"""
    resource: str  # e.g., "filesystem", "network", "system_command"
    action: str    # e.g., "read", "write", "execute"
    level: PermissionLevel = PermissionLevel.DENY
    constraint: Optional[str] = None  # e.g., path constraint


class SafetyManager:
    """Manages permissions and safe execution"""

    def __init__(self):
        self.permissions: Dict[str, List[Permission]] = {}
        self.audit_log: List[Dict] = []
        self.sandbox_enabled = True
        self._init_default_permissions()

    def _init_default_permissions(self) -> None:
        """Initialize default safe permissions"""
        # By default, restrict dangerous operations
        default_permissions = {
            "automation_agent": [
                Permission("filesystem", "read", PermissionLevel.READ_ONLY),
                Permission("filesystem", "write", PermissionLevel.DENY),
                Permission("system", "execute", PermissionLevel.DENY),
            ],
            "research_agent": [
                Permission("network", "http", PermissionLevel.EXECUTE),
                Permission("filesystem", "read", PermissionLevel.READ_ONLY),
            ],
            "coder_agent": [
                Permission("code", "execute", PermissionLevel.EXECUTE),
                Permission("filesystem", "read", PermissionLevel.EXECUTE),
                Permission("filesystem", "write", PermissionLevel.EXECUTE),
            ],
        }
        
        for agent, perms in default_permissions.items():
            self.permissions[agent] = perms

    def has_permission(
        self,
        agent: str,
        resource: str,
        action: str,
        constraint: Optional[str] = None
    ) -> bool:
        """
        Check if an agent has permission for a specific action.
        """
        if agent not in self.permissions:
            logger.warning(f"Agent {agent} has no permissions defined")
            return False
        
        for perm in self.permissions[agent]:
            if perm.resource == resource and perm.action == action:
                if perm.level == PermissionLevel.DENY:
                    return False
                if constraint and perm.constraint:
                    # Check constraint match (e.g., path constraint)
                    return constraint.startswith(perm.constraint)
                return perm.level != PermissionLevel.DENY
        
        return False

    def grant_permission(
        self,
        agent: str,
        resource: str,
        action: str,
        level: PermissionLevel = PermissionLevel.EXECUTE
    ) -> None:
        """
        Grant a permission to an agent.
        """
        if agent not in self.permissions:
            self.permissions[agent] = []
        
        perm = Permission(resource, action, level)
        self.permissions[agent].append(perm)
        
        logger.info(f"Permission granted to {agent}: {resource}/{action} ({level.name})")
        self._log_audit("permission_granted", agent, resource, action, level)

    def revoke_permission(
        self,
        agent: str,
        resource: str,
        action: str
    ) -> None:
        """
        Revoke a permission from an agent.
        """
        if agent in self.permissions:
            self.permissions[agent] = [
                p for p in self.permissions[agent]
                if not (p.resource == resource and p.action == action)
            ]
            logger.info(f"Permission revoked from {agent}: {resource}/{action}")
            self._log_audit("permission_revoked", agent, resource, action)

    def sandbox_execute(self, agent: str, func, *args, **kwargs):
        """
        Execute a function in a sandboxed environment with permission checks.
        """
        if not self.sandbox_enabled:
            logger.warning("Sandbox is disabled - executing without isolation")
            return func(*args, **kwargs)
        
        # TODO: Implement actual sandboxing (e.g., using containers, processes)
        try:
            result = func(*args, **kwargs)
            self._log_audit("sandboxed_execution", agent, "success")
            return result
        except Exception as e:
            logger.error(f"Sandboxed execution failed for {agent}: {e}")
            self._log_audit("sandboxed_execution", agent, "failed", str(e))
            raise

    def _log_audit(self, action: str, agent: str = None, *details) -> None:
        """
        Log security-related events to audit log.
        """
        entry = {
            "timestamp": __import__("datetime").datetime.now().isoformat(),
            "action": action,
            "agent": agent,
            "details": details
        }
        self.audit_log.append(entry)
        if len(self.audit_log) > 10000:
            self.audit_log.pop(0)

    def get_audit_log(self, agent: Optional[str] = None, limit: int = 100) -> List[Dict]:
        """
        Retrieve audit log entries.
        """
        log = self.audit_log[-limit:]
        if agent:
            log = [e for e in log if e.get("agent") == agent]
        return log
