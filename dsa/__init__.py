"""
Data Structures and Algorithms Package for AI Student Risk System.
Provides custom educational and operational implementations of:
- Array Operations (traversal, filter, sort)
- Singly Linked List (dynamic student sequence)
- Stack (LIFO undo/history mechanism)
- Queue (FIFO prediction processing buffer)
- Custom Hash Table (separate chaining O(1) average lookup)
- Binary Search Tree (ordered score indexing and range search)
"""

from .array_operations import StudentArrayOperations
from .linked_list import SinglyLinkedList, StudentNode
from .stack import OperationStack
from .queue import PredictionQueue
from .hash_table import CustomHashTable
from .bst import BinarySearchTree, BSTNode

__all__ = [
    "StudentArrayOperations",
    "SinglyLinkedList",
    "StudentNode",
    "OperationStack",
    "PredictionQueue",
    "CustomHashTable",
    "BinarySearchTree",
    "BSTNode",
]
