"""
Module: stack.py
Demonstrates Stack (Last-In, First-Out) data structure.
Applied in the system for tracking administrative mutations and executing safe Undo operations.

Time Complexities:
- Push: O(1)
- Pop: O(1)
- Peek: O(1)
- Is Empty: O(1)
- Size: O(1)
Space Complexity:
- O(M) where M is the maximum history depth.
"""

from typing import Any, Dict, List, Optional
import copy

class OperationStack:
    """
    Stack implementation designed to store mutation snapshots for audit and undo capabilities.
    """

    def __init__(self, max_capacity: int = 50):
        self._items: List[Dict[str, Any]] = []
        self._max_capacity: int = max_capacity

    def is_empty(self) -> bool:
        """Checks whether the stack contains any operations. Time Complexity: O(1)."""
        return len(self._items) == 0

    def push(self, operation: Dict[str, Any]) -> None:
        """
        Pushes an operation record onto the top of the stack.
        Evicts oldest record if exceeding max_capacity.
        Time Complexity: O(1).
        """
        if len(self._items) >= self._max_capacity:
            self._items.pop(0)  # Evict oldest to preserve memory
        self._items.append(copy.deepcopy(operation))

    def pop(self) -> Optional[Dict[str, Any]]:
        """
        Removes and returns the most recent operation from the top of the stack.
        Time Complexity: O(1).
        """
        if self.is_empty():
            return None
        return self._items.pop()

    def peek(self) -> Optional[Dict[str, Any]]:
        """
        Returns the top operation without removing it.
        Time Complexity: O(1).
        """
        if self.is_empty():
            return None
        return copy.deepcopy(self._items[-1])

    def size(self) -> int:
        """Returns the current number of operations in the stack. Time Complexity: O(1)."""
        return len(self._items)

    def get_history(self) -> List[Dict[str, Any]]:
        """
        Returns all stored operations in reverse chronological order (most recent first).
        Time Complexity: O(N).
        """
        return list(reversed(self._items))

    def clear(self) -> None:
        """Clears all stored operations. Time Complexity: O(1)."""
        self._items.clear()
