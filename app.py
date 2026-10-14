"""
AI-Based Student Performance & Risk Prediction System
Main Flask Application Controller
"""

import time
import json
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from config import Config
from database.db import init_db, get_db_connection, execute_query
from services.student_service import (
    StudentService,
    student_hash_table,
    student_bst,
    student_linked_list,
    operation_stack
)
from services.prediction_service import PredictionService, prediction_queue
from services.recommendation_service import AcademicRecommendationService
from ml.predict import predictor
from ml.train_model import train_and_evaluate_model

def _seed_initial_students_if_empty(db_path):
    """Populates a small initial set of students from CSV or defaults if table is empty."""
    try:
        count_row = execute_query("SELECT COUNT(*) as count FROM students;", db_path=db_path, fetchone=True)
        if count_row and count_row["count"] == 0:
            csv_path = Path(Config.DATASET_PATH)
            if csv_path.exists():
                import pandas as pd
                df = pd.read_csv(csv_path).head(25)
                for _, row in df.iterrows():
                    try:
                        StudentService.create_student({
                            "student_id": str(row["student_id"]),
                            "name": str(row["name"]),
                            "attendance": float(row["attendance"]),
                            "internal_marks": float(row["internal_marks"]),
                            "assignment_marks": float(row["assignment_marks"]),
                            "previous_percentage": float(row["previous_percentage"]),
                            "study_hours": float(row["study_hours"]),
                            "failed_subjects": int(row["failed_subjects"]),
                        }, db_path=db_path, predicted_risk=str(row["risk_label"]), risk_probability=0.88)
                    except Exception:
                        pass
    except Exception:
        pass

# ==========================================
# Route Handlers
# ==========================================

def dashboard():
    """Renders the main Academic Dashboard with live statistics and charts."""
    db_path = Config.DATABASE_PATH
    stats = StudentService.get_dashboard_statistics(db_path)
    return render_template("dashboard.html", stats=stats)

def list_students():
    """Lists students with search, multi-field risk filtering, BST score range queries, and QuickSort."""
    search_q = request.args.get("search", "").strip()
    risk_filter = request.args.get("risk", "all").strip()
    score_range = request.args.get("score_range", "all").strip()
    sort_by = request.args.get("sort", "id").strip()
    sort_order = request.args.get("order", "asc" if sort_by in ("name", "id") else "desc").strip()

    db_path = Config.DATABASE_PATH
    students = StudentService.search_and_filter_students(
        search_query=search_q,
        risk_filter=risk_filter,
        sort_by=sort_by,
        sort_order=sort_order,
        score_range=score_range,
        db_path=db_path
    )

    return render_template(
        "students.html",
        students=students,
        search_query=search_q,
        current_risk=risk_filter,
        current_score_range=score_range,
        current_sort=sort_by,
        current_order=sort_order
    )

def create_student_page():
    """Handles new student registration."""
    db_path = Config.DATABASE_PATH
    if request.method == "POST":
        try:
            new_student = StudentService.create_student(request.form.to_dict(), db_path=db_path)
            flash(f"Student {new_student['student_id']} ({new_student['name']}) enrolled successfully!", "success")
            return redirect(url_for("view_student", student_id=new_student["student_id"]))
        except Exception as e:
            flash(f"Validation error: {e}", "danger")
            return render_template("student_form.html", is_edit=False, student=request.form)

    return render_template("student_form.html", is_edit=False, student=None)

def view_student(student_id):
    """Displays student profile with academic breakdown and recommendations."""
    db_path = Config.DATABASE_PATH
    t0 = time.perf_counter()
    student = student_hash_table.search(student_id.strip().upper())
    cache_hit = False
    if student:
        cache_hit = True
    else:
        student = StudentService.get_student_by_id(student_id, db_path=db_path)
    lookup_ms = round((time.perf_counter() - t0) * 1000, 2)
    
    if not student:
        flash(f"Student with ID '{student_id}' does not exist.", "warning")
        return redirect(url_for("list_students"))

    recs = AcademicRecommendationService.generate_recommendations(student, student.get("predicted_risk", "Not Predicted"))
    return render_template(
        "student_detail.html",
        student=student,
        recommendations=recs,
        cache_hit=cache_hit,
        lookup_ms=lookup_ms
    )

def edit_student_page(student_id):
    """Modifies student academic record and pushes previous state to Stack."""
    db_path = Config.DATABASE_PATH
    student = StudentService.get_student_by_id(student_id, db_path=db_path)
    if not student:
        flash(f"Student {student_id} not found.", "danger")
        return redirect(url_for("list_students"))

    if request.method == "POST":
        try:
            updated = StudentService.update_student(student_id, request.form.to_dict(), db_path=db_path)
            flash(f"Student {student_id} updated successfully. Undo snapshot preserved in Stack.", "success")
            return redirect(url_for("view_student", student_id=student_id))
        except Exception as e:
            flash(f"Update failed: {e}", "danger")
            return render_template("student_form.html", is_edit=True, student=request.form)

    return render_template("student_form.html", is_edit=True, student=student)

