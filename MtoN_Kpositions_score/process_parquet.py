import duckdb as db
import random
from collections import deque
from models import Professor, Student
import time
from generate import generate_random_instance
from typing import List, Optional
from calc_stability import calculate_stability

def convert_to_parquet(students: List[Student], professors: List[Professor]):

    con = db.connect()

    #row to hold dictionary values {studentName, professorName, stabilityScore}
    rows = []

    #loop through students
    for student in students:
        student_name = student.name
        student_scores = student.interest_score_list
        #loop through each professor for each student to calculate stability
        for professor in professors:
            professor_name = professor.name
            professor_scores = professor.interest_score_list

            stability_score = calculate_stability(studentscores= student_scores, professorscores= professor_scores)

            #put values into row
            rows.append({
                "studentName": student_name,
                "professorName": professor_name,
                "stabilityScore": stability_score
            })

     # register the data with DuckDB
    con.register("matches", rows)

    # write to parquet
    con.execute("""
        COPY matches TO 'matches.parquet' (FORMAT PARQUET)
    """)

    con.close()