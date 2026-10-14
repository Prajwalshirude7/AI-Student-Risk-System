"""
Module: queue.py
Demonstrates Queue (First-In, First-Out) data structure.
Applied in the system for buffering and processing prediction tasks in arrival sequence.

Time Complexities:
- Enqueue: O(1) amortized
- Dequeue: O(1) (with collections.deque or head pointer)
- Peek: O(1)
- Is Empty: O(1)
- Size: O(1)
Space Complexity:
- O(N) where N is queue length.
"""

from collections import deque
from typing import Any, Dict, List, Optional
import copy

class PredictionQueue:
    """
    Queue implementation for managing and processing batch prediction tasks in strict FIFO order.
    """

    def __init__(self):
        self._queue: deque = deque()

    def is_empty(self) -> bool:
        """Checks if queue is empty. Time Complexity: O(1)."""
        return len(self._queue) == 0

    def enqueue(self, item: Dict[str, Any]) -> None:
        """
        Inserts a prediction request at the back of the queue.
        Time Complexity: O(1).
        """
        self._queue.append(copy.deepcopy(item))

    def dequeue(self) -> Optional[Dict[str, Any]]:
        """
        Removes and returns the front item of the queue.
        Time Complexity: O(1).
        """
        if self.is_empty():
            return None
        return self._queue.popleft()

    def peek(self) -> Optional[Dict[str, Any]]:
        """
        Returns the front item without removing it.
        Time Complexity: O(1).
        """
        if self.is_empty():
            return None
        return copy.deepcopy(self._queue[0])

    def size(self) -> int:
        """Returns the number of elements in queue. Time Complexity: O(1)."""
        return len(self._queue)

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Returns all queued items in FIFO sequence.
        Time Complexity: O(N).
        """
        return list(self._queue)

    def clear(self) -> None:
        """Clears the queue. Time Complexity: O(1)."""
        self._queue.clear()
