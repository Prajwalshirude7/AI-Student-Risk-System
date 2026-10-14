# Comprehensive Project Guide & Presentation Manual
## AI-Based Student Performance & Risk Prediction System

> **Target Audience:** Anyone from a beginner to an examiner. This manual explains the complete architecture, data structures, machine learning pipeline, running instructions, and database inspection procedures.

---

## 1. System Overview & Technology Stack

This project is an **Early Warning & Decision Support System** that analyzes academic indicators to identify students at risk of failing or dropping out before semester examinations occur.

### Complete Technology Stack Summary

| Layer | Technologies Used | Purpose |
| :--- | :--- | :--- |
| **Frontend** | HTML5, CSS3, JavaScript, Bootstrap 5.3, Chart.js, Bootstrap Icons | Responsive UI, interactive academic analytics dashboards, radar charts, and diagnostics console. |
| **Backend** | Python 3.10+, Flask Web Framework, Jinja2 Templates | HTTP routing, REST API endpoints, business logic validation, service layer coordination. |
| **Machine Learning** | Scikit-Learn, Pandas, NumPy, Joblib | Decision Tree Risk Classifier ($92.5\%$ accuracy) predicting Low, Medium, and High Risk. |
| **Database** | SQLite3 (`database/students.db`), Parameterized SQL | Persistent relational storage for student profiles, audit history, and prediction logs. |
| **Data Structures** | Custom implementations in `dsa/` (Hash Table, BST, Stack, Queue, Linked List, QuickSort) | High-speed in-memory L1 cache, indexed range queries, transaction rollback (undo), and request buffering. |
| **Testing** | Pytest, Pytest-Cov | 28 automated test cases covering database integrity, routes, ML inference, and DSA operations. |

---

## 2. In-Depth DSA Breakdown (Where, Why & How)

Unlike toy academic scripts, every data structure in this project serves an operational purpose in the system.

```
                           ┌─────────────────────────┐
                           │   Flask Web / Service   │
                           └────────────┬────────────┘
                                        │
           ┌────────────────────────────┼────────────────────────────┐
           ▼                            ▼                            ▼
  ┌─────────────────┐          ┌─────────────────┐          ┌─────────────────┐
  │ 1. Hash Table   │          │ 2. BST          │          │ 3. Stack        │
  │ L1 Fast Lookup  │          │ Range Queries   │          │ Undo Mutation   │
  │ dsa/hash_table  │          │ dsa/bst.py      │          │ dsa/stack.py    │
  └─────────────────┘          └─────────────────┘          └─────────────────┘
           │                            │                            │
           ▼                            ▼                            ▼
  ┌─────────────────┐          ┌─────────────────┐          ┌─────────────────┐
  │ 4. Queue        │          │ 5. Linked List  │          │ 6. QuickSort    │
  │ FIFO Batch ML   │          │ Sequential List │          │ Array Sorting   │
  │ dsa/queue.py    │          │ dsa/linked_list │          │ dsa/array_ops   │
  └─────────────────┘          └─────────────────┘          └─────────────────┘
```

---

### Structure 1: Custom Hash Table (L1 In-Memory Cache)
* **File:** `dsa/hash_table.py`
* **Used in:** `app.py:view_student()` (Line 102) & `services/student_service.py`
* **Why we use it:**
  * When a teacher clicks on a student profile (`/students/<student_id>`), querying the SQLite database on disk involves filesystem I/O which is slow.
  * We use an in-memory Hash Table as an **L1 Cache**. If the student is in RAM, we return it in **$0.05\text{ ms}$** without touching the disk.
* **How it works:**
  1. **Polynomial Rolling Hash:** It computes an integer bucket index from the string key (e.g. `"STU-1001"`):
     $$\text{hash} = \left(\sum s[i] \times 31^{k-1-i}\right) \pmod{\text{capacity}}$$
  2. **Separate Chaining:** If two student IDs land in the same bucket index (collision), they are chained together in a linked list of `HashNode`s.
  3. **Dynamic Rehashing:** When the load factor ($\frac{\text{count}}{\text{capacity}}$) exceeds $0.75$, the table automatically doubles its capacity and redistributes all keys.
* **Complexities:**
  * Average Lookup/Insert: **$O(1)$**
  * Worst Case (all keys collide): **$O(N)$**

---

### Structure 2: Binary Search Tree (BST) (Ordered Score Index)
* **File:** `dsa/bst.py`
* **Used in:** `services/student_service.py:search_and_filter_students()` & `app.py:list_students()`
* **Why we use it:**
  * Teachers frequently need to find students whose internal marks fall within a specific danger zone (e.g., marks between $0$ and $40$).
  * A standard database table scan requires checking every row ($O(N)$). The BST maintains an in-memory sorted tree keyed by student marks, enabling fast sub-tree range pruning.
