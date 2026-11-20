import unittest
import tempfile
from pathlib import Path

from main import StudentPerformance


class TestStudentPerformance(unittest.TestCase):

    def test_actual_student_dataset(self):
        csv_path = Path(__file__).parent / "data" / "students.csv"

        students = StudentPerformance(csv_path)
        data = students.load_data()

        self.assertEqual(len(data), 12)
        self.assertEqual(len(students), 12)

        self.assertIn("student_id", data.columns)
        self.assertIn("study_hours", data.columns)
        self.assertIn("assessment_score", data.columns)
        self.assertEqual(
            data["student_id"].nunique(), 12
        )

        self.assertTrue(
            (data["study_hours"] >= 0).all()
        )

        self.assertTrue(
            data["assessment_score"].between(0, 100).all()
        )

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.csv_path = Path(self.temp_dir.name) / "students.csv"

        self.csv_path.write_text(
            "student_id,study_hours,assessment_score\n"
            "S001,2,50\n"
            "S002,4,70\n"
            "S003,6,90\n",
            encoding="utf-8"
        )

        self.students = StudentPerformance(self.csv_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_csv_loading(self):
        data = self.students.load_data()
        self.assertEqual(len(data), 3)

    def test_average_calculations(self):
        self.students.load_data()
        stats = self.students.calculate_statistics()

        self.assertEqual(stats["average_study_hours"], 4.0)
        self.assertEqual(stats["average_score"], 70.0)

    def test_len_special_method(self):
        self.students.load_data()
        self.assertEqual(len(self.students), 3)

    def test_class_creation(self):
        self.assertIsInstance(self.students, StudentPerformance)

    def test_invalid_and_missing_values(self):
        self.csv_path.write_text(
            "student_id,study_hours,assessment_score\n"
            "S001,2,50\n"
            "S002,bad,70\n"
            "S003,4,\n"
            "S004,6,105\n"
            "S005,-1,40\n"
            "S006,6,90\n"
            "S007,,60\n"
            ",3,60\n"
            "S008,3,-5\n",
            encoding="utf-8"
        )

        data = self.students.load_data()

        self.assertEqual(len(data), 2)
        self.assertEqual(
            data["student_id"].tolist(),
            ["S001", "S006"]
        )

        data = self.students.load_data()
        self.assertEqual(len(data), 2)

    def test_no_valid_records(self):
        self.csv_path.write_text(
            "student_id,study_hours,assessment_score\n"
            "S001,-2,50\n"
            "S002,3,110\n",
            encoding="utf-8"
        )

        with self.assertRaises(ValueError):
            self.students.load_data()

    def test_missing_csv_file(self):
        missing_file = Path(self.temp_dir.name) / "missing.csv"
        students = StudentPerformance(missing_file)

        with self.assertRaises(FileNotFoundError):
            students.load_data()

    def test_missing_required_column(self):
        self.csv_path.write_text(
            "student_id,study_hours\n"
            "S001,2\n",
            encoding="utf-8"
        )

        with self.assertRaises(ValueError):
            self.students.load_data()


if __name__ == "__main__":
    unittest.main()