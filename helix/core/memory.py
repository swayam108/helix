"""Multi-level memory system for agents"""

import json
from typing import Any, Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
import sqlite3
from helix.utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class MemoryEntry:
    """Single memory entry with metadata"""
    key: str
    value: Any
    timestamp: datetime
    category: str = "general"
    ttl_seconds: Optional[int] = None  # Time to live
    importance: float = 1.0  # 0-1 scale


class Memory:
    """Unified memory system with short and long-term storage"""

    def __init__(self, db_path: str = "memory_store/helix_memory.db"):
        self.db_path = db_path
        self.short_term: Dict[str, MemoryEntry] = {}  # Fast access
        self.init_db()

    def init_db(self) -> None:
        """Initialize SQLite database for long-term storage"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS memory (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    category TEXT,
                    importance REAL,
                    created_at TIMESTAMP,
                    accessed_at TIMESTAMP,
                    ttl_seconds INTEGER
                )
            """)
            conn.commit()
            conn.close()
            logger.info(f"Memory database initialized at {self.db_path}")
        except Exception as e:
            logger.error(f"Error initializing memory database: {e}")

    def store(self, key: str, value: Any, category: str = "general",
              importance: float = 1.0, ttl_seconds: Optional[int] = None) -> None:
        """Store information in memory"""
        entry = MemoryEntry(
            key=key,
            value=value,
            timestamp=datetime.now(),
            category=category,
            ttl_seconds=ttl_seconds,
            importance=importance
        )
        self.short_term[key] = entry
        self._persist_to_db(entry)
        logger.debug(f"Stored memory: {key} (category: {category})")

    def retrieve(self, key: str) -> Optional[Any]:
        """Retrieve from memory (short-term first, then long-term)"""
        if key in self.short_term:
            entry = self.short_term[key]
            entry.timestamp = datetime.now()  # Update access time
            return entry.value
        return self._retrieve_from_db(key)

    def search(self, category: str, limit: int = 10) -> List[MemoryEntry]:
        """Search memory by category"""
        results = [e for e in self.short_term.values() if e.category == category]
        results.extend(self._search_db(category, limit))
        return sorted(results, key=lambda x: x.importance, reverse=True)[:limit]

    def _persist_to_db(self, entry: MemoryEntry) -> None:
        """Persist entry to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO memory 
                (key, value, category, importance, created_at, accessed_at, ttl_seconds)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                entry.key,
                json.dumps(entry.value, default=str),
                entry.category,
                entry.importance,
                entry.timestamp,
                datetime.now(),
                entry.ttl_seconds
            ))
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Error persisting memory: {e}")

    def _retrieve_from_db(self, key: str) -> Optional[Any]:
        """Retrieve from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM memory WHERE key = ?", (key,))
            result = cursor.fetchone()
            conn.close()
            if result:
                return json.loads(result[0])
        except Exception as e:
            logger.error(f"Error retrieving from memory: {e}")
        return None

    def _search_db(self, category: str, limit: int) -> List[MemoryEntry]:
        """Search database by category"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT key, value, category, importance, created_at, ttl_seconds
                FROM memory WHERE category = ? ORDER BY importance DESC LIMIT ?
            """, (category, limit))
            results = []
            for row in cursor.fetchall():
                results.append(MemoryEntry(
                    key=row[0],
                    value=json.loads(row[1]),
                    category=row[2],
                    importance=row[3],
                    timestamp=datetime.fromisoformat(row[4]),
                    ttl_seconds=row[5]
                ))
            conn.close()
            return results
        except Exception as e:
            logger.error(f"Error searching memory: {e}")
        return []

    def clear(self, category: Optional[str] = None) -> None:
        """Clear memory entries"""
        if category:
            self.short_term = {k: v for k, v in self.short_term.items() if v.category != category}
        else:
            self.short_term.clear()
        logger.info(f"Memory cleared{'(category: ' + category + ')' if category else ''}")
