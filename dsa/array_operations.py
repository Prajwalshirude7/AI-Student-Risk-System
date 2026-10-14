"""
Module: array_operations.py
Demonstrates Array / List algorithms on student records.

Time Complexities:
- Insertion: O(1) amortized
- Linear Search: O(N)
- Binary Search (on sorted array): O(log N)
- QuickSort: O(N log N) average, O(N^2) worst-case
- Filtering: O(N)
Space Complexity:
- QuickSort: O(log N) auxiliary stack space
- Filtering: O(K) where K is number of matched records
"""

from typing import List, Dict, Any, Optional

class StudentArrayOperations:
    """Provides genuine algorithmic operations on student record collections."""

    @staticmethod
    def insert(records: List[Dict[str, Any]], student: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Inserts a new student record into the array.
        Time Complexity: O(1) amortized.
        """
        records.append(student)
        return records

    @staticmethod
    def linear_search(records: List[Dict[str, Any]], field: str, value: Any) -> Optional[Dict[str, Any]]:
        """
        Performs linear search over student records.
        Time Complexity: O(N).
        """
        target = str(value).strip().lower()
        for record in records:
            if str(record.get(field, "")).strip().lower() == target:
                return record
        return None

    @staticmethod
    def binary_search_by_id(sorted_records: List[Dict[str, Any]], student_id: str) -> Optional[Dict[str, Any]]:
        """
        Performs binary search by student_id on pre-sorted array.
        Time Complexity: O(log N).
        Requires sorted_records to be ordered ascending by student_id.
        """
        low = 0
        high = len(sorted_records) - 1
        target = student_id.strip().upper()

        while low <= high:
            mid = (low + high) // 2
            mid_val = str(sorted_records[mid].get("student_id", "")).strip().upper()

            if mid_val == target:
                return sorted_records[mid]
            elif mid_val < target:
                low = mid + 1
            else:
                high = mid - 1
        return None

    @staticmethod
    def filter_by_risk(records: List[Dict[str, Any]], risk_level: str) -> List[Dict[str, Any]]:
        """
        Filters students by predicted risk category.
        Time Complexity: O(N).
        """
        target = risk_level.strip().lower()
        if target in ("all", ""):
            return records
        return [r for r in records if str(r.get("predicted_risk", "")).strip().lower() == target]

    @staticmethod
    def filter_by_attendance_range(records: List[Dict[str, Any]], min_att: float, max_att: float) -> List[Dict[str, Any]]:
        """
        Filters students with attendance between min_att and max_att.
        Time Complexity: O(N).
        """
        return [r for r in records if min_att <= float(r.get("attendance", 0)) <= max_att]

    @staticmethod
    def quick_sort(records: List[Dict[str, Any]], sort_key: str = "name", reverse: bool = False) -> List[Dict[str, Any]]:
        """
        Sorts student records using an algorithmic QuickSort implementation.
        Time Complexity: O(N log N) average, O(N^2) worst case.
        Auxiliary Space: O(log N).
        """
        items = list(records)
        if len(items) <= 1:
            return items

        def _get_val(rec):
            val = rec.get(sort_key)
            if val is None:
                return 0 if sort_key in ("attendance", "internal_marks", "assignment_marks", "previous_percentage", "study_hours", "failed_subjects") else ""
            if sort_key in ("attendance", "internal_marks", "assignment_marks", "previous_percentage", "study_hours", "failed_subjects"):
                try:
                    return float(val)
                except (ValueError, TypeError):
                    return 0.0
            return str(val).lower()

        def _quicksort_helper(arr, low, high):
            if low < high:
                pi = _partition(arr, low, high)
                _quicksort_helper(arr, low, pi - 1)
                _quicksort_helper(arr, pi + 1, high)

        def _partition(arr, low, high):
            pivot = _get_val(arr[high])
            i = low - 1
            for j in range(low, high):
                curr = _get_val(arr[j])
                condition = (curr > pivot) if reverse else (curr < pivot)
                if condition:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            return i + 1

        _quicksort_helper(items, 0, len(items) - 1)
        return items
