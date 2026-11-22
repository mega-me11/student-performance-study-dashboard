
let marksChart = null;
let studyChart = null;

// Display error or status messages
function showError(message) {
    document.getElementById("errorMessage").textContent = message;
}

// Display summary statistics
function displayStatistics(students) {
    const total = students.length;

    const averageMarks = students.reduce(
        (sum, student) => sum + Number(student.marks), 0
    ) / total;

    const averageHours = students.reduce(
        (sum, student) => sum + Number(student.study_hours), 0
    ) / total;

    const highestMarks = Math.max(
        ...students.map(student => Number(student.marks))
    );

    document.getElementById("totalStudents").textContent = total;

    document.getElementById("averageMarks").textContent =
        averageMarks.toFixed(2);

    document.getElementById("averageHours").textContent =
        averageHours.toFixed(2) + " hrs";

    document.getElementById("highestMarks").textContent =
        highestMarks;
}

// Display student records in the table
function displayStudents(students) {
    const table = document.getElementById("studentTable");

    table.innerHTML = "";

    students.forEach(student => {
        const marks = Number(student.marks);

        let performance;

        if (marks >= 80) {
            performance = "Excellent";
        } else if (marks >= 60) {
            performance = "Good";
        } else {
            performance = "Needs Improvement";
        }

        const row = document.createElement("tr");

        [
            student.name,
            student.study_hours,
            marks,
            performance
        ].forEach(value => {
            const cell = document.createElement("td");
            cell.textContent = value;
            row.appendChild(cell);
        });

        table.appendChild(row);
    });
}

// Display charts using Chart.js
function displayCharts(students) {

    if (typeof Chart === "undefined") {
        showError("Chart.js could not load. Check your internet connection.");
        return;
    }

    if (marksChart) marksChart.destroy();
    if (studyChart) studyChart.destroy();

    const names = students.map(student => student.name);

    const marks = students.map(
        student => Number(student.marks)
    );

    // Student Marks Comparison
    marksChart = new Chart(
        document.getElementById("marksChart"),
        {
            type: "bar",

            data: {
                labels: names,

                datasets: [{
                    label: "Student Marks",
                    data: marks,
                    backgroundColor: "#4e79d9"
                }]
            },

            options: {
                responsive: true,

                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        }
    );

    // Study Hours vs Marks
    studyChart = new Chart(
        document.getElementById("studyChart"),
        {
            type: "scatter",

            data: {
                datasets: [{
                    label: "Study Hours vs Marks",

                    data: students.map(student => ({
                        x: Number(student.study_hours),
                        y: Number(student.marks)
                    })),

                    backgroundColor: "#e67e22"
                }]
            },

            options: {
                responsive: true,

                scales: {
                    x: {
                        type: "linear",

                        title: {
                            display: true,
                            text: "Study Hours"
                        }
                    },

                    y: {
                        beginAtZero: true,
                        max: 100,

                        title: {
                            display: true,
                            text: "Marks"
                        }
                    }
                }
            }
        }
    );
}

// Fetch student data from Flask backend
async function loadDashboard() {

    try {
        showError("Loading dashboard data...");

        const response = await fetch("/api/results");

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Unable to fetch student data.");
        }

        if (!data.students || data.students.length === 0) {
            throw new Error("No student records found.");
        }

        displayStatistics(data.students);

        displayStudents(data.students);

        displayCharts(data.students);

        if (typeof Chart !== "undefined") {
            showError("");
        }

    } catch (error) {

        console.error(error);

        showError(error.message);
    }
}

// Start dashboard after page loads
document.addEventListener("DOMContentLoaded", loadDashboard);
