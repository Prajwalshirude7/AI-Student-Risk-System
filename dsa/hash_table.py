"""
Module: hash_table.py
Demonstrates Custom Hash Table with Separate Chaining collision handling and dynamic resizing.
Applied in the system for high-performance O(1) average lookup by student_id.

Time Complexities:
- Insert: O(1) average, O(N) worst case (if all keys collide)
- Search: O(1) average, O(N) worst case
- Delete: O(1) average, O(N) worst case
- Resize / Rehash: O(N)
Space Complexity:
- O(Capacity + N)
"""

from typing import Any, List, Optional, Tuple

class HashNode:
    """Entry node inside a bucket linked chain."""
    def __init__(self, key: str, value: Any):
        self.key: str = key
        self.value: Any = value
        self.next: Optional['HashNode'] = None

    def __repr__(self):
        return f"HashNode({self.key})"


class CustomHashTable:
    """
    Custom Hash Table utilizing polynomial rolling hash, separate chaining,
    and automatic capacity doubling when load factor exceeds 0.75.
    """

    INITIAL_CAPACITY = 16
    LOAD_FACTOR_THRESHOLD = 0.75

    def __init__(self, initial_capacity: int = INITIAL_CAPACITY):
        self.capacity: int = max(4, initial_capacity)
        self.buckets: List[Optional[HashNode]] = [None] * self.capacity
        self.count: int = 0

    def _hash(self, key: str) -> int:
        """
        Polynomial rolling hash function.
        hash = (s[0]*31^(k-1) + s[1]*31^(k-2) + ... + s[k-1]) % capacity
        """
        p = 31
        hash_val = 0
        for char in str(key):
            hash_val = (hash_val * p + ord(char)) % self.capacity
        return hash_val

    def load_factor(self) -> float:
        """Returns the current load factor (count / capacity)."""
        return self.count / self.capacity

    def _resize(self, new_capacity: int) -> None:
        """
        Resizes the bucket array and re-hashes all existing entries.
        Time Complexity: O(N).
        """
        old_buckets = self.buckets
        self.capacity = new_capacity
        self.buckets = [None] * new_capacity
        self.count = 0

        for head in old_buckets:
            curr = head
            while curr:
                self.insert(curr.key, curr.value)
                curr = curr.next

    def insert(self, key: str, value: Any) -> None:
        """
        Inserts or updates a key-value pair.
        Automatically rehashes if load factor threshold is exceeded.
        Time Complexity: O(1) average.
        """
        if self.load_factor() >= self.LOAD_FACTOR_THRESHOLD:
            self._resize(self.capacity * 2)

        idx = self._hash(key)
        head = self.buckets[idx]

        # Check if key already exists, update value
        curr = head
        while curr:
            if curr.key == key:
                curr.value = value
                return
            curr = curr.next

        # Insert new node at bucket head
        new_node = HashNode(key, value)
        new_node.next = self.buckets[idx]
        self.buckets[idx] = new_node
        self.count += 1

    def search(self, key: str) -> Optional[Any]:
        """
        Searches for a key and returns associated value.
        Time Complexity: O(1) average.
        """
        idx = self._hash(key)
        curr = self.buckets[idx]
        while curr:
            if curr.key == key:
                return curr.value
            curr = curr.next
        return None

    def contains(self, key: str) -> bool:
        """Returns True if key is found, False otherwise."""
        return self.search(key) is not None

    def delete(self, key: str) -> bool:
        """
        Deletes key-value pair from hash table.
        Time Complexity: O(1) average.
        """
        idx = self._hash(key)
        curr = self.buckets[idx]
        prev = None

        while curr:
            if curr.key == key:
                if prev is None:
                    self.buckets[idx] = curr.next
                else:
                    prev.next = curr.next
                self.count -= 1
                return True
            prev = curr
            curr = curr.next
        return False

    def size(self) -> int:
        """Returns total number of items stored."""
        return self.count

    def get_all(self) -> List[Tuple[str, Any]]:
        """Returns all (key, value) pairs stored in hash table."""
        items = []
        for head in self.buckets:
            curr = head
            while curr:
                items.append((curr.key, curr.value))
                curr = curr.next
        return items

    def clear(self) -> None:
        """Clears all stored entries."""
        self.buckets = [None] * self.capacity
        self.count = 0
