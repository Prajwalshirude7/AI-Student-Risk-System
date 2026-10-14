# Test Cases Specification & Verification Matrix

## AI-Based Student Performance & Risk Prediction System

**Automated Test Framework:** `pytest 9.1+`  
**Execution Environment:** Windows 10/11, Python 3.13.7  
**Test Suite Summary:** **28 passed in 5.29 seconds** (100% Pass Rate)

---

## 1. Database & Persistence Test Cases (`tests/test_database.py`)

| Test ID | Test Case Name | Objective | Input / Condition | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-DB-01** | `test_database_initialization` | Verify table schema creation | Fresh isolated temporary DB | `students`, `predictions`, `operations_log` tables exist | All 3 tables created | **PASS** |
| **TC-DB-02** | `test_student_insertion_and_query` | Verify parameterized write and read | Insert `STU-9999` with attributes | Data retrieved matches inputs with correct types | Stored & queried successfully | **PASS** |
| **TC-DB-03** | `test_database_check_constraints` | Verify CHECK constraints on invalid bounds | Insert attendance = 150.0% | SQLite raises `sqlite3.IntegrityError` | `IntegrityError` raised | **PASS** |

---

## 2. Data Structures & Algorithms Test Cases (`tests/test_dsa.py`)

| Test ID | Test Case Name | Objective | Input / Condition | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-DSA-01** | `test_array_quicksort_and_search` | Verify QuickSort and Binary Search | 3 unsorted student records | Ascending & descending sorted orders; Binary search finds exact record | QuickSort & Binary Search verified | **PASS** |
| **TC-DSA-02** | `test_linked_list_operations` | Verify node chaining, head/tail insert, search, delete | Linked list inserts at head & tail | Node order maintained; search returns data; delete removes node | Length updated, node deleted | **PASS** |
| **TC-DSA-03** | `test_stack_lifo_order` | Verify LIFO mutation stack | Push items 1, 2, 3 | Pop returns 3, 2, 1; peek returns 3 without removal | Strict LIFO verified | **PASS** |
| **TC-DSA-04** | `test_queue_fifo_order` | Verify FIFO prediction queue | Enqueue tasks A, B, C | Dequeue returns A, B, C in exact arrival sequence | Strict FIFO verified | **PASS** |
| **TC-DSA-05** | `test_custom_hash_table` | Verify custom polynomial hash, separate chaining, resize | Insert 4 items into initial capacity 4 | Collision resolved via bucket chaining; $O(1)$ search returns correct value | Search & resize verified | **PASS** |
| **TC-DSA-06** | `test_binary_search_tree` | Verify score indexing, sorted traversal, range search | Scores: 50.0, 60.0, 75.0, 90.0 | In-order yields sorted sequence; range search `[55, 80]` returns 60 & 75 | In-order & range queries passed | **PASS** |

---

## 3. Student Service & CRUD Test Cases (`tests/test_students.py`)

| Test ID | Test Case Name | Objective | Input / Condition | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-STU-01** | `test_student_crud_lifecycle` | Verify create, read, update, delete | Full valid student payload | Created -> Fetched -> Updated -> Deleted verified | Complete lifecycle passed | **PASS** |
| **TC-STU-02** | `test_undo_student_deletion` | Verify LIFO Stack undo restores deleted student | Delete student `STU-8002`, trigger undo | Student record safely restored in SQLite DB | Record restored into DB | **PASS** |

---

## 4. Input Validation & Boundary Test Cases (`tests/test_validation.py`)

| Test ID | Test Case Name | Objective | Input / Condition | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-VAL-01** | `test_valid_student_payload` | Verify clean acceptance of valid inputs | Normal student features | `is_valid = True`, error = None | Validated successfully | **PASS** |
| **TC-VAL-02** | `test_empty_or_short_name` | Reject empty or whitespace-only names | `name = " "` | `is_valid = False`, mentions name error | Validation error returned | **PASS** |
| **TC-VAL-03** | `test_attendance_bounds` | Reject negative or >100% attendance | `attendance = -5.0` and `105.0` | Both rejected with specific attendance error | Boundaries enforced | **PASS** |
| **TC-VAL-04** | `test_study_hours_bounds` | Reject >24 daily study hours | `study_hours = 26.0` | Rejected with study hours error | Boundary enforced | **PASS** |
| **TC-VAL-05** | `test_negative_failed_subjects` | Reject negative backlog counts | `failed_subjects = -2` | Rejected with backlogs error | Boundary enforced | **PASS** |

---

## 5. Machine Learning Inference Test Cases (`tests/test_predictions.py`)

| Test ID | Test Case Name | Objective | Input / Condition | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-ML-01** | `test_model_inference_and_categories` | Verify valid class and probabilities | Balanced academic indicators | Category in `{Low, Med, High}`; probabilities sum to ~1.0 | Valid category & probabilities | **PASS** |
| **TC-ML-02** | `test_high_risk_inference` | Verify struggling indicators trigger vulnerability | Low att (42%), 3 backlogs | High or Medium Risk flagged with contributing factors | High/Med risk & factors flagged | **PASS** |
| **TC-ML-03** | `test_academic_recommendations` | Verify constructive advice generation | Low attendance, backlogs | Generates constructive advice without negative labels | Constructive guidance produced | **PASS** |
| **TC-ML-04** | `test_missing_model_handling` | Verify graceful error when model missing | Non-existent model path | Raises clean `RuntimeError` | Clean exception raised | **PASS** |

---

## 6. Flask Web Routes Test Cases (`tests/test_routes.py`)

| Test ID | Test Case Name | Objective | Route / Method | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-RT-01** | `test_dashboard_route` | Render analytics dashboard | `GET /` | HTTP 200, dashboard template rendered | HTTP 200 OK | **PASS** |
| **TC-RT-02** | `test_students_list_route` | Render student directory | `GET /students` | HTTP 200, student table rendered | HTTP 200 OK | **PASS** |
| **TC-RT-03** | `test_predict_page_route` | Render predict form & execute POST | `GET & POST /predict` | HTTP 200, results displayed | HTTP 200 OK | **PASS** |
| **TC-RT-04** | `test_dsa_demo_route` | Render interactive DSA console | `GET /dsa-demo` | HTTP 200, DSA console rendered | HTTP 200 OK | **PASS** |
| **TC-RT-05** | `test_model_evaluation_route`| Render ML metrics & confusion matrix | `GET /model-evaluation` | HTTP 200, metrics displayed | HTTP 200 OK | **PASS** |
| **TC-RT-06** | `test_about_route` | Render documentation page | `GET /about` | HTTP 200, architecture displayed | HTTP 200 OK | **PASS** |
| **TC-RT-07** | `test_api_predict_endpoint` | Programmatic JSON inference | `POST /api/predict` | HTTP 200 with JSON payload | HTTP 200 JSON OK | **PASS** |
| **TC-RT-08** | `test_404_not_found_route` | Custom 404 handler verification | `GET /non-existent-xyz` | HTTP 404 with custom error page | HTTP 404 Custom OK | **PASS** |
