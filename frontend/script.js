// STUDENT PERFORMANCE DASHBOARD

const sampleStudents = [
    { name: "Rahul", study_hours: 5, marks: 85 },
    { name: "Priya", study_hours: 7, marks: 92 },
    { name: "Amit", study_hours: 3, marks: 65 },
    { name: "Sneha", study_hours: 6, marks: 88 },
    { name: "Rohan", study_hours: 2, marks: 55 }
];

let marksChart = null;
let studyChart = null;

// Show loading message
function showLoading() {
    document.getElementById("studentTable").innerHTML =
        '<tr><td colspan="4">Loading student data...</td></tr>';
}

// Show error message
function showError(message) {
    document.getElementById("errorMessage").textContent = message;
}

// Display statistics
function displayStatistics(students) {
    const total = students.length;

    const averageMarks = students.reduce(
        (sum, s) => sum + Number(s.marks), 0
    ) / total;

    const averageHours = students.reduce(
        (sum, s) => sum + Number(s.study_hours), 0
    ) / total;

    const highestMarks = Math.max(
        ...students.map(s => Number(s.marks))
    );

    document.getElementById("totalStudents").textContent = total;
    document.getElementById("averageMarks").textContent =
        averageMarks.toFixed(2);

    document.getElementById("averageHours").textContent =
        averageHours.toFixed(2) + " hrs";

    document.getElementById("highestMarks").textContent =
        highestMarks;
}

// Display student table
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

        [student.name, student.study_hours, marks, performance]
            .forEach(value => {
                const cell = document.createElement("td");
                cell.textContent = value;
                row.appendChild(cell);
            });

        table.appendChild(row);
    });
}

// Display charts
function displayCharts(students) {

    if (typeof Chart === "undefined") {
        showError("Chart.js could not load. Please check your internet connection.");
        return;
    }

    if (marksChart) marksChart.destroy();
    if (studyChart) studyChart.destroy();

    const names = students.map(s => s.name);
    const marks = students.map(s => Number(s.marks));

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

    studyChart = new Chart(
        document.getElementById("studyChart"),
        {
            type: "scatter",
            data: {
                datasets: [{
                    label: "Study Hours vs Marks",
                    data: students.map(s => ({
                        x: Number(s.study_hours),
                        y: Number(s.marks)
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

// Load dashboard with sample data
function testDashboard() {
    try {
        showLoading();
        displayStatistics(sampleStudents);
        displayStudents(sampleStudents);
        displayCharts(sampleStudents);

        document.getElementById("errorMessage").textContent = "";
    } catch (error) {
        console.error(error);
        showError("Unable to display dashboard data.");
    }
}

// Connect to Python backend when it is ready
async function loadDashboard() {
    try {
        const response = await fetch(
            "http://127.0.0.1:5000/api/results"
        );

        if (!response.ok) {
            throw new Error("Backend response failed.");
        }

        const data = await response.json();

        if (!data.students || data.students.length === 0) {
            throw new Error("No student data found.");
        }

        displayStatistics(data.students);
        displayStudents(data.students);
        displayCharts(data.students);

        document.getElementById("errorMessage").textContent = "";

    } catch (error) {
        console.error(error);
        showError(error.message);
    }
}

// Start dashboard
document.addEventListener("DOMContentLoaded", testDashboard);