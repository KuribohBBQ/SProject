import duckdb as db
import pandas as pd
from typing import List
from models import Professor, Student
from calc_compatibility import calculate_compatibility
from generate import generate_random_instance

def convert_to_parquet(students: List[Student], professors: List[Professor]) -> None:
    con = db.connect()

    rows = []

    for student in students:
        student_name = student.name
        student_scores = student.interest_score_list
        emplID = student.emplID

        for professor in professors:
            professor_name = professor.name
            professor_scores = professor.interest_score_list

            compatibility_score = calculate_compatibility(
                studentscores=student_scores,
                professorscores=professor_scores
            )

            rows.append({
                "studentName": student_name,
                "EMPLID": emplID,
                "professorName": professor_name,
                "compatibilityScore": float(compatibility_score)
            })

    df = pd.DataFrame(rows)

    con.register("matches", df)

    con.execute("""
        COPY matches TO 'matches.parquet' (FORMAT PARQUET)
    """)

    con.close()

if __name__ == "__main__":
    students, professors = generate_random_instance()
    convert_to_parquet(students, professors)
