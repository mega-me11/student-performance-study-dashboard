
from pathlib import Path

from flask import Flask, jsonify
from main import StudentPerformance

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "students.csv"

app = Flask(
    __name__,
    static_folder="frontend",
    static_url_path=""
)

@app.route("/")
def home():
    return app.send_static_file("index.html")

@app.route("/api/results")
def get_results():
    try:
        students = StudentPerformance(DATA_FILE)
        data = students.load_data()

        statistics = students.calculate_statistics()

        student_records = []

        for _, row in data.iterrows():
            student_records.append({
                "name": str(row["student_id"]),
                "study_hours": float(row["study_hours"]),
                "marks": float(row["assessment_score"])
            })

        return jsonify({
            "students": student_records,
            "statistics": statistics
        })

    except (FileNotFoundError, ValueError) as error:
        return jsonify({"error": str(error)}), 400

    except Exception as error:
        return jsonify({"error": str(error)}), 500

if __name__ == "__main__":
    app.run(debug=True)