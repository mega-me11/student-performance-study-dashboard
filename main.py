
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")  # Allows charts to be saved without a GUI
import matplotlib.pyplot as plt


# Find project folders relative to this Python file
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "students.csv"
OUTPUT_DIR = BASE_DIR / "outputs"


class StudentPerformance:
    """Load and analyze student study hours and assessment scores."""

    def __init__(self, csv_file):
        self.csv_file = Path(csv_file)
        self.data = pd.DataFrame()

    def load_data(self):
        """Load the CSV and remove invalid records."""

        if not self.csv_file.exists():
            raise FileNotFoundError(
                f"Dataset not found: {self.csv_file}"
            )

        data = pd.read_csv(self.csv_file)

        required_columns = [
            "student_id",
            "study_hours",
            "assessment_score",
        ]

        if not all(column in data.columns for column in required_columns):
            raise ValueError(
                f"CSV must contain these columns: {required_columns}"
            )

        data = data[required_columns].copy()

        # Convert numeric columns; invalid values become missing
        data["study_hours"] = pd.to_numeric(
            data["study_hours"], errors="coerce"
        )
        data["assessment_score"] = pd.to_numeric(
            data["assessment_score"], errors="coerce"
        )

        # Remove records with missing or invalid values
        data = data.dropna(subset=required_columns)
        data["student_id"] = data["student_id"].astype(str).str.strip()
        data = data[data["student_id"] != ""]
        data = data[data["study_hours"] >= 0]
        data = data[data["assessment_score"].between(0, 100)]

        if data.empty:
            raise ValueError("The dataset contains no valid student records.")

        self.data = data.reset_index(drop=True)
        return self.data

    def __len__(self):
        """Return the number of valid student records."""
        return len(self.data)

    def calculate_statistics(self):
        """Calculate summary statistics and correlation."""

        if self.data.empty:
            raise ValueError("Load the dataset before calculating statistics.")

        hours = self.data["study_hours"]
        scores = self.data["assessment_score"]

        # NumPy correlation requires variation in both variables
        if hours.nunique() > 1 and scores.nunique() > 1:
            correlation = float(np.corrcoef(hours, scores)[0, 1])
        else:
            correlation = None

        return {
            "student_count": len(self),
            "average_study_hours": round(float(hours.mean()), 2),
            "average_score": round(float(scores.mean()), 2),
            "median_score": round(float(scores.median()), 2),
            "minimum_score": round(float(scores.min()), 2),
            "maximum_score": round(float(scores.max()), 2),
            "score_standard_deviation": round(float(scores.std()), 2),
            "study_hours_score_correlation": (
                round(correlation, 3)
                if correlation is not None
                else None
            ),
        }

    def create_charts(self):
        """Save two charts in the outputs folder."""

        if self.data.empty:
            raise ValueError("Load the dataset before creating charts.")

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        # Chart 1: Study hours versus assessment score
        plt.figure(figsize=(8, 5))
        plt.scatter(
            self.data["study_hours"],
            self.data["assessment_score"],
        )
        plt.xlabel("Study Hours")
        plt.ylabel("Assessment Score")
        plt.title("Study Hours vs Assessment Scores")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / "study_hours_vs_scores.png")
        plt.close()

        # Chart 2: Average score for each study-hour value
        average_scores = self.data.groupby(
            "study_hours"
        )["assessment_score"].mean()

        plt.figure(figsize=(8, 5))
        average_scores.plot(kind="bar")
        plt.xlabel("Study Hours")
        plt.ylabel("Average Assessment Score")
        plt.title("Average Score by Study Hours")
        plt.xticks(rotation=0)
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / "average_scores_by_hours.png")
        plt.close()


def main():
    """Run the complete analysis."""

    try:
        students = StudentPerformance(DATA_FILE)
        students.load_data()

        statistics = students.calculate_statistics()
        students.create_charts()

        print("\nSTUDENT PERFORMANCE DASHBOARD")
        print("=" * 35)

        for name, value in statistics.items():
            print(f"{name.replace('_', ' ').title()}: {value}")

        print("\nCharts saved in the outputs folder.")

    except (FileNotFoundError, ValueError, pd.errors.ParserError) as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
