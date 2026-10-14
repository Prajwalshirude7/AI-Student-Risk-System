# AI-Based Student Performance & Risk Prediction System

**B.Tech Second-Year Mini-Project**  
*Integrating Data Structures & Algorithms, Machine Learning, Database Management, and Web Development.*

---

## 1. Project Overview

The **AI-Based Student Performance & Risk Prediction System** is an educational analytics and decision-support portal designed to identify students experiencing academic vulnerability early in their semester. 

By combining classical **Data Structures & Algorithms (Array, Singly Linked List, Stack, Queue, Custom Hash Table, Binary Search Tree)** with a **Supervised Decision Tree Classifier** and **Persistent SQLite Database Management**, the application provides faculty mentors with:
1. Live diagnostic dashboards computed directly from student records.
2. Predictive academic risk classification (`Low Risk`, `Medium Risk`, `High Risk`) with multiclass probabilities.
3. Specific, non-judgmental, actionable mentorship recommendations.
4. Functional LIFO Undo capabilities and FIFO batch prediction processing.
5. Interactive educational verification console for all 6 data structures.

---

## 2. Technology Stack

- **Operating System:** Windows 10 / 11
- **Backend Language:** Python 3.11+ (Compatible with Python 3.12 & 3.13)
- **Web Framework:** Flask 3.x
- **Database Engine:** SQLite3 (Persistent SQL storage with parameterized queries)
- **Machine Learning:** Scikit-Learn (Decision Tree Classifier), Pandas, NumPy, Joblib
- **Frontend / UI:** HTML5, CSS3 (Custom Design System), Bootstrap 5.3 CDN, Chart.js 4.4 CDN
- **Automated Testing:** pytest (28 automated unit, integration, and boundary test cases)

---

## 3. Mandatory College Data Structure Mappings

| Data Structure | Module | Primary Operational Use Case | Asymptotic Time Complexity |
| :--- | :--- | :--- | :--- |
| **Custom Hash Table** | `dsa/hash_table.py` | High-speed student ID lookup cache with separate chaining collision resolution & dynamic rehashing | **O(1)** avg lookup, **O(N)** worst |
| **Binary Search Tree (BST)** | `dsa/bst.py` | Indexes student performance scores, enabling sorted In-Order retrieval and range queries `[min_score, max_score]` | **O(log N)** search/insert, **O(K + log N)** range |
| **Stack (LIFO)** | `dsa/stack.py` | Preserves operation snapshots (CREATE, UPDATE, DELETE) powering the **Undo Last Action** feature | **O(1)** Push / Pop / Peek |
| **Queue (FIFO)** | `dsa/queue.py` | Buffers incoming prediction requests for deterministic First-In, First-Out batch processing | **O(1)** Enqueue / Dequeue |
| **Singly Linked List** | `dsa/linked_list.py` | Dynamic sequential student node chaining with pointer traversal | **O(1)** Head insert, **O(N)** search/delete |
| **Array Operations** | `dsa/array_operations.py` | Algorithmic QuickSort (divide-and-conquer), multi-field filtering, and Binary Search over contiguous memory | **O(N log N)** sort, **O(log N)** binary search |

---

## 4. Machine Learning Pipeline

- **Algorithm:** Scikit-Learn `DecisionTreeClassifier` (`criterion='gini'`, `max_depth=6`, `min_samples_split=8`)
- **Input Features (6):**
  1. `attendance` (0.0 – 100.0%)
  2. `internal_marks` (0.0 – 100.0)
  3. `assignment_marks` (0.0 – 100.0)
  4. `previous_percentage` (0.0 – 100.0%)
  5. `study_hours` (0.0 – 24.0 hrs/day)
  6. `failed_subjects` (Integer backlogs &ge; 0)
- **Target Output:** `Low Risk`, `Medium Risk`, `High Risk`
- **Evaluation:** Stratified 80/20 train/test split (Accuracy: **~92.5%**, Macro F1: **~0.918**), Confusion Matrix, and Feature Importances.
- **Pedagogical Disclaimer:** The synthetic dataset heuristic demonstrates ML engineering workflows. It does not constitute an empirical clinical guarantee of institutional student performance.

---

## 5. Project Directory Structure