def delete_student_action(student_id):
    """Deletes student record after preserving snapshot in Stack for undo."""
    db_path = Config.DATABASE_PATH
    success = StudentService.delete_student(student_id, db_path=db_path)
    if success:
        flash(f"Student {student_id} deleted. You can undo this action using the 'Undo Last Action' button.", "info")
    else:
        flash(f"Could not delete student {student_id}.", "warning")
    return redirect(url_for("list_students"))

def predict_student_record(student_id):
    """Executes fresh AI prediction for an existing enrolled student."""
    db_path = Config.DATABASE_PATH
    student = StudentService.get_student_by_id(student_id, db_path=db_path)
    if not student:
        flash(f"Student {student_id} not found.", "danger")
        return redirect(url_for("list_students"))

    try:
        res = PredictionService.predict_and_record(
            student_data=student,
            student_id=student_id,
            student_name=student["name"],
            save_to_db=True,
            db_path=db_path
        )
        StudentService.sync_dsa_structures(db_path)
        flash(f"AI Risk evaluated: {res['predicted_risk']} (Confidence: {(res['confidence_score']*100):.1f}%)", "success")
    except Exception as e:
        flash(f"Prediction failed: {e}", "danger")

    return redirect(url_for("view_student", student_id=student_id))

def undo_action():
    """Pops the last operation from LIFO Stack and restores SQLite database state."""
    db_path = Config.DATABASE_PATH
    res = StudentService.undo_last_operation(db_path=db_path)
    if res["success"]:
        flash(res["message"], "success")
    else:
        flash(res["message"], "warning")
    return redirect(url_for("list_students"))

def predict_page():
    """Interactive prediction interface with confidence and recommendations."""
    prediction_result = None
    form_data = None
    db_path = Config.DATABASE_PATH

    if request.method == "POST":
        form_data = request.form.to_dict()
        try:
            save_db = ("save_to_db" in form_data)
            prediction_result = PredictionService.predict_and_record(
                student_data=form_data,
                student_id="ANONYMOUS",
                student_name=form_data.get("student_name") or "Anonymous Candidate",
                save_to_db=save_db,
                db_path=db_path
            )
            flash(f"Prediction generated: {prediction_result['predicted_risk']}", "success")
        except Exception as e:
            flash(f"Inference error: {e}", "danger")

    return render_template("predict.html", prediction_result=prediction_result, form_data=form_data)

def prediction_history():
    """Displays audit history of all recorded predictions."""
    db_path = Config.DATABASE_PATH
    history = PredictionService.get_prediction_history(limit=50, db_path=db_path)
    return render_template("prediction_history.html", history=history)

def dsa_demo():
    """Interactive educational demonstration console for all 6 data structures."""
    return render_template(
        "dsa_demo.html",
        demo_results={},
        ht_stats={
            "capacity": student_hash_table.capacity,
            "count": student_hash_table.size(),
            "load_factor": student_hash_table.load_factor()
        },
        bst_count=len(student_bst),
        stack_history=operation_stack.get_history()[:10],
        queue_items=prediction_queue.get_all(),
        linked_list_nodes=student_linked_list.to_list()
    )

def dsa_demo_action(structure):
    """Executes specific interactive test operation on chosen data structure."""
    demo_results = {}
    db_path = Config.DATABASE_PATH
    
    if structure == "hash_table":
        target_id = request.form.get("student_id", "").strip().upper()
        t0 = time.perf_counter()
        found_student = student_hash_table.search(target_id)
        t_elapsed = round((time.perf_counter() - t0) * 1000, 3)

        demo_results["hash_table"] = {
            "searched_id": target_id,
            "found": found_student is not None,
            "student": found_student,
            "execution_time_ms": t_elapsed
        }
        flash(f"Hash Table Search for {target_id} completed in {t_elapsed} ms.", "info")

    elif structure == "bst":
        try:
            min_score = float(request.form.get("min_score", 0))
            max_score = float(request.form.get("max_score", 100))
        except ValueError:
            min_score, max_score = 40.0, 70.0

        t0 = time.perf_counter()
        matched_students = student_bst.range_search(min_score, max_score)
        t_elapsed = round((time.perf_counter() - t0) * 1000, 3)

        demo_results["bst"] = {
            "min_score": min_score,
            "max_score": max_score,
            "matching_count": len(matched_students),
            "students": matched_students[:15],
            "execution_time_ms": t_elapsed
        }
        flash(f"BST Range Search executed in {t_elapsed} ms. Matched {len(matched_students)} students.", "info")

    elif structure == "stack":
        op = request.form.get("op", "push")
        if op == "push":
            act = request.form.get("action_name", "DEMO_ACTION")
            operation_stack.push({
                "action": act,
                "student_id": "DEMO-USER",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            })
            flash(f"Pushed '{act}' onto Stack top. Current depth: {operation_stack.size()}", "success")
        elif op == "pop":
            popped = operation_stack.pop()
            if popped:
                flash(f"Popped item from Stack: [{popped.get('action')}]", "warning")
            else:
                flash("Stack Underflow: Stack is empty.", "secondary")

    elif structure == "queue":
        op = request.form.get("op", "enqueue")
        if op == "enqueue":
            sname = request.form.get("student_name", "Demo Queued Student")
            prediction_queue.enqueue({
                "student_name": sname,
                "data": {
                    "attendance": 65.0, "internal_marks": 55.0,
                    "assignment_marks": 60.0, "previous_percentage": 58.0,
                    "study_hours": 2.5, "failed_subjects": 1
                }
            })
            flash(f"Enqueued '{sname}' into FIFO Prediction Buffer. Queue Size: {prediction_queue.size()}", "success")
        elif op == "process_all":
            processed = PredictionService.process_queue_synchronously(db_path=db_path)
            flash(f"Dequeued and processed {len(processed)} predictions in FIFO order.", "success")

    return render_template(
        "dsa_demo.html",
        demo_results=demo_results,
        ht_stats={
            "capacity": student_hash_table.capacity,
            "count": student_hash_table.size(),
            "load_factor": student_hash_table.load_factor()
        },
        bst_count=len(student_bst),
        stack_history=operation_stack.get_history()[:10],
        queue_items=prediction_queue.get_all(),
        linked_list_nodes=student_linked_list.to_list()
    )

