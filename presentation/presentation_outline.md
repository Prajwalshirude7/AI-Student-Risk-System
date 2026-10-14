# Project Presentation Outline & Slide Deck Script

## AI-Based Student Performance & Risk Prediction System
**B.Tech Second-Year Mini-Project Demonstration (10-12 Minutes)**

---

### Slide 1: Title & Introduction (Time: 1 min)
- **Title:** AI-Based Student Performance & Risk Prediction System
- **Subtitle:** An Integrated Educational Decision Support System
- **Authors:** Student Name(s), Department of Computer Science & Engineering
- **Mentor:** Faculty Advisor / Project Guide
- **Key Talking Points:**
  - Introduce the objective: Transforming retrospective grading into proactive academic mentorship.
  - Highlight integration of four foundational CS subjects: DSA, Machine Learning, Database Management, and Web Technologies.

---

### Slide 2: Problem Statement & Existing Limitations (Time: 1 min)
- **Problem:** Conventional academic reviews detect student failure only after semester exams conclude.
- **Existing Drawbacks:**
  - Spreadsheets and siloed attendance registers lack cross-indicator intelligence.
  - Manual thresholds (e.g. attendance < 75%) overlook multi-dimensional distress.
  - Lack of algorithmic transparency and expensive commercial cloud tools.

---

### Slide 3: Proposed System Architecture (Time: 1.5 min)
- **Architecture Overview:** 4-Tier Clean Architecture.
  - **Frontend:** Bootstrap 5.3 + Chart.js responsive dashboard.
  - **Backend:** Flask web server with service layer.
  - **Algorithms:** 6 Custom Data Structures.
  - **AI Model:** Decision Tree Classifier ($92.5\%$ test accuracy).
  - **Database:** SQLite3 persistent store with parameterized queries.

---

### Slide 4: Mandatory College Data Structures in Action (Time: 2.5 min)
*Show how every structure genuinely powers live functionality:*
1. **Custom Hash Table:** Separate Chaining with dynamic capacity doubling ($O(1)$ student ID lookup).
2. **Binary Search Tree (BST):** Score indexing with sorted In-Order traversal & $O(K + \log N)$ range search.
3. **Stack (LIFO):** Mutation snapshot history enabling the functional **Undo Last Action** feature.
4. **Queue (FIFO):** Prediction request buffer for arrival-sequence batch processing.
5. **Singly Linked List:** Dynamic sequential node allocation.
6. **Array Operations:** Algorithmic QuickSort ($O(N \log N)$) & Binary Search ($O(\log N)$).

---

### Slide 5: Machine Learning Pipeline & Dataset (Time: 1.5 min)
- **Dataset:** 1,200 synthetic student records with documented labelling heuristic.
- **Features (6):** Attendance, Internals, Assignments, Prior %, Study Hours, Active Backlogs.
- **Algorithm:** Scikit-Learn `DecisionTreeClassifier` (`max_depth=6`, `min_samples_split=8`).
- **Evaluation:** Stratified 80/20 train/test split.
  - Accuracy: **$92.50\%$**
  - Macro F1: **$0.9181$**

---

### Slide 6: Model Evaluation & Confusion Matrix (Time: 1 min)
- Present Confusion Matrix breakdown across Low, Medium, and High Risk.
- Feature Importances ranking: Shows that backlogs, internal assessment marks, and attendance are the strongest split predictors.
- Transparent disclaimer: Ethical compliance and pedagogical heuristic disclosure.

---

### Slide 7: Live Demonstration Walkthrough (Time: 2.5 min)
*Switch to browser at http://127.0.0.1:5000:*
1. **Dashboard:** Show live metrics, Doughnut Risk Chart, and Bar Chart averages.
2. **Student CRUD & Undo:** Add a student, delete a student, and click "Undo Last Action" to show the LIFO Stack in action.
3. **Risk Predictor:** Enter student data on `/predict`, show multiclass probabilities and non-judgmental recommendations.
4. **DSA Verification Console:** Run a live $O(1)$ Hash Table lookup and a BST score range query `[40, 70]`.

---

### Slide 8: Software Engineering & Automated Testing (Time: 1 min)
- **Test Suite:** 28 automated tests written in `pytest`.
- **Coverage:** Relational schema, check constraints, all 6 DSA structures, CRUD lifecycle, ML inference, and HTTP routes.
- **Result:** $100\%$ pass rate in $5.29$ seconds.

---

### Slide 9: Ethical Safeguards & Educational Value (Time: 0.5 min)
- Non-judgmental guidance: Constructive academic habits instead of fatalistic labels.
- Local execution: Zero third-party telemetry, preserving student data confidentiality.
- Accessible codebase: Zero-cost, local zero-API dependencies.

---

### Slide 10: Conclusion & Q&A (Time: 1 min)
- Summarize deliverables: Fully functional local web portal, reproducible ML model, tested custom data structures, and complete documentation.
- Thank the evaluation panel and open for Viva Voce questions.