* **How it works:**
  1. Each `BSTNode` has a key (`internal_marks`) and a list of students with that exact score.
  2. Lower scores go to the left child; higher scores go to the right child.
  3. `range_search(min_score, max_score)` recursively traverses only the branches that fall within the range, pruning irrelevant subtrees.
  4. In-order traversal gives all students sorted by score in $O(N)$ without needing extra sorting algorithms.
* **Complexities:**
  * Search / Insert: **$O(\log N)$** average
  * Range Search: **$O(K + \log N)$** (where $K$ is number of matches)

---

### Structure 3: Stack (LIFO - Last In, First Out) (Undo Engine)
* **File:** `dsa/stack.py`
* **Used in:** `services/student_service.py:undo_last_operation()` & `app.py:undo_action()`
* **Why we use it:**
  * If a user accidentally deletes, creates, or updates a student record, they can click **"Undo Last Action"** to revert it immediately.
* **How it works:**
  1. Whenever a mutation occurs (CREATE, UPDATE, DELETE), a deep snapshot of the previous state is pushed onto the top of the stack (`push()`).
  2. Clicking "Undo" triggers `pop()`, retrieving the topmost (most recent) snapshot.
  3. The service reverses the action in SQLite:
     * If last action was `DELETE` $\rightarrow$ re-inserts the student.
     * If last action was `CREATE` $\rightarrow$ deletes the student.
     * If last action was `UPDATE` $\rightarrow$ restores the old values.
  4. Max capacity is capped at 50 to prevent memory exhaustion.
* **Complexities:**
  * Push / Pop / Peek: **$O(1)$**
  * Space: **$O(M)$** (bounded by max history size)

---

### Structure 4: Queue (FIFO - First In, First Out) (Batch Prediction Buffer)
* **File:** `dsa/queue.py`
* **Used in:** `services/prediction_service.py:enqueue_prediction()` & `process_queue_synchronously()`
* **Why we use it:**
  * In production systems, running machine learning inference on hundreds of incoming student submissions simultaneously can spike CPU and freeze the server.
  * The Queue acts as a buffer: requests are placed in line and processed in strict arrival sequence (First-In, First-Out).
* **How it works:**
  1. When bulk predictions arrive, each student payload is `enqueue()`ed at the tail.
  2. A worker loop calls `dequeue()`, feeds the record into the Scikit-Learn model, attaches academic recommendations, and persists the result.
* **Complexities:**
  * Enqueue / Dequeue / Peek: **$O(1)$**

---

### Structure 5: Singly Linked List (Sequential Node Chaining)
* **File:** `dsa/linked_list.py`
* **Used in:** `services/student_service.py:sync_dsa_structures()` & System Diagnostics
* **Why we use it:**
  * Demonstrates dynamic memory allocation where records do not need to be stored in contiguous memory blocks.
  * Adding a new student to the beginning of a linked list is $O(1)$, unlike a contiguous array which requires shifting all elements.
* **How it works:**
  1. Each `StudentNode` stores student data and a reference (`next`) to the next node in memory.
  2. Traversal walks node by node until `next is None`.
* **Complexities:**
  * Head Insert: **$O(1)$**
  * Search / Delete: **$O(N)$**

---

### Structure 6: Array Operations & QuickSort (In-Place Sorting)
* **File:** `dsa/array_operations.py`
* **Used in:** `services/student_service.py:search_and_filter_students()` (Line 360)
* **Why we use it:**
  * On the Student Directory table, users can sort by Attendance, Internals, Name, or Backlogs.
  * Instead of issuing a database `ORDER BY` query on every click, sorting is executed directly on the in-memory array using the divide-and-conquer **QuickSort** algorithm.
* **How it works:**
  1. Picks a pivot element from the array.
  2. Partitions the array into two sub-arrays: elements smaller than the pivot and elements greater.
  3. Recursively sorts the partitions in-place.
  4. Also implements **Binary Search** ($O(\log N)$) over arrays sorted by student ID.
* **Complexities:**
  * QuickSort: **$O(N \log N)$** average
  * Binary Search: **$O(\log N)$**

---

## 3. How to Run the Project (Step-by-Step)

### Prerequisites
* Windows OS with Python 3.10, 3.11, 3.12, or 3.13 installed.

### Option A: The 1-Click Batch Script
Open Command Prompt in the project folder and run:
```cmd
run_project.bat
```
*(This script checks your virtual environment, installs packages, runs tests, and launches the web app).*