def model_evaluation():
    """Displays Decision Tree training metrics, confusion matrix, and feature importances."""
    metadata = predictor.metadata
    if not metadata and Path(Config.METADATA_PATH).exists():
        with open(Config.METADATA_PATH, "r", encoding="utf-8") as f:
            metadata = json.load(f)
    return render_template("model_evaluation.html", metadata=metadata)

def retrain_model_action():
    """Retrains the Decision Tree model and updates metadata."""
    try:
        train_and_evaluate_model()
        predictor._load_artifacts()
        flash("Decision Tree model successfully retrained and reloaded into memory!", "success")
    except Exception as e:
        flash(f"Retraining failed: {e}", "danger")
    return redirect(url_for("model_evaluation"))

def about():
    """Displays project report synopsis, architecture, and college documentation."""
    return render_template("about.html")

def api_predict():
    """JSON API endpoint for programmatic inference."""
    data = request.get_json(silent=True) or request.form.to_dict()
    if not data:
        return jsonify({"error": "No input payload provided"}), 400
    try:
        res = PredictionService.predict_and_record(
            student_data=data,
            save_to_db=False
        )
        return jsonify(res), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 422

def not_found_error(error):
    return render_template("404.html"), 404

def internal_error(error):
    return render_template("500.html"), 500

def create_app(config_class=Config):
    """Application factory for Flask web server."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize SQLite database schema
    init_db(app.config["DATABASE_PATH"])

    # Seed initial students if database is newly initialized
    _seed_initial_students_if_empty(app.config["DATABASE_PATH"])

    # Synchronize custom DSA in-memory structures from DB
    StudentService.sync_dsa_structures(app.config["DATABASE_PATH"])

    # Register URL rules
    app.add_url_rule("/", "dashboard", dashboard)
    app.add_url_rule("/students", "list_students", list_students)
    app.add_url_rule("/students/new", "create_student_page", create_student_page, methods=["GET", "POST"])
    app.add_url_rule("/students/<student_id>", "view_student", view_student)
    app.add_url_rule("/students/<student_id>/edit", "edit_student_page", edit_student_page, methods=["GET", "POST"])
    app.add_url_rule("/students/<student_id>/delete", "delete_student_action", delete_student_action, methods=["POST"])
    app.add_url_rule("/students/<student_id>/predict", "predict_student_record", predict_student_record, methods=["POST"])
    app.add_url_rule("/students/undo", "undo_action", undo_action, methods=["POST"])
    app.add_url_rule("/predict", "predict_page", predict_page, methods=["GET", "POST"])
    app.add_url_rule("/predictions/history", "prediction_history", prediction_history)
    app.add_url_rule("/dsa-demo", "dsa_demo", dsa_demo)
    app.add_url_rule("/dsa-demo/<structure>", "dsa_demo_action", dsa_demo_action, methods=["POST"])
    app.add_url_rule("/model-evaluation", "model_evaluation", model_evaluation)
    app.add_url_rule("/model-evaluation/retrain", "retrain_model_action", retrain_model_action, methods=["POST"])
    app.add_url_rule("/about", "about", about)
    app.add_url_rule("/api/predict", "api_predict", api_predict, methods=["POST"])

    # Register error handlers
    app.register_error_handler(404, not_found_error)
    app.register_error_handler(500, internal_error)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host=Config.HOST, port=Config.PORT, debug=True)