```text
AI-Student-Risk-System/
├── app.py                      # Flask main application & route controller
├── config.py                   # Centralized application configuration
├── requirements.txt            # Python dependencies
├── run_project.bat             # One-click Windows setup & launch batch file
├── README.md                   # Project documentation & execution guide
├── .gitignore                  # Git ignore rules
├── .env.example                # Environment variables template
├── database/
│   ├── __init__.py
│   └── db.py                   # SQLite connection, schema, and parameterized helpers
├── dsa/
│   ├── __init__.py
│   ├── array_operations.py     # QuickSort, binary search, filtering
│   ├── linked_list.py          # Singly Linked List dynamic sequence
│   ├── stack.py                # LIFO stack for undo & mutation history
│   ├── queue.py                # FIFO queue for prediction buffering
│   ├── hash_table.py           # Custom Hash Table with separate chaining
│   └── bst.py                  # Binary Search Tree for score indexing
├── ml/
│   ├── __init__.py
│   ├── generate_dataset.py     # Synthetic dataset generator (>= 1,000 records)
│   ├── train_model.py          # DecisionTreeClassifier training & evaluation
│   ├── predict.py              # Model loader & inference service
│   ├── dataset/
│   │   └── students.csv        # 1,200 synthetic student records
│   └── models/
│       ├── risk_model.pkl      # Serialized trained Scikit-Learn model
│       └── model_metadata.json # Evaluation metrics, confusion matrix, params
├── services/
│   ├── __init__.py
│   ├── student_service.py      # Student CRUD, validation, stats & DSA sync
│   ├── prediction_service.py   # Prediction workflows, FIFO queue dispatch
│   └── recommendation_service.py # Non-judgmental educational guidance
├── templates/
│   ├── base.html               # Master layout with navbar & flash alerts
│   ├── dashboard.html          # Main analytics dashboard & Chart.js
│   ├── students.html           # Student table, search, filter, and Undo
│   ├── student_form.html       # Student add / edit form with live previews
│   ├── student_detail.html     # Student profile & instant AI prediction
│   ├── predict.html            # Standalone risk prediction interface
│   ├── prediction_history.html # Audit log of past predictions
│   ├── dsa_demo.html           # Interactive 6-DSA demonstration console
│   ├── model_evaluation.html   # Confusion matrix, metrics, retrain button
│   ├── about.html              # System architecture & B.Tech report summary
│   ├── 404.html                # Not Found error page
│   └── 500.html                # Server error page
├── static/
│   ├── css/
│   │   └── style.css           # Modern custom CSS styling
│   └── js/
│       └── app.js              # Real-time score previews & confirmation dialogues
├── tests/
│   ├── __init__.py
│   ├── test_database.py        # Database schema & constraint tests
│   ├── test_students.py        # Student CRUD & Undo restoration tests
│   ├── test_predictions.py     # ML inference & probability tests
│   ├── test_dsa.py             # Unit tests for all 6 DSA structures
│   ├── test_validation.py      # Input validation & boundary tests
│   └── test_routes.py          # Flask HTTP routes & API endpoint tests
├── docs/
│   ├── project_report.md       # Comprehensive B.Tech mini-project report
│   ├── architecture.md         # System architecture & sequence diagrams
│   ├── test_cases.md           # Formal test cases matrix & results
│   └── viva_questions.md       # 25+ Viva Voce questions and answers
└── presentation/
    └── presentation_outline.md # Slide-by-slide project presentation guide
```

---

## 6. Installation & Execution on Windows

### Option A: One-Click Windows Batch File (Recommended)
Double-click `run_project.bat` or execute in Windows Command Prompt / PowerShell:
```cmd
run_project.bat
```
This script will safely verify Python, install dependencies, generate the dataset if missing, train the model, initialize the database, and launch the web server.

### Option B: Manual Step-by-Step Setup

1. **Clone / Navigate to Project Directory:**
   ```cmd
   cd c:\Users\Prajwal\Downloads\AI-Student-Risk-System
   ```

2. **Create and Activate a Virtual Environment:**
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```cmd
   python -m pip install -r requirements.txt
   ```

4. **Generate the Synthetic Academic Dataset (1,200 records):**
   ```cmd
   python ml\generate_dataset.py
   ```

5. **Train the Decision Tree Model:**
   ```cmd
   python ml\train_model.py
   ```

6. **Start the Flask Application:**
   ```cmd
   python app.py
   ```

7. **Open Application in Browser:**
   Navigate to: **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 7. Running Automated Tests

Run the complete test suite using `pytest`:
```cmd
python -m pytest tests/ -v
```

Expected output:
```text
tests/test_database.py::test_database_initialization PASSED
tests/test_database.py::test_student_insertion_and_query PASSED
tests/test_database.py::test_database_check_constraints PASSED
tests/test_dsa.py::test_array_quicksort_and_search PASSED
tests/test_dsa.py::test_linked_list_operations PASSED
tests/test_dsa.py::test_stack_lifo_order PASSED
tests/test_dsa.py::test_queue_fifo_order PASSED
tests/test_dsa.py::test_custom_hash_table PASSED
tests/test_dsa.py::test_binary_search_tree PASSED
tests/test_predictions.py::test_model_inference_and_categories PASSED
tests/test_predictions.py::test_high_risk_inference PASSED
tests/test_predictions.py::test_academic_recommendations PASSED
tests/test_predictions.py::test_missing_model_handling PASSED
tests/test_routes.py::test_dashboard_route PASSED
tests/test_routes.py::test_students_list_route PASSED
tests/test_routes.py::test_predict_page_route PASSED
tests/test_routes.py::test_dsa_demo_route PASSED
tests/test_routes.py::test_model_evaluation_route PASSED
tests/test_routes.py::test_about_route PASSED
tests/test_routes.py::test_api_predict_endpoint PASSED
tests/test_routes.py::test_404_not_found_route PASSED
tests/test_students.py::test_student_crud_lifecycle PASSED
tests/test_students.py::test_undo_student_deletion PASSED
tests/test_validation.py::test_valid_student_payload PASSED
tests/test_validation.py::test_empty_or_short_name PASSED
tests/test_validation.py::test_attendance_bounds PASSED
tests/test_validation.py::test_study_hours_bounds PASSED
tests/test_validation.py::test_negative_failed_subjects PASSED

============================= 28 passed in 5.29s =============================
```

---

## 8. College Submission Material

Comprehensive submission documents have been generated in the `docs/` and `presentation/` folders:
- **[Project Report](docs/project_report.md)**: Full academic report structured per university guidelines.
- **[System Architecture](docs/architecture.md)**: Deep dive into design patterns and data flows.
- **[Test Cases Matrix](docs/test_cases.md)**: Test plan with boundary conditions and actual observed results.
- **[Viva Voce Questions & Answers](docs/viva_questions.md)**: Comprehensive viva guide for the final demonstration.
- **[Presentation Outline](presentation/presentation_outline.md)**: Presentation slides for project evaluation.
