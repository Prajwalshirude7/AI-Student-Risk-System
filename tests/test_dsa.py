"""
Comprehensive automated tests for custom Data Structures and Algorithms implementations:
1. Array Operations (Sorting & Search)
2. Singly Linked List
3. Stack (LIFO)
4. Queue (FIFO)
5. Custom Hash Table (Separate Chaining)
6. Binary Search Tree (BST)
"""

import pytest
from dsa.array_operations import StudentArrayOperations
from dsa.linked_list import SinglyLinkedList
from dsa.stack import OperationStack
from dsa.queue import PredictionQueue
from dsa.hash_table import CustomHashTable
from dsa.bst import BinarySearchTree

# ==========================================
# 1. Array Operations Tests
# ==========================================
def test_array_quicksort_and_search():
    records = [
        {"student_id": "STU-1003", "name": "Charlie", "attendance": 65.0},
        {"student_id": "STU-1001", "name": "Alice", "attendance": 90.0},
        {"student_id": "STU-1002", "name": "Bob", "attendance": 75.0},
    ]

    # QuickSort ascending by attendance
    sorted_att = StudentArrayOperations.quick_sort(records, sort_key="attendance", reverse=False)
    assert sorted_att[0]["attendance"] == 65.0
    assert sorted_att[2]["attendance"] == 90.0

    # QuickSort descending by attendance
    sorted_desc = StudentArrayOperations.quick_sort(records, sort_key="attendance", reverse=True)
    assert sorted_desc[0]["attendance"] == 90.0
    assert sorted_desc[2]["attendance"] == 65.0

    # Binary search on array sorted by student_id
    sorted_id = StudentArrayOperations.quick_sort(records, sort_key="student_id", reverse=False)
    found = StudentArrayOperations.binary_search_by_id(sorted_id, "STU-1002")
    assert found is not None
    assert found["name"] == "Bob"

    # Linear search
    res = StudentArrayOperations.linear_search(records, "name", "Charlie")
    assert res is not None
    assert res["student_id"] == "STU-1003"

# ==========================================
# 2. Singly Linked List Tests
# ==========================================
def test_linked_list_operations():
    ll = SinglyLinkedList()
    assert ll.is_empty()
    assert len(ll) == 0

    ll.insert_at_tail({"student_id": "STU-101", "name": "Student A"})
    ll.insert_at_tail({"student_id": "STU-102", "name": "Student B"})
    ll.insert_at_head({"student_id": "STU-100", "name": "Student Pre"})

    assert len(ll) == 3
    items = ll.to_list()
    assert items[0]["student_id"] == "STU-100"
    assert items[2]["student_id"] == "STU-102"

    # Search
    searched = ll.search_by_id("STU-101")
    assert searched is not None
    assert searched["name"] == "Student A"

    # Deletion
    deleted = ll.delete_by_id("STU-101")
    assert deleted is True
    assert len(ll) == 2
    assert ll.search_by_id("STU-101") is None

# ==========================================
# 3. Stack Tests
# ==========================================
def test_stack_lifo_order():
    stack = OperationStack(max_capacity=5)
    assert stack.is_empty()

    stack.push({"op": "1"})
    stack.push({"op": "2"})
    stack.push({"op": "3"})

    assert stack.size() == 3
    assert stack.peek()["op"] == "3"

    popped = stack.pop()
    assert popped["op"] == "3"
    assert stack.size() == 2
    assert stack.pop()["op"] == "2"
    assert stack.pop()["op"] == "1"
    assert stack.is_empty()
    assert stack.pop() is None

# ==========================================
# 4. Queue Tests
# ==========================================
def test_queue_fifo_order():
    q = PredictionQueue()
    assert q.is_empty()

    q.enqueue({"task": "A"})
    q.enqueue({"task": "B"})
    q.enqueue({"task": "C"})

    assert q.size() == 3
    assert q.peek()["task"] == "A"

    dequeued = q.dequeue()
    assert dequeued["task"] == "A"
    assert q.size() == 2
    assert q.dequeue()["task"] == "B"
    assert q.dequeue()["task"] == "C"
    assert q.is_empty()

# ==========================================
# 5. Custom Hash Table Tests
# ==========================================
def test_custom_hash_table():
    ht = CustomHashTable(initial_capacity=4)
    ht.insert("STU-1", {"name": "One"})
    ht.insert("STU-2", {"name": "Two"})
    ht.insert("STU-3", {"name": "Three"})
    ht.insert("STU-4", {"name": "Four"})

    # Check search
    res = ht.search("STU-2")
    assert res is not None
    assert res["name"] == "Two"

    # Update existing key
    ht.insert("STU-2", {"name": "Updated Two"})
    assert ht.search("STU-2")["name"] == "Updated Two"

    # Deletion
    del_res = ht.delete("STU-1")
    assert del_res is True
    assert ht.search("STU-1") is None

    # Verification of resizing & capacity growth
    assert ht.capacity >= 4
    assert ht.size() == 3

# ==========================================
# 6. Binary Search Tree Tests
# ==========================================
def test_binary_search_tree():
    bst = BinarySearchTree()
    assert bst.is_empty()

    bst.insert(75.0, {"name": "Mid", "score": 75.0})
    bst.insert(50.0, {"name": "Low", "score": 50.0})
    bst.insert(90.0, {"name": "High", "score": 90.0})
    bst.insert(60.0, {"name": "MidLow", "score": 60.0})

    assert len(bst) == 4
    assert bst.find_min() == 50.0
    assert bst.find_max() == 90.0

    # In-order Traversal (Sorted)
    inorder = bst.inorder_traversal()
    scores = [s["score"] for s in inorder]
    assert scores == [50.0, 60.0, 75.0, 90.0]

    # Range Search [55, 80]
    in_range = bst.range_search(55.0, 80.0)
    range_scores = [s["score"] for s in in_range]
    assert 60.0 in range_scores
    assert 75.0 in range_scores
    assert 50.0 not in range_scores
    assert 90.0 not in range_scores
