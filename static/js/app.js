/**
 * AI Student Risk System - Client Side Scripting
 * Handles Chart.js initializations, UI validations, and interactive elements.
 */

document.addEventListener("DOMContentLoaded", function () {
    // Enable Bootstrap Tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Confirmation on deletion forms
    const deleteForms = document.querySelectorAll(".form-delete-confirm");
    deleteForms.forEach(form => {
        form.addEventListener("submit", function (e) {
            const studentId = form.getAttribute("data-student-id") || "this student";
            const confirmed = confirm(`Are you sure you want to delete ${studentId}? You can undo this action from the Students page.`);
            if (!confirmed) {
                e.preventDefault();
            }
        });
    });

    // Real-time calculation helper on prediction form (composite score estimator)
    const attInput = document.getElementById("attendance");
    const intInput = document.getElementById("internal_marks");
    const assnInput = document.getElementById("assignment_marks");
    const prevInput = document.getElementById("previous_percentage");
    const previewContainer = document.getElementById("academic-composite-preview");

    function updatePreview() {
        if (!attInput || !intInput || !assnInput || !prevInput || !previewContainer) return;
        const att = parseFloat(attInput.value) || 0;
        const intMarks = parseFloat(intInput.value) || 0;
        const assn = parseFloat(assnInput.value) || 0;
        const prev = parseFloat(prevInput.value) || 0;

        const avgScore = ((att * 0.25) + (intMarks * 0.35) + (assn * 0.20) + (prev * 0.20)).toFixed(1);
        previewContainer.textContent = `Estimated Academic Index: ${avgScore}/100`;
    }

    if (attInput) {
        [attInput, intInput, assnInput, prevInput].forEach(elem => {
            if (elem) elem.addEventListener("input", updatePreview);
        });
        updatePreview();
    }
});
