# Test Results – Student Performance Dashboard

## 1. Testing Overview

The StudentPerformance class was tested using Python unittest and pytest.

## 2. Test Cases

1. CSV data loading
2. Average study hours calculation
3. Average assessment score calculation
4. Class object creation
5. __len__() special method
6. Handling invalid and missing values
7. Handling datasets with no valid records
8. Handling a missing CSV file
9. Handling missing required columns
10. Validation of the actual student dataset

## 3. Test Results

All 9 unittest test methods passed successfully.

The pytest test run also completed successfully with all tests passing.

## 4. Dataset Validation

The actual dataset contains 12 student records.

- Student IDs are unique.
- Study hours are non-negative.
- Assessment scores are between 0 and 100.
- Required CSV columns are present.

## 5. Conclusion

The tests successfully verified CSV loading, statistical calculations, data validation, invalid-value handling, and the class special method.