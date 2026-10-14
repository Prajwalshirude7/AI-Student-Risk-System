# College Viva Voce Questions & Answers Guide

## AI-Based Student Performance & Risk Prediction System
**B.Tech Second-Year Mini-Project Viva Voce Preparation**

---

### Q1. What is the core problem solved by your project?
**Answer:**  
Traditional educational monitoring is retrospective; mentors discover that a student is struggling only after mid-term or semester examination results are released. Our project implements early intervention by taking six continuous academic indicators (attendance, internal tests, assignments, prior marks, study hours, and active backlogs) and classifying the student into `Low Risk`, `Medium Risk`, or `High Risk` with calibrated probabilities and constructive recommendations.

---

### Q2. Which mandatory data structures did you implement, and where are they used?
**Answer:**  
1. **Custom Hash Table (`dsa/hash_table.py`):** Provides $O(1)$ average in-memory lookup of student profiles by their unique `student_id`.
2. **Binary Search Tree (`dsa/bst.py`):** Indexes students by academic score, enabling sorted In-Order traversal and $O(K + \log N)$ range search queries (`[min_score, max_score]`).
3. **Stack (`dsa/stack.py`):** Implements Last-In, First-Out (LIFO) tracking of mutations (`CREATE`, `UPDATE`, `DELETE`) powering the functional "Undo" feature.
4. **Queue (`dsa/queue.py`):** Implements First-In, First-Out (FIFO) buffer for batch prediction requests.
5. **Singly Linked List (`dsa/linked_list.py`):** Provides dynamic memory allocation with sequential pointer traversal for student chains.
6. **Array Operations (`dsa/array_operations.py`):** Implements algorithmic QuickSort ($O(N \log N)$) and Binary Search ($O(\log N)$) over contiguous student record memory.

---

### Q3. Why did you implement BOTH a Hash Table and a Binary Search Tree?
**Answer:**  
They serve two fundamentally distinct algorithmic access patterns:
- **Hash Table:** Optimized for **point queries** by exact key (e.g., "Find student `STU-1005`"). Average time complexity is $O(1)$, but keys are unordered.
- **Binary Search Tree:** Optimized for **range and ordered queries** (e.g., "List all students with internal marks between 40 and 60 in ascending order"). While search is $O(\log N)$, BST maintains natural sorted ordering which a Hash Table cannot do without additional sorting overhead.

---

### Q4. How does your Custom Hash Table handle collisions?
**Answer:**  
We implemented **Separate Chaining**. Each slot in the hash table bucket array holds a pointer to the head of a linked list of `HashNode` objects. When two different keys hash to the same bucket index, the new node is appended to the chain at that bucket. If the load factor ($\alpha = \frac{\text{Count}}{\text{Capacity}}$) exceeds $0.75$, the table automatically resizes by doubling its capacity and rehashing all existing entries to maintain $O(1)$ average performance.

---

### Q5. What is the time and space complexity of your QuickSort implementation?
**Answer:**  
- **Best / Average Time Complexity:** $O(N \log N)$ where the pivot divides the partition into roughly equal sub-arrays.
- **Worst-case Time Complexity:** $O(N^2)$ if the pivot is consistently the smallest or largest element.
- **Auxiliary Space Complexity:** $O(\log N)$ on the recursive call stack.

---

### Q6. How does your "Undo" feature work internally?
**Answer:**  
The undo feature uses a **LIFO Stack** (`OperationStack`). Every time an administrative mutation occurs:
- If a student is deleted, a snapshot of the deleted student is pushed to the stack.
- If updated, the previous state before edit is pushed to the stack.
When the user clicks "Undo Last Action", the topmost operation is popped from the stack, and an inverse parameterized SQL query executes to restore the student into SQLite. Then, in-memory DSA caches are automatically re-synchronized.

---

