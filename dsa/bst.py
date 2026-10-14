"""
Module: bst.py
Demonstrates Binary Search Tree (BST) for student performance score indexing and ordered range querying.

Time Complexities:
- Insert: O(log N) average, O(N) worst-case (unbalanced)
- Search: O(log N) average, O(N) worst-case
- Deletion: O(log N) average, O(N) worst-case
- In-order Traversal (Sorted retrieval): O(N)
- Range Search [min_score, max_score]: O(K + log N) where K is matching nodes
Space Complexity:
- O(N) for tree nodes and recursion stack
"""

from typing import Any, Dict, List, Optional

class BSTNode:
    """Represents a node in the Binary Search Tree."""
    def __init__(self, key: float, data: Dict[str, Any]):
        self.key: float = float(key)
        self.records: List[Dict[str, Any]] = [data]  # Handle multiple students with same score
        self.left: Optional['BSTNode'] = None
        self.right: Optional['BSTNode'] = None

    def __repr__(self):
        return f"BSTNode(Score={self.key}, Count={len(self.records)})"


class BinarySearchTree:
    """
    Binary Search Tree indexing student records by academic score
    to enable fast sorted retrieval and range filtering.
    """

    def __init__(self):
        self.root: Optional[BSTNode] = None
        self._total_records: int = 0

    def is_empty(self) -> bool:
        """Checks if the BST has no nodes."""
        return self.root is None

    def __len__(self) -> int:
        return self._total_records

    def insert(self, score: float, data: Dict[str, Any]) -> None:
        """
        Inserts a student record keyed by their performance score.
        Time Complexity: O(log N) average, O(N) worst.
        """
        key = round(float(score), 2)
        if self.root is None:
            self.root = BSTNode(key, data)
            self._total_records += 1
            return

        curr = self.root
        while True:
            if key == curr.key:
                curr.records.append(data)
                self._total_records += 1
                return
            elif key < curr.key:
                if curr.left is None:
                    curr.left = BSTNode(key, data)
                    self._total_records += 1
                    return
                curr = curr.left
            else:
                if curr.right is None:
                    curr.right = BSTNode(key, data)
                    self._total_records += 1
                    return
                curr = curr.right

    def search(self, score: float) -> List[Dict[str, Any]]:
        """
        Searches for all students matching the exact score.
        Time Complexity: O(log N) average, O(N) worst.
        """
        key = round(float(score), 2)
        curr = self.root
        while curr:
            if key == curr.key:
                return list(curr.records)
            elif key < curr.key:
                curr = curr.left
            else:
                curr = curr.right
        return []

    def inorder_traversal(self) -> List[Dict[str, Any]]:
        """
        Traverses tree in ascending order of score (In-order: Left -> Root -> Right).
        Time Complexity: O(N).
        """
        result: List[Dict[str, Any]] = []

        def _inorder(node: Optional[BSTNode]):
            if node:
                _inorder(node.left)
                result.extend(node.records)
                _inorder(node.right)

        _inorder(self.root)
        return result

    def range_search(self, min_score: float, max_score: float) -> List[Dict[str, Any]]:
        """
        Performs bounded range query retrieving all students whose score falls within [min_score, max_score].
        Time Complexity: O(K + log N) where K is number of records within range.
        """
        result: List[Dict[str, Any]] = []

        def _range(node: Optional[BSTNode]):
            if not node:
                return
            if min_score < node.key:
                _range(node.left)
            if min_score <= node.key <= max_score:
                result.extend(node.records)
            if node.key < max_score:
                _range(node.right)

        _range(self.root)
        return result

    def find_min(self) -> Optional[float]:
        """Finds minimum score in tree. Time: O(log N) average."""
        if not self.root:
            return None
        curr = self.root
        while curr.left:
            curr = curr.left
        return curr.key

    def find_max(self) -> Optional[float]:
        """Finds maximum score in tree. Time: O(log N) average."""
        if not self.root:
            return None
        curr = self.root
        while curr.right:
            curr = curr.right
        return curr.key

    def delete(self, score: float) -> bool:
        """
        Deletes the node corresponding to score.
        Time Complexity: O(log N) average, O(N) worst.
        """
        key = round(float(score), 2)
        deleted = False

        def _delete_node(node: Optional[BSTNode], target: float) -> Optional[BSTNode]:
            nonlocal deleted
            if node is None:
                return None

            if target < node.key:
                node.left = _delete_node(node.left, target)
            elif target > node.key:
                node.right = _delete_node(node.right, target)
            else:
                deleted = True
                self._total_records -= len(node.records)
                # Node with only one child or no child
                if node.left is None:
                    return node.right
                elif node.right is None:
                    return node.left

                # Node with two children: Get the inorder successor (min in right subtree)
                succ = node.right
                while succ.left:
                    succ = succ.left
                node.key = succ.key
                node.records = succ.records
                # Delete the inorder successor
                node.right = _delete_node(node.right, succ.key)

            return node

        self.root = _delete_node(self.root, key)
        return deleted