### Option B: Manual Command Line Execution
1. **Open PowerShell or CMD** in the project root:
   ```powershell
   cd c:\Users\Prajwal\Downloads\AI-Student-Risk-System
   ```
2. **Install requirements (if not already done):**
   ```powershell
   pip install -r requirements.txt
   ```
3. **Run the Automated Test Suite (to verify everything passes):**
   ```powershell
   pytest
   ```
   *(All 28 tests should pass in ~5 seconds).*
4. **Start the Flask Application:**
   ```powershell
   python app.py
   ```
5. **Open your web browser:**
   Go to: **`http://127.0.0.1:5000`**

---

## 4. How to Access and View the SQLite Database

The database file is stored locally at:
`c:\Users\Prajwal\Downloads\AI-Student-Risk-System\database\students.db`

### Database Tables:
1. **`students`**: Contains all enrolled students with attendance, marks, study hours, backlogs, and risk predictions.
2. **`predictions`**: Audit trail of every single AI prediction run, confidence scores, and recommendations.
3. **`operations_log`**: Log of mutation operations used for stack undo auditing.

---

### Method 1: DB Browser for SQLite (Recommended for Presentations)
1. Download the free tool **DB Browser for SQLite** (from [sqlitebrowser.org](https://sqlitebrowser.org/)).
2. Open the application and click **"Open Database"**.
3. Navigate to: `c:\Users\Prajwal\Downloads\AI-Student-Risk-System\database\students.db`.
4. Click on the **"Browse Data"** tab:
   * Select `students` table to see student records in an Excel-like view.
   * Select `predictions` table to inspect AI output probabilities.

---

### Method 2: Inspect Database via Python Command Line (No Software Needed)
Run this single command in PowerShell or CMD to print out the top records directly in your terminal:

```powershell
python -c "import sqlite3; conn = sqlite3.connect('database/students.db'); c = conn.cursor(); [print(dict(zip([col[0] for col in c.description], row))) for row in c.execute('SELECT student_id, name, attendance, internal_marks, predicted_risk FROM students LIMIT 5').fetchall()]"
```

To see the total student count:
```powershell
python -c "import sqlite3; conn = sqlite3.connect('database/students.db'); print('Total Students:', conn.execute('SELECT COUNT(*) FROM students').fetchone()[0])"
```

---

### Method 3: Using the SQLite Command Line Tool (`sqlite3`)
If you have `sqlite3` installed on your machine:
```powershell
sqlite3 database/students.db
```
Inside the prompt:
```sql
.tables
SELECT student_id, name, attendance, internal_marks, predicted_risk FROM students LIMIT 10;
.quit
```

---

## 5. How to Ace Your Presentation & Viva (Cheatsheet)

When presenting, examiners will typically ask 4 key questions. Here are your exact answers:

### Q1: "Where have you used Data Structures in your project?"
> *"Instead of using DSA as isolated toy scripts, they form the high-performance in-memory engine of our system:*
> 1. *Our **Custom Hash Table** acts as an L1 cache, retrieving student profiles in $0.05\text{ ms}$ without disk I/O.*
> 2. *Our **Binary Search Tree** indexes student performance scores, enabling $O(K + \log N)$ range queries when teachers filter score bands.*
> 3. *Our **Stack** powers the 'Undo Last Action' feature, storing mutation snapshots in LIFO order.*
> 4. *Our **Queue** buffers prediction requests so the ML model processes batch submissions in FIFO order.*
> 5. *Our **QuickSort** algorithm handles table column sorting in $O(N \log N)$ directly in RAM."*

### Q2: "Why not just use SQL for everything?"
> *"In real-world architectures like Redis, Git, or database query planners, hitting disk I/O for every operation causes bottlenecks. By combining an in-memory caching and indexing layer (DSA) with a relational database (SQLite), we get both sub-millisecond retrieval speeds and permanent storage persistence."*

### Q3: "Which Machine Learning model did you choose and why?"
> *"We trained a **Decision Tree Classifier** (`max_depth=6`, `min_samples_split=8`) using Scikit-Learn. We specifically chose Decision Trees over black-box models (like Neural Networks) because educational risk assessment requires **explainability**. A teacher must see exactly why a student was flagged (e.g., Attendance $< 75\%$ AND Internals $< 40$) so they can recommend the right academic intervention."*

### Q4: "What accuracy did the model achieve?"
> *"On a stratified $80/20$ train/test split of $1,200$ student records, the model achieved **$92.50\%$ test accuracy** and a **Macro F1-score of $0.9181$**, with consistent precision across Low, Medium, and High Risk categories."*