### Q7. Why did you choose a Decision Tree Classifier instead of other algorithms?
**Answer:**  
1. **Interpretability:** In educational risk management, stakeholders (teachers, students, parents) need to understand *why* a student is flagged. Decision trees produce transparent decision rules.
2. **Handling Non-linear Interactions:** A student with low study hours and backlogs is at high risk even if attendance is average; decision trees model these hierarchical splits naturally.
3. **No Distance Scaling Required:** Decision trees are invariant to monotonic feature scaling, eliminating sensitivity to differing numeric scales (e.g., 0–24 hours vs 0–100 marks).
4. **Fast Inference:** Once trained, decision tree evaluation is $O(\text{Tree Depth})$, making predictions instantaneous (< 5 milliseconds).

---

### Q8. What is Gini Impurity, and how is it calculated?
**Answer:**  
Gini Impurity measures the probability of incorrectly classifying a randomly chosen element if it were randomly labeled according to the class distribution in the node:
$$\text{Gini}(t) = 1 - \sum_{i=1}^{C} p_i^2$$
Where $C$ is the number of target classes and $p_i$ is the probability of class $i$. A pure node containing records of only one risk category has a Gini impurity of $0.0$.

---

### Q9. How did you prevent overfitting in your Decision Tree?
**Answer:**  
We constrained the tree hyperparameters:
- `max_depth = 6`: Prevents the tree from growing leaves tailored to individual synthetic training samples.
- `min_samples_split = 8`: Demands at least 8 samples at an internal node before attempting a split.
- `min_samples_leaf = 4`: Ensures terminal leaves have at least 4 student samples.

---

### Q10. What is a Stratified Train/Test Split, and why did you use it?
**Answer:**  
A stratified split divides the dataset into 80% training and 20% test partitions while strictly maintaining the original proportion of target classes (`Low Risk`, `Medium Risk`, `High Risk`) across both subsets. This prevents sampling bias where rare classes might be underrepresented in the test partition.

---

### Q11. Explain Precision, Recall, and F1-Score in your system.
**Answer:**  
- **Precision:** $\frac{TP}{TP + FP}$ — Of all students predicted as High Risk, how many were actually High Risk?
- **Recall:** $\frac{TP}{TP + FN}$ — Of all actual High-Risk students, how many did the model successfully identify? (Critical in academic risk to avoid missing vulnerable students).
- **F1-Score:** The harmonic mean of precision and recall:
  $$F_1 = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$

---

### Q12. How do you prevent SQL Injection attacks?
**Answer:**  
All database interactions use **parameterized SQL queries** with placeholder markers (`?` in SQLite). Values are never concatenated into the raw SQL string. This ensures the database engine treats all input strictly as literal values rather than executable SQL commands.

---

### Q13. How does the application persist data across restarts?
**Answer:**  
We use an **SQLite3** relational database (`database/students.db`). SQLite stores relational tables on disk in a single file. Our initialization routine uses `CREATE TABLE IF NOT EXISTS`, ensuring that existing student records and prediction logs remain intact whenever the application restarts.

---

### Q14. What are the ethical implications of predicting student failure?
**Answer:**  
Predictive models can inadvertently create self-fulfilling prophecies or discourage learners if presented fatalistically. Our application incorporates three ethical safeguards:
1. Model probabilities are presented as statistical patterns over training heuristics, never as guaranteed failure.
2. Recommendations are non-judgmental and actionable (e.g. peer study, faculty doubt clearing).
3. Clear disclaimers explicitly communicate that the synthetic dataset demonstrates computer science engineering workflows rather than institutional evaluation validity.

---

### Q15. How many automated tests does your project have, and what do they verify?
**Answer:**  
The project includes **28 automated tests** executed via `pytest`, covering:
- Database table initialization, relational writes/reads, and SQLite CHECK constraints.
- Custom DSA operations, sorting, traversals, and edge cases for all 6 data structures.
- Student CRUD lifecycle and Stack-driven Undo recovery.
- Boundary condition validation (e.g. rejecting attendance > 100% or study hours > 24).
- ML prediction inference, probability calibration, and missing model fallback.
- Web routing, template rendering, and REST API endpoints.
