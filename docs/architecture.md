# System Architecture & Technical Specification

## AI-Based Student Performance & Risk Prediction System

---

## 1. Architectural Style: Layered Modular Architecture

The system implements a classic 4-tier clean architectural pattern ensuring complete separation of concerns:

```text
+-------------------------------------------------------------------+
|                        Presentation Layer                         |
|   HTML5 + CSS3 + Bootstrap 5.3 + Chart.js (Responsive Dashboard)   |
+----------------------------------+--------------------------------+
                                   | HTTP Requests / JSON Payloads
+----------------------------------v--------------------------------+
|                        Application Layer                          |
|    Flask Web Framework (Routing, Session, Request Dispatching)     |
+----------------------------------+--------------------------------+
                                   | Service Calls
+----------------------------------v--------------------------------+
|                          Service Layer                            |
|  - StudentService (CRUD, Validation, DSA Sync, Live Statistics)   |
|  - PredictionService (ML Pipeline, Batch FIFO Queue Processing)   |
|  - RecommendationService (Non-judgmental Guidance Engine)         |
+------------------+-------------------------------+----------------+
                   |                               |
                   v                               v
+------------------+------------+   +--------------+----------------+
|   Data Structures Layer (DSA) |   |  Machine Learning Layer (ML)  |
|  - Array / QuickSort          |   |  - Scikit-Learn DecisionTree  |
|  - Singly Linked List         |   |  - Feature Extraction (6 Dims)|
|  - Stack (Undo Engine)        |   |  - Probability Calibration    |
|  - Queue (FIFO Buffer)        |   |  - Model Persistence (.pkl)   |
|  - Custom Hash Table (O(1))   |   +-------------------------------+
|  - Binary Search Tree (BST)   |
+------------------+------------+
                   |
                   v
+------------------+------------------------------------------------+
|                        Data Persistence Layer                     |
|           SQLite3 Relational Database Engine (students.db)        |
+-------------------------------------------------------------------+
```

---

## 2. Component Interaction & Flow

### 2.1 Student Registration & DSA Synchronization
1. Client submits student attributes via `/students/new`.
2. `StudentService.validate_student_payload` enforces type and range bounds ($0 \le \text{Marks} \le 100$, $0 \le \text{Hours} \le 24$).
3. Parameterized SQL insert executes into the `students` SQLite table.
4. Mutation record is pushed to `OperationStack` (LIFO).
5. In-memory data structures are immediately updated:
   - `student_hash_table.insert(student_id, student)`: Enables instant $O(1)$ lookup cache.
   - `student_bst.insert(internal_marks, student)`: Updates ordered score index.
   - `student_linked_list.insert_at_tail(student)`: Updates dynamic chain.

### 2.2 Machine Learning Inference Flow
1. Client triggers prediction on `/predict` or from a student's profile page.
2. `PredictionService` extracts the 6 ordered features: `attendance`, `internal_marks`, `assignment_marks`, `previous_percentage`, `study_hours`, `failed_subjects`.
3. `RiskPredictor` passes a 1-row Pandas DataFrame to the pre-loaded Scikit-Learn Decision Tree (`risk_model.pkl`).
4. Multi-class probabilities are computed using `predict_proba()`.
5. Key contributing academic vulnerabilities are identified.
6. `AcademicRecommendationService` pairs the risk classification with supportive guidance.
7. Diagnostic record is persisted to SQLite's `predictions` table for historical audit.

### 2.3 Undo Mutation Execution Flow
1. User clicks "Undo Last Action" on the Student Management page.
2. `StudentService.undo_last_operation()` pops the topmost action from `OperationStack`.
3. If the action was `DELETE`, the student record is restored to SQLite.
4. If the action was `CREATE`, the record is removed from SQLite.
5. If the action was `UPDATE`, previous column values are reapplied.
6. In-memory DSA caches are refreshed via `sync_dsa_structures()`.

---

## 3. Security & Reliability Highlights
- **SQL Injection Prevention:** 100% of queries use parameter substitution (`?`).
- **XSS Protection:** Automatic Jinja2 contextual HTML escaping.
- **Data Persistence:** SQLite database persists across application restarts; schema initialization preserves existing records.
- **Local Network Safety:** Bound to `127.0.0.1:5000` with debug mode controlled via configuration.
