"""
Module: linked_list.py
Demonstrates Singly Linked List data structure for dynamic student record management.

Time Complexities:
- Insertion at Head: O(1)
- Insertion at Tail: O(N) (or O(1) with tail pointer)
- Deletion by ID: O(N)
- Search: O(N)
- Traversal (to_list): O(N)
Space Complexity:
- O(N) auxiliary memory for pointers
"""

from typing import Dict, Any, Optional, List

class StudentNode:
    """Represents a node in a Singly Linked List holding student data."""
    def __init__(self, data: Dict[str, Any], next_node: Optional['StudentNode'] = None):
        self.data = data
        self.next = next_node

    def __repr__(self):
        return f"StudentNode({self.data.get('student_id', 'Unknown')})"


class SinglyLinkedList:
    """Custom Singly Linked List for sequential student record operations."""

    def __init__(self):
        self.head: Optional[StudentNode] = None
        self._size: int = 0

    def is_empty(self) -> bool:
        """Check if the linked list is empty."""
        return self.head is None

    def __len__(self) -> int:
        """Return the count of nodes in the linked list."""
        return self._size

    def insert_at_head(self, data: Dict[str, Any]) -> None:
        """
        Inserts a student node at the head of the list.
        Time Complexity: O(1).
        """
        new_node = StudentNode(data, next_node=self.head)
        self.head = new_node
        self._size += 1

    def insert_at_tail(self, data: Dict[str, Any]) -> None:
        """
        Inserts a student node at the end of the list.
        Time Complexity: O(N).
        """
        new_node = StudentNode(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self._size += 1

    def search_by_id(self, student_id: str) -> Optional[Dict[str, Any]]:
        """
        Searches for a student by ID.
        Time Complexity: O(N).
        """
        target = student_id.strip().upper()
        current = self.head
        while current:
            if str(current.data.get("student_id", "")).strip().upper() == target:
                return current.data
            current = current.next
        return None

    def search_by_name(self, name: str) -> List[Dict[str, Any]]:
        """
        Searches for students matching given name substring.
        Time Complexity: O(N).
        """
        query = name.strip().lower()
        results = []
        current = self.head
        while current:
            if query in str(current.data.get("name", "")).strip().lower():
                results.append(current.data)
            current = current.next
        return results

    def delete_by_id(self, student_id: str) -> bool:
        """
        Deletes the first student node matching the student_id.
        Time Complexity: O(N). Returns True if deleted, False if not found.
        """
        target = student_id.strip().upper()
        if self.head is None:
            return False

        if str(self.head.data.get("student_id", "")).strip().upper() == target:
            self.head = self.head.next
            self._size -= 1
            return True

        current = self.head
        while current.next:
            if str(current.next.data.get("student_id", "")).strip().upper() == target:
                current.next = current.next.next
                self._size -= 1
                return True
            current = current.next

        return False

    def to_list(self) -> List[Dict[str, Any]]:
        """
        Traverses the linked list and converts to standard Python list of dicts.
        Time Complexity: O(N).
        """
        records = []
        current = self.head
        while current:
            records.append(dict(current.data))
            current = current.next
        return records

    def clear(self) -> None:
        """Resets the list."""
        self.head = None
        self._size = 0
