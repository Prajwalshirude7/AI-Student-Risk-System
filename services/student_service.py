"""
Module: student_service.py
Provides comprehensive Student Management CRUD, validation,
and connects persistent SQLite storage with custom DSA structures:
- Stack for operation undo
- Custom Hash Table for O(1) student ID lookup cache
- Binary Search Tree for score indexing and range queries
- Array Operations for sorting and filtering
"""

import json
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from database.db import get_db_connection, execute_query, execute_mutation
from dsa.stack import OperationStack
from dsa.hash_table import CustomHashTable
from dsa.bst import BinarySearchTree
from dsa.array_operations import StudentArrayOperations
from dsa.linked_list import SinglyLinkedList

# In-memory DSA state instances
operation_stack = OperationStack(max_capacity=50)
student_hash_table = CustomHashTable(initial_capacity=32)
student_bst = BinarySearchTree()
student_linked_list = SinglyLinkedList()

class StudentService:
    """Service layer managing student database operations and synchronized DSA structures."""

    @classmethod
    def sync_dsa_structures(cls, db_path=None):
        """
        Populates in-memory DSA structures (Hash Table, BST, Linked List)
        from SQLite database records.
        """
        student_hash_table.clear()
        student_bst.__init__()
        student_linked_list.clear()

        rows = execute_query(
            "SELECT * FROM students ORDER BY id ASC;",
            db_path=db_path
        )

        for row in rows:
            student_dict = dict(row)
            # 1. Custom Hash Table: student_id -> student_dict
            student_hash_table.insert(student_dict["student_id"], student_dict)
            
            # 2. Binary Search Tree: composite score / internal_marks -> student_dict
            student_bst.insert(student_dict["internal_marks"], student_dict)
            
            # 3. Linked List: dynamic sequential chain
            student_linked_list.insert_at_tail(student_dict)

    @classmethod
    def validate_student_payload(cls, data: Dict[str, Any]) -> Tuple[bool, Optional[str], Dict[str, Any]]:
        """
        Strict server-side validation for student fields.
        Returns (is_valid, error_message, cleaned_data).
        """
        name = str(data.get("name", "")).strip()
        if not name or len(name) < 2:
            return False, "Student name must be at least 2 characters long.", {}

        try:
            attendance = float(data.get("attendance", -1))
            if not (0.0 <= attendance <= 100.0):
                return False, "Attendance must be between 0.0 and 100.0%.", {}
        except (ValueError, TypeError):
            return False, "Invalid attendance percentage value.", {}

        try:
            internal_marks = float(data.get("internal_marks", -1))
            if not (0.0 <= internal_marks <= 100.0):
                return False, "Internal marks must be between 0.0 and 100.0.", {}
        except (ValueError, TypeError):
            return False, "Invalid internal marks value.", {}

        try:
            assignment_marks = float(data.get("assignment_marks", -1))
            if not (0.0 <= assignment_marks <= 100.0):
                return False, "Assignment marks must be between 0.0 and 100.0.", {}
        except (ValueError, TypeError):
            return False, "Invalid assignment marks value.", {}

        try:
            previous_percentage = float(data.get("previous_percentage", -1))
            if not (0.0 <= previous_percentage <= 100.0):
                return False, "Previous percentage must be between 0.0 and 100.0%.", {}
        except (ValueError, TypeError):
            return False, "Invalid previous percentage value.", {}

        try:
            study_hours = float(data.get("study_hours", -1))
            if not (0.0 <= study_hours <= 24.0):
                return False, "Daily study hours must be between 0.0 and 24.0.", {}
        except (ValueError, TypeError):
            return False, "Invalid study hours value.", {}

        try:
            failed_subjects = int(data.get("failed_subjects", -1))
            if failed_subjects < 0:
                return False, "Number of failed subjects must be 0 or greater.", {}
        except (ValueError, TypeError):
            return False, "Invalid failed subjects integer.", {}

        cleaned = {
            "name": name,
            "attendance": round(attendance, 2),
            "internal_marks": round(internal_marks, 2),
            "assignment_marks": round(assignment_marks, 2),
            "previous_percentage": round(previous_percentage, 2),
            "study_hours": round(study_hours, 2),
            "failed_subjects": failed_subjects,
        }
        return True, None, cleaned

    @classmethod
    def generate_next_student_id(cls, db_path=None) -> str:
        """Generates consecutive unique student ID like STU-1001."""
        row = execute_query(
            "SELECT student_id FROM students ORDER BY id DESC LIMIT 1;",
            db_path=db_path,
            fetchone=True
        )
        if not row:
            return "STU-1001"
        last_id = row["student_id"]
        try:
            num = int(last_id.split("-")[1])
            return f"STU-{num + 1}"
        except Exception:
            import random
            return f"STU-{random.randint(2000, 9999)}"

    @classmethod
    def create_student(cls, data: Dict[str, Any], db_path=None, predicted_risk: str = "Not Predicted", risk_probability: float = 0.0) -> Dict[str, Any]:
        """Creates a new student record in database and updates DSA caches."""
        is_valid, err, cleaned = cls.validate_student_payload(data)
        if not is_valid:
            raise ValueError(err)

        student_id = data.get("student_id") or cls.generate_next_student_id(db_path)
        now_ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        query = """
        INSERT INTO students (
            student_id, name, attendance, internal_marks, assignment_marks,
            previous_percentage, study_hours, failed_subjects, predicted_risk,
            risk_probability, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        params = (
            student_id, cleaned["name"], cleaned["attendance"], cleaned["internal_marks"],
            cleaned["assignment_marks"], cleaned["previous_percentage"], cleaned["study_hours"],
            cleaned["failed_subjects"], predicted_risk, risk_probability, now_ts, now_ts
        )

        res = execute_mutation(query, params, db_path=db_path)
        new_record = cls.get_student_by_id(student_id, db_path=db_path)

        # Log into Stack for undo / history
        operation_stack.push({
            "action": "CREATE",
            "student_id": student_id,
            "data": new_record,
            "timestamp": now_ts
        })

        # Update in-memory caches
        if new_record:
            student_hash_table.insert(student_id, new_record)
            student_bst.insert(new_record["internal_marks"], new_record)
            student_linked_list.insert_at_tail(new_record)

        return new_record

    @classmethod
    def get_all_students(cls, db_path=None) -> List[Dict[str, Any]]:
        """Retrieves all students from database ordered by ID descending."""
        rows = execute_query("SELECT * FROM students ORDER BY id DESC;", db_path=db_path)
        return [dict(r) for r in rows]

    @classmethod
    def get_student_by_id(cls, student_id: str, db_path=None) -> Optional[Dict[str, Any]]:
        """Retrieves a single student by student_id."""
        row = execute_query(
            "SELECT * FROM students WHERE student_id = ?;",
            (student_id.strip().upper(),),
            db_path=db_path,
            fetchone=True
        )
        return dict(row) if row else None

    @classmethod
    def update_student(cls, student_id: str, data: Dict[str, Any], db_path=None) -> Dict[str, Any]:
        """Updates student record and logs previous state into Stack."""
        old_record = cls.get_student_by_id(student_id, db_path=db_path)
        if not old_record:
            raise KeyError(f"Student {student_id} not found.")

        is_valid, err, cleaned = cls.validate_student_payload(data)
        if not is_valid:
            raise ValueError(err)

        predicted_risk = data.get("predicted_risk", old_record["predicted_risk"])
        risk_probability = float(data.get("risk_probability", old_record["risk_probability"]))
        now_ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        query = """
        UPDATE students SET
            name = ?, attendance = ?, internal_marks = ?, assignment_marks = ?,
            previous_percentage = ?, study_hours = ?, failed_subjects = ?,
            predicted_risk = ?, risk_probability = ?, updated_at = ?
        WHERE student_id = ?;
        """
        params = (
            cleaned["name"], cleaned["attendance"], cleaned["internal_marks"],
            cleaned["assignment_marks"], cleaned["previous_percentage"], cleaned["study_hours"],
            cleaned["failed_subjects"], predicted_risk, risk_probability, now_ts,
            student_id.strip().upper()
        )
        execute_mutation(query, params, db_path=db_path)
        updated_record = cls.get_student_by_id(student_id, db_path=db_path)

        # Push to undo stack
        operation_stack.push({
            "action": "UPDATE",
            "student_id": student_id,
            "previous_data": old_record,
            "new_data": updated_record,
            "timestamp": now_ts
        })

        # Resync DSA structures
        cls.sync_dsa_structures(db_path=db_path)

        return updated_record

    @classmethod
    def delete_student(cls, student_id: str, db_path=None) -> bool:
        """Deletes student record after preserving snapshot in Stack for undo."""
        record = cls.get_student_by_id(student_id, db_path=db_path)
        if not record:
            return False

        now_ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        execute_mutation(
            "DELETE FROM students WHERE student_id = ?;",
            (student_id.strip().upper(),),
            db_path=db_path
        )

        # Push deletion to Stack for safe undo
        operation_stack.push({
            "action": "DELETE",
            "student_id": student_id,
            "data": record,
            "timestamp": now_ts
        })

        # Remove from DSA structures
        student_hash_table.delete(student_id)
        student_linked_list.delete_by_id(student_id)
        # Resync BST
        cls.sync_dsa_structures(db_path=db_path)

        return True

    @classmethod
    def undo_last_operation(cls, db_path=None) -> Dict[str, Any]:
        """
        Pops the last mutation from the Stack and restores previous state in the SQLite database.
        Demonstrates practical, real-world utility of the LIFO Stack data structure.
        """
        last_op = operation_stack.pop()
        if not last_op:
            return {"success": False, "message": "No operations available in undo history."}

        action = last_op.get("action")
        student_id = last_op.get("student_id")

        if action == "DELETE":
            # Re-insert the deleted student
            data = last_op["data"]
            query = """
            INSERT INTO students (
                student_id, name, attendance, internal_marks, assignment_marks,
                previous_percentage, study_hours, failed_subjects, predicted_risk,
                risk_probability, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """
            params = (
                data["student_id"], data["name"], data["attendance"], data["internal_marks"],
                data["assignment_marks"], data["previous_percentage"], data["study_hours"],
                data["failed_subjects"], data["predicted_risk"], data["risk_probability"],
                data["created_at"], datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            execute_mutation(query, params, db_path=db_path)
            cls.sync_dsa_structures(db_path=db_path)
            return {"success": True, "message": f"Successfully restored deleted student {student_id}."}

        elif action == "CREATE":
            # Delete the newly created student
            execute_mutation("DELETE FROM students WHERE student_id = ?;", (student_id,), db_path=db_path)
            cls.sync_dsa_structures(db_path=db_path)
            return {"success": True, "message": f"Undid creation of student {student_id}."}

        elif action == "UPDATE":
            # Revert to previous_data
            prev = last_op["previous_data"]
            query = """
            UPDATE students SET
                name = ?, attendance = ?, internal_marks = ?, assignment_marks = ?,
                previous_percentage = ?, study_hours = ?, failed_subjects = ?,
                predicted_risk = ?, risk_probability = ?, updated_at = ?
            WHERE student_id = ?;
            """
            params = (
                prev["name"], prev["attendance"], prev["internal_marks"], prev["assignment_marks"],
                prev["previous_percentage"], prev["study_hours"], prev["failed_subjects"],
                prev["predicted_risk"], prev["risk_probability"], datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                student_id
            )
            execute_mutation(query, params, db_path=db_path)
            cls.sync_dsa_structures(db_path=db_path)
            return {"success": True, "message": f"Reverted updates for student {student_id}."}

        return {"success": False, "message": f"Unknown operation action {action}."}

    @classmethod
    def search_and_filter_students(
        cls,
        search_query: str = "",
        risk_filter: str = "all",
        sort_by: str = "id",
        sort_order: str = "desc",
        score_range: str = "all",
        db_path=None
    ) -> List[Dict[str, Any]]:
        """
        Flexible search and filtering combining database query, Array operations, and BST range queries.
        """
        # Ensure BST index is populated
        if len(student_bst) == 0:
            cls.sync_dsa_structures(db_path=db_path)

        all_students = cls.get_all_students(db_path=db_path)

        # 1. Search by student_id or name
        if search_query:
            q = search_query.strip().lower()
            all_students = [
                s for s in all_students
                if q in str(s["student_id"]).lower() or q in str(s["name"]).lower()
            ]

        # 2. Score Range filter powered directly by Binary Search Tree (BST) range query
        if score_range and score_range != "all":
            if score_range == "below_40":
                min_s, max_s = 0.0, 39.99
            elif score_range == "40_70":
                min_s, max_s = 40.0, 70.0
            elif score_range == "above_70":
                min_s, max_s = 70.01, 100.0
            else:
                min_s, max_s = None, None

            if min_s is not None:
                matched_from_bst = student_bst.range_search(min_s, max_s)
                matched_ids = {m["student_id"] for m in matched_from_bst}
                all_students = [s for s in all_students if s["student_id"] in matched_ids]

        # 3. Filter by risk
        if risk_filter and risk_filter.lower() != "all":
            all_students = StudentArrayOperations.filter_by_risk(all_students, risk_filter)

        # 4. Sort using custom QuickSort
        reverse = (sort_order.lower() == "desc")
        all_students = StudentArrayOperations.quick_sort(all_students, sort_key=sort_by, reverse=reverse)

        return all_students

    @classmethod
    def get_dashboard_statistics(cls, db_path=None) -> Dict[str, Any]:
        """Calculates authentic live academic and risk metrics directly from SQLite."""
        total_students_row = execute_query("SELECT COUNT(*) as count FROM students;", db_path=db_path, fetchone=True)
        total = total_students_row["count"] if total_students_row else 0

        low_risk_row = execute_query("SELECT COUNT(*) as count FROM students WHERE predicted_risk = 'Low Risk';", db_path=db_path, fetchone=True)
        low_risk = low_risk_row["count"] if low_risk_row else 0

        med_risk_row = execute_query("SELECT COUNT(*) as count FROM students WHERE predicted_risk = 'Medium Risk';", db_path=db_path, fetchone=True)
        med_risk = med_risk_row["count"] if med_risk_row else 0

        high_risk_row = execute_query("SELECT COUNT(*) as count FROM students WHERE predicted_risk = 'High Risk';", db_path=db_path, fetchone=True)
        high_risk = high_risk_row["count"] if high_risk_row else 0

        unpredicted_row = execute_query("SELECT COUNT(*) as count FROM students WHERE predicted_risk = 'Not Predicted';", db_path=db_path, fetchone=True)
        unpredicted = unpredicted_row["count"] if unpredicted_row else 0

        avg_row = execute_query(
            "SELECT AVG(attendance) as avg_att, AVG(internal_marks) as avg_int, AVG(assignment_marks) as avg_assn FROM students;",
            db_path=db_path,
            fetchone=True
        )

        avg_attendance = round(avg_row["avg_att"], 1) if avg_row and avg_row["avg_att"] is not None else 0.0
        avg_internal = round(avg_row["avg_int"], 1) if avg_row and avg_row["avg_int"] is not None else 0.0
        avg_assignment = round(avg_row["avg_assn"], 1) if avg_row and avg_row["avg_assn"] is not None else 0.0

        # At risk students needing support (High Risk or low attendance)
        at_risk_students = execute_query(
            """
            SELECT * FROM students 
            WHERE predicted_risk = 'High Risk' OR attendance < 65.0 OR failed_subjects > 0
            ORDER BY failed_subjects DESC, attendance ASC LIMIT 8;
            """,
            db_path=db_path
        )

        recent_predictions = execute_query(
            "SELECT * FROM predictions ORDER BY id DESC LIMIT 5;",
            db_path=db_path
        )

        return {
            "total_students": total,
            "low_risk": low_risk,
            "medium_risk": med_risk,
            "high_risk": high_risk,
            "unpredicted": unpredicted,
            "avg_attendance": avg_attendance,
            "avg_internal_marks": avg_internal,
            "avg_assignment_marks": avg_assignment,
            "at_risk_students": [dict(s) for s in at_risk_students],
            "recent_predictions": [dict(p) for p in recent_predictions]
        }
